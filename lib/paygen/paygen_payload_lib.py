# -*- coding: utf-8 -*-
# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Hold the functions that do the real work generating payloads."""

from __future__ import print_function

import base64
import datetime
import json
import os
import shutil
import tempfile

from chromite.lib import chroot_util
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_logging as logging
from chromite.lib import image_lib
from chromite.lib import osutils
from chromite.lib import path_util
from chromite.lib.paygen import download_cache
from chromite.lib.paygen import filelib
from chromite.lib.paygen import gspaths
from chromite.lib.paygen import partition_lib
from chromite.lib.paygen import signer_payloads_client
from chromite.lib.paygen import urilib
from chromite.lib.paygen import utils

from chromite.scripts import build_dlc
from chromite.scripts import cros_set_lsb_release


DESCRIPTION_FILE_VERSION = 2

# See class docs for functionality information. Configured to reserve 6GB and
# consider each individual task as consuming 6GB. Therefore we won't start a
# new task unless available memory is about 12GB (including base utilization).
_mem_semaphore = utils.MemoryConsumptionSemaphore(
    system_available_buffer_bytes=2**31 + 2**32,  # 6 GB
    single_proc_max_bytes=2**31 + 2**32,  # 6 GB
    quiescence_time_seconds=60.0,
    unchecked_acquires=4)


class Error(Exception):
  """Base class for payload generation errors."""


class UnexpectedSignerResultsError(Error):
  """This is raised when signer results don't match our expectations."""


class PayloadVerificationError(Error):
  """Raised when the generated payload fails to verify."""


class PaygenPayload(object):
  """Class to manage the process of generating and signing a payload."""

  # 250 GB of cache.
  CACHE_SIZE = 250 * 1024 * 1024 * 1024

  # 10 minutes.
  _SEMAPHORE_TIMEOUT = 10 * 60

  # What keys do we sign payloads with, and what size are they?
  PAYLOAD_SIGNATURE_KEYSETS = ('update_signer',)
  PAYLOAD_SIGNATURE_SIZES_BYTES = (2048 // 8,)  # aka 2048 bits in bytes.

  TEST_IMAGE_NAME = 'chromiumos_test_image.bin'
  RECOVERY_IMAGE_NAME = 'recovery_image.bin'
  BASE_IMAGE_NAME = 'chromiumos_base_image.bin'

  _KERNEL = 'kernel'
  _ROOTFS = 'root'

  def __init__(self, payload, work_dir, sign=False, verify=False,
               private_key=None):
    """Init for PaygenPayload.

    Args:
      payload: An instance of gspaths.Payload describing the payload to
               generate.
      work_dir: A working directory inside the chroot to put temporary files.
          This can NOT be shared among different runs of PaygenPayload otherwise
          there would be file collisions. Among the things that may go into this
          direcotry are intermediate image files, extracted partitions,
          different logs and metadata files, payload and metadata hashes along
          with their signatures, the payload itself, postinstall config file,
          intermediate files that is generated by the signer, etc.
      sign: Boolean saying if the payload should be signed (normally, you do).
      verify: whether the payload should be verified after being generated
      private_key: If passed, the payload will be signed with that private key.
                   If also verify is True, the public key is extracted from the
                   private key and is used for verification.
    """
    self.payload = payload
    self.work_dir = work_dir
    self._verify = verify
    self._private_key = private_key
    self._public_key = None

    self.src_image_file = os.path.join(work_dir, 'src_image.bin')
    self.tgt_image_file = os.path.join(work_dir, 'tgt_image.bin')

    self.partition_names = None
    self.tgt_partitions = None
    self.src_partitions = None

    self._appid = ''

    self.payload_file = os.path.join(work_dir, 'delta.bin')
    self.log_file = os.path.join(work_dir, 'delta.log')
    self.description_file = os.path.join(work_dir, 'delta.json')
    self.metadata_size = 0
    self.metadata_hash_file = os.path.join(work_dir, 'metadata_hash')
    self.payload_hash_file = os.path.join(work_dir, 'payload_hash')

    self._postinst_config_file = os.path.join(work_dir, 'postinst_config')

    self.signer = None
    if sign:
      self._SetupSigner(payload.build)

    # This cache dir will be shared with other processes, but we need our own
    # instance of the cache manager to properly coordinate.
    self._cache = download_cache.DownloadCache(
        self._FindCacheDir(), cache_size=PaygenPayload.CACHE_SIZE)

  def _MetadataUri(self, uri):
    """Given a payload uri, find the uri for the metadata signature."""
    return uri + '.metadata-signature'

  def _LogsUri(self, uri):
    """Given a payload uri, find the uri for the logs."""
    return uri + '.log'

  def _JsonUri(self, uri):
    """Given a payload uri, find the uri for the json payload description."""
    return uri + '.json'

  def _FindCacheDir(self):
    """Helper for deciding what cache directory to use.

    Returns:
      Returns a directory suitable for use with a DownloadCache.
    """
    return os.path.join(path_util.GetCacheDir(), 'paygen_cache')

  def _SetupSigner(self, payload_build):
    """Sets up the signer based on which bucket the payload is supposed to go.

    Args:
      payload_build: The build defined for the payload.
    """
    self.signed_payload_file = self.payload_file + '.signed'
    self.metadata_signature_file = self._MetadataUri(self.signed_payload_file)

    if (payload_build and
        payload_build.bucket == gspaths.ChromeosReleases.BUCKET):
      # We are using the official buckets, so sign it with official signers.
      self.signer = signer_payloads_client.SignerPayloadsClientGoogleStorage(
          payload_build, self.work_dir)
      # We set the private key to None so we don't accidentally use a valid
      # passed private key to verify the image.
      self._private_key = None
    else:
      # Otherwise use a private key for signing and verifying the payload. If
      # no private_key was provided, use a test key.
      if not self._private_key:
        self._private_key = os.path.join(constants.CHROMITE_DIR, 'ssh_keys',
                                         'testing_rsa')
      self.signer = signer_payloads_client.UnofficialSignerPayloadsClient(
          self._private_key, self.work_dir)

    if self._private_key and self.signer:
      self._public_key = os.path.join(self.work_dir, 'public_key.pem')
      self.signer.ExtractPublicKey(self._public_key)

  def _GetDlcImageParams(self, tgt_image, src_image=None):
    """Returns parameters related to target and source DLC images.

    Args:
      tgt_image: The target image.
      src_image: The source image.

    Returns:
      A tuple of three parameters that was discovered from the image: The DLC
      ID, The DLC package and its release AppID.
    """

    def _GetImageParams(image):
      """Returns the parameters of a single DLC image.

      Args:
        image: The input image.

      Returns:
        Same values as _GetDlcImageParams()
      """
      mount_point = os.path.join(self.work_dir, 'mount-point')
      osutils.MountDir(image, mount_point, mount_opts=('ro',))
      try:
        lsb_release = utils.ReadLsbRelease(mount_point)
      finally:
        osutils.UmountDir(mount_point)

      dlc_id = lsb_release[build_dlc.DLC_ID_KEY]
      dlc_package = lsb_release[build_dlc.DLC_PACKAGE_KEY]
      appid = lsb_release[build_dlc.DLC_APPID_KEY]

      if gspaths.IsDLCImage(image):
        if dlc_id != image.dlc_id:
          raise Error('The DLC ID (%s) inferred from the file path does not '
                      'match the one (%s) from the lsb-release.' %
                      (image.dlc_id, dlc_id))
        if dlc_package != image.dlc_package:
          raise Error('The DLC package (%s) inferred from the file path '
                      'does not match the one (%s) from the lsb-release.' %
                      (image.dlc_package, dlc_package))

      return dlc_id, dlc_package, appid

    tgt_dlc_id, tgt_dlc_package, tgt_appid = _GetImageParams(tgt_image)
    if src_image:
      src_dlc_id, src_dlc_package, src_appid = _GetImageParams(src_image)
      if tgt_dlc_id != src_dlc_id:
        raise Error('Source (%s) and target (%s) DLC IDs do not match.' %
                    (src_dlc_id, tgt_dlc_id))
      if tgt_dlc_package != src_dlc_package:
        raise Error('Source (%s) and target (%s) DLC packages do not match.'
                    % (src_dlc_package, tgt_dlc_package))
      # This may cause problems when we try to switch a board to a different App
      # ID. If that ever happens the following few lines should be deleted.
      if tgt_appid != src_appid:
        raise Error('Source (%s) and target (%s) App IDs do not match.' %
                    (src_appid, tgt_appid))

    return tgt_dlc_id, tgt_dlc_package, tgt_appid

  def _GetPlatformImageParams(self, image):
    """Returns parameters related to target or source platform images.

    Since this function is mounting a GPT image, if the mount (for reasons like
    a bug, etc), changes the bits on the image, then the image cannot be trusted
    after this call.

    Args:
      image: The input image.

    Returns:
      The release APPID of the image.
    """
    # Mount the ROOT-A partition of the image. The reason we don't mount the
    # extracted partition directly is that if by mistake/bug the mount changes
    # the bits on the partition, then we will create a payload for a changed
    # partition which is not equivalent to the original partition. So just mount
    # the partition of the GPT image and even if it changes, then who cares.
    #
    # TODO(crbug.com/925203): Replace this with image_lib.LoopbackPartition()
    # once the mentioned bug is resolved.
    with osutils.TempDir(base_dir=self.work_dir) as mount_point:
      with image_lib.LoopbackPartitions(image, destination=mount_point,
                                        part_ids=(constants.PART_ROOT_A,)):
        sysroot_dir = os.path.join(mount_point,
                                   'dir-%s' % constants.PART_ROOT_A)
        lsb_release = utils.ReadLsbRelease(sysroot_dir)
        app_id = lsb_release.get(cros_set_lsb_release.LSB_KEY_APPID_RELEASE)
        if app_id is None:
          board = lsb_release.get(cros_set_lsb_release.LSB_KEY_APPID_BOARD)
          logging.error('APPID is missing in board %s. In some boards that do '
                        'not do auto updates, like amd64-generic, this is '
                        'expected, otherwise this is an error.', board)
        return app_id

  def _PreparePartitions(self):
    """Prepares parameters related to partitions of the given image.

    This function basically distinguishes between normal platform images and DLC
    images and creates and checks parameters necessary for each of them.
    """
    tgt_image_type = partition_lib.LookupImageType(self.tgt_image_file)
    if self.payload.src_image:
      src_image_type = partition_lib.LookupImageType(self.src_image_file)
      if (tgt_image_type != src_image_type and
          partition_lib.CROS_IMAGE in (tgt_image_type, src_image_type)):
        raise Error('Source (%s) and target (%s) images have different types.' %
                    (src_image_type, tgt_image_type))

    if tgt_image_type == partition_lib.DLC_IMAGE:
      logging.info('Detected a DLC image.')

      # DLC module image has only one partition which is the image itself.
      dlc_id, dlc_package, self._appid = self._GetDlcImageParams(
          self.tgt_image_file,
          src_image=self.src_image_file if self.payload.src_image else None)
      self.partition_names = ('dlc/%s/%s' % (dlc_id, dlc_package),)
      self.tgt_partitions = (self.tgt_image_file,)
      self.src_partitions = (self.src_image_file,)

    elif tgt_image_type == partition_lib.CROS_IMAGE:
      logging.info('Detected a Chromium OS image.')

      self.partition_names = (self._ROOTFS, self._KERNEL)
      self.tgt_partitions = tuple(os.path.join(self.work_dir,
                                               'tgt_%s.bin' % name)
                                  for name in self.partition_names)
      self.src_partitions = tuple(os.path.join(self.work_dir,
                                               'src_%s.bin' % name)
                                  for name in self.partition_names)

      partition_lib.ExtractRoot(self.tgt_image_file, self.tgt_partitions[0])
      partition_lib.ExtractKernel(self.tgt_image_file, self.tgt_partitions[1])
      if self.payload.src_image:
        partition_lib.ExtractRoot(self.src_image_file, self.src_partitions[0])
        partition_lib.ExtractKernel(self.src_image_file, self.src_partitions[1])

      # This step should be done after extracting partitions, look at the
      # _GetPlatformImageParams() documentation for more info.
      self._appid = self._GetPlatformImageParams(self.tgt_image_file)
      # Reset the target image file path so no one uses it later.
      self.tgt_image_file = None

      # Makes sure we have generated postinstall config for major version 2 and
      # platform image.
      self._GeneratePostinstConfig(True)
    else:
      raise Error('Invalid image type %s' % tgt_image_type)

  def _RunGeneratorCmd(self, cmd):
    """Wrapper for run in chroot.

    Run the given command inside the chroot. It will automatically log the
    command output. Note that the command's stdout and stderr are combined into
    a single string.

    Args:
      cmd: Program and argument list in a list. ['delta_generator', '--help']

    Raises:
      cros_build_lib.RunCommandError if the command exited with a nonzero code.
    """

    try:
      # Run the command.
      result = cros_build_lib.run(
          cmd,
          redirect_stdout=True,
          enter_chroot=True,
          combine_stdout_stderr=True)
    except cros_build_lib.RunCommandError as e:
      # Dump error output and re-raise the exception.
      logging.error('Nonzero exit code (%d), dumping command output:\n%s',
                    e.result.returncode, e.result.output)
      raise

    self._StoreLog('Output of command: ' + result.cmdstr)
    self._StoreLog(result.output.decode('utf-8', 'replace'))

  @staticmethod
  def _BuildArg(flag, dict_obj, key, default=None):
    """Returns a command-line argument iff its value is present in a dictionary.

    Args:
      flag: the flag name to use with the argument value, e.g. --foo; if None
            or an empty string, no flag will be used
      dict_obj: a dictionary mapping possible keys to values
      key: the key of interest; e.g. 'foo'
      default: a default value to use if key is not in dict_obj (optional)

    Returns:
      If dict_obj[key] contains a non-False value or default is non-False,
      returns a string representing the flag and value arguments
      (e.g. '--foo=bar')
    """
    val = dict_obj.get(key) or default
    return '%s=%s' % (flag, str(val))


  def _PrepareImage(self, image, image_file):
    """Download an prepare an image for delta generation.

    Preparation includes downloading, extracting and converting the image into
    an on-disk format, as necessary.

    Args:
      image: an object representing the image we're processing, either
             UnsignedImageArchive or Image type from gspaths module.
      image_file: file into which the prepared image should be copied.
    """

    logging.info('Preparing image from %s as %s', image.uri, image_file)

    # Figure out what we're downloading and how to handle it.
    image_handling_by_type = {
        'signed': (None, True),
        'test': (self.TEST_IMAGE_NAME, False),
        'recovery': (self.RECOVERY_IMAGE_NAME, True),
        'base': (self.BASE_IMAGE_NAME, True),
    }
    if gspaths.IsImage(image):
      # No need to extract.
      extract_file = None
    elif gspaths.IsUnsignedImageArchive(image):
      extract_file, _ = image_handling_by_type[image.get('image_type',
                                                         'signed')]
    else:
      raise Error('Unknown image type %s' % type(image))

    # Are we donwloading an archive that contains the image?
    if extract_file:
      # Archive will be downloaded to a temporary location.
      with tempfile.NamedTemporaryFile(
          prefix='image-archive-', suffix='.tar.xz', dir=self.work_dir,
          delete=False) as temp_file:
        download_file = temp_file.name
    else:
      download_file = image_file

    # Download the image file or archive. If it was just a local file, ignore
    # caching and do a simple copy. TODO(crbug.com/926034): Add a caching
    # mechanism for local files.
    if urilib.GetUriType(image.uri) == urilib.TYPE_LOCAL:
      filelib.Copy(image.uri, download_file)
    else:
      self._cache.GetFileCopy(image.uri, download_file)

    # If we downloaded an archive, extract the image file from it.
    if extract_file:
      cmd = ['tar', '-xJf', download_file, extract_file]
      cros_build_lib.run(cmd, cwd=self.work_dir)

      # Rename it into the desired image name.
      shutil.move(os.path.join(self.work_dir, extract_file), image_file)

      # It should be safe to delete the archive at this point.
      # TODO(crbug/1016555): consider removing the logging once resolved.
      logging.info('Removing %s', download_file)
      os.remove(download_file)

  def _GeneratePostinstConfig(self, run_postinst):
    """Generates the postinstall config file

    This file is used in update engine's major version 2.

    Args:
      run_postinst: Whether the updater should run postinst or not.
    """
    # In major version 2 we need to explicity mark the postinst on the root
    # partition to run.
    osutils.WriteFile(self._postinst_config_file,
                      'RUN_POSTINSTALL_root=%s\n' %
                      ('true' if run_postinst else 'false'))

  def _GenerateUnsignedPayload(self):
    """Generate the unsigned delta into self.payload_file."""
    # Note that the command run here requires sudo access.
    logging.info('Generating unsigned payload as %s', self.payload_file)

    tgt_image = self.payload.tgt_image
    cmd = ['delta_generator',
           '--major_version=2',
           '--out_file=' + path_util.ToChrootPath(self.payload_file),
           # Target image args: (The order of partitions are important.)
           '--partition_names=' + ':'.join(self.partition_names),
           '--new_partitions=' +
           ':'.join(path_util.ToChrootPath(x) for x in self.tgt_partitions)]

    if os.path.exists(self._postinst_config_file):
      cmd += ['--new_postinstall_config_file=' +
              path_util.ToChrootPath(self._postinst_config_file)]

    if tgt_image.build:
      # These next 6 parameters are basically optional and the update engine
      # client ignores them, but we can keep them to identify parameters of a
      # payload by looking at itself.  Either all of the build options should be
      # passed or non of them. So, set the default key to 'test' only if it
      # didn't have a key but it had other build options like channel, board,
      # etc.
      cmd += ['--new_channel=' + tgt_image.build.channel,
              '--new_board=' + tgt_image.build.board,
              '--new_version=' + tgt_image.build.version,
              self._BuildArg('--new_build_channel', tgt_image, 'image_channel',
                             default=tgt_image.build.channel),
              self._BuildArg('--new_build_version', tgt_image, 'image_version',
                             default=tgt_image.build.version),
              self._BuildArg('--new_key', tgt_image, 'key',
                             default='test' if tgt_image.build.channel else '')]

    if self.payload.src_image:
      src_image = self.payload.src_image
      cmd += ['--old_partitions=' +
              ':'.join(path_util.ToChrootPath(x) for x in self.src_partitions)]

      if src_image.build:
        # See above comment for new_channel.
        cmd += ['--old_channel=' + src_image.build.channel,
                '--old_board=' + src_image.build.board,
                '--old_version=' + src_image.build.version,
                self._BuildArg('--old_build_channel', src_image,
                               'image_channel',
                               default=src_image.build.channel),
                self._BuildArg('--old_build_version', src_image,
                               'image_version',
                               default=src_image.build.version),
                self._BuildArg(
                    '--old_key', src_image, 'key',
                    default='test' if src_image.build.channel else '')]

    self._RunGeneratorCmd(cmd)

  def _GenerateHashes(self):
    """Generate a payload hash and a metadata hash.

    Works from an unsigned update payload.

    Returns:
      payload_hash as a string, metadata_hash as a string.
    """
    logging.info('Calculating hashes on %s.', self.payload_file)

    # How big will the signatures be.
    signature_sizes = [str(size) for size in self.PAYLOAD_SIGNATURE_SIZES_BYTES]

    cmd = ['delta_generator',
           '--in_file=' + path_util.ToChrootPath(self.payload_file),
           '--signature_size=' + ':'.join(signature_sizes),
           '--out_hash_file=' +
           path_util.ToChrootPath(self.payload_hash_file),
           '--out_metadata_hash_file=' +
           path_util.ToChrootPath(self.metadata_hash_file)]

    self._RunGeneratorCmd(cmd)

    return (osutils.ReadFile(self.payload_hash_file, mode='rb'),
            osutils.ReadFile(self.metadata_hash_file, mode='rb'))

  def _GenerateSignerResultsError(self, format_str, *args):
    """Helper for reporting errors with signer results."""
    msg = format_str % args
    logging.error(msg)
    raise UnexpectedSignerResultsError(msg)

  def _SignHashes(self, hashes):
    """Get the signer to sign the hashes with the update payload key via GS.

    May sign each hash with more than one key, based on how many keysets are
    required.

    Args:
      hashes: List of hashes to be signed.

    Returns:
      List of lists which contain each signed hash.
      [[hash_1_sig_1, hash_1_sig_2], [hash_2_sig_1, hash_2_sig_2]]
    """
    logging.info('Signing payload hashes with %s.',
                 ', '.join(self.PAYLOAD_SIGNATURE_KEYSETS))

    # Results look like:
    #  [[hash_1_sig_1, hash_1_sig_2], [hash_2_sig_1, hash_2_sig_2]]
    hashes_sigs = self.signer.GetHashSignatures(
        hashes,
        keysets=self.PAYLOAD_SIGNATURE_KEYSETS)

    if hashes_sigs is None:
      self._GenerateSignerResultsError('Signing of hashes failed')
    if len(hashes_sigs) != len(hashes):
      self._GenerateSignerResultsError(
          'Count of hashes signed (%d) != Count of hashes (%d).',
          len(hashes_sigs),
          len(hashes))

    # Make sure that the results we get back the expected number of signatures.
    for hash_sigs in hashes_sigs:
      # Make sure each hash has the right number of signatures.
      if len(hash_sigs) != len(self.PAYLOAD_SIGNATURE_SIZES_BYTES):
        self._GenerateSignerResultsError(
            'Signature count (%d) != Expected signature count (%d)',
            len(hash_sigs),
            len(self.PAYLOAD_SIGNATURE_SIZES_BYTES))

      # Make sure each hash signature is the expected size.
      for sig, sig_size in zip(hash_sigs, self.PAYLOAD_SIGNATURE_SIZES_BYTES):
        if len(sig) != sig_size:
          self._GenerateSignerResultsError(
              'Signature size (%d) != expected size(%d)',
              len(sig),
              sig_size)

    return hashes_sigs

  def _WriteSignaturesToFile(self, signatures):
    """Write each signature into a temp file in the chroot.

    Args:
      signatures: A list of signaturs to write into file.

    Returns:
      The list of files in the chroot with the same order as signatures.
    """
    file_paths = []
    for signature in signatures:
      path = tempfile.NamedTemporaryFile(dir=self.work_dir, delete=False).name
      osutils.WriteFile(path, signature)
      file_paths.append(path_util.ToChrootPath(path))

    return file_paths

  def _InsertSignaturesIntoPayload(self, payload_signatures,
                                   metadata_signatures):
    """Put payload and metadta signatures into the payload we sign.

    Args:
      payload_signatures: List of signatures for the payload.
      metadata_signatures: List of signatures for the metadata.
    """
    logging.info('Inserting payload and metadata signatures into %s.',
                 self.signed_payload_file)

    payload_signature_file_names = self._WriteSignaturesToFile(
        payload_signatures)
    metadata_signature_file_names = self._WriteSignaturesToFile(
        metadata_signatures)

    cmd = ['delta_generator',
           '--in_file=' + path_util.ToChrootPath(self.payload_file),
           '--payload_signature_file=' + ':'.join(payload_signature_file_names),
           '--metadata_signature_file=' +
           ':'.join(metadata_signature_file_names),
           '--out_file=' + path_util.ToChrootPath(self.signed_payload_file)]

    self._RunGeneratorCmd(cmd)

  def _StoreMetadataSignatures(self, signatures):
    """Store metadata signatures related to the payload.

    Our current format for saving metadata signatures only supports a single
    signature at this time.

    Args:
      signatures: A list of metadata signatures in binary string format.
    """
    if len(signatures) != 1:
      self._GenerateSignerResultsError(
          'Received %d metadata signatures, only a single signature supported.',
          len(signatures))

    logging.info('Saving metadata signatures in %s.',
                 self.metadata_signature_file)

    encoded_signature = base64.b64encode(signatures[0])

    with open(self.metadata_signature_file, 'w+b') as f:
      f.write(encoded_signature)

  def GetPayloadPropertiesMap(self, payload_path):
    """Returns the payload's properties attributes in dictionary.

    The payload description contains a dictionary of key/values describing the
    characteristics of the payload. Look at
    update_engine/payload_generator/payload_properties.cc for the basic
    description of these values.

    In addition we add the following three keys to description file:

    "appid": The APP ID associated with this payload.
    "public_key": The public key the payload was signed with.

    Args:
      payload_path: The path to the payload file.

    Returns:
      A map of payload properties that can be directly used to create the
      payload.json file.
    """
    try:
      payload_path = path_util.ToChrootPath(payload_path)
    except ValueError:
      # Copy the payload inside the chroot and try with that path instead.
      logging.info('The payload is not in the chroot. We will copy it there in '
                   'order to get its properties.')
      copied_payload = os.path.join(self.work_dir, 'copied-payload.bin')
      shutil.copyfile(payload_path, copied_payload)
      payload_path = path_util.ToChrootPath(copied_payload)

    props_file = os.path.join(self.work_dir, 'properties.json')
    cmd = ['delta_generator',
           '--in_file=' + payload_path,
           '--properties_file=' + path_util.ToChrootPath(props_file),
           '--properties_format=json']
    self._RunGeneratorCmd(cmd)
    props_map = json.load(open(props_file))

    # delta_generator assigns empty string for signatures when the payload is
    # not signed. Replace it with 'None' so the json.dumps() writes 'null' as
    # the value to be consistent with the current scheme and not break GE.
    key = 'metadata_signature'
    if not props_map[key]:
      props_map[key] = None

    props_map['appid'] = self._appid

    # Add the public key if it exists.
    if self._public_key:
      props_map['public_key'] = base64.b64encode(
          osutils.ReadFile(self._public_key, mode='rb')).decode('utf-8')

    # We need the metadata size later for payload verification. Just grab it
    # from the properties file.
    self.metadata_size = props_map['metadata_size']

    return props_map

  def _StorePayloadJson(self, metadata_signatures):
    """Generate the payload description json file.

    Args:
      metadata_signatures: A list of signatures in binary string format.
    """
    # Decide if we use the signed or unsigned payload file.
    payload_file = self.payload_file
    if self.signer:
      payload_file = self.signed_payload_file

    # Currently we have no way of getting the appid from the payload itself. So
    # just put what we got from the image itself (if any).
    props_map = self.GetPayloadPropertiesMap(payload_file)

    # Check that the calculated metadata signature is the same as the one on the
    # payload.
    if metadata_signatures:
      if len(metadata_signatures) != 1:
        self._GenerateSignerResultsError(
            'Received %d metadata signatures, only one supported.',
            len(metadata_signatures))
      metadata_signature = base64.b64encode(metadata_signatures[0])
      if metadata_signature != props_map['metadata_signature']:
        raise Error('Calculated metadata signature (%s) and the signature in'
                    ' the payload (%s) do not match.' %
                    (metadata_signature, props_map['metadata_signature']))

    # Convert to Json.
    payload_json = json.dumps(props_map, sort_keys=True)
    # Write out the results.
    osutils.WriteFile(self.description_file, payload_json)

  def _StoreLog(self, log):
    """Store any log related to the payload.

    Write out the log to a known file name. Mostly in its own function
    to simplify unittest mocks.

    Args:
      log: The delta logs as a single string.
    """
    osutils.WriteFile(self.log_file, log, mode='a')

  def _SignPayload(self):
    """Wrap all the steps for signing an existing payload.

    Returns:
      List of payload signatures, List of metadata signatures.
    """
    # Create hashes to sign or even if signing not needed.  TODO(ahassani): In
    # practice we don't need to generate hashes if we are not signing, so when
    # devserver stopped depending on cros_generate_update_payload. this can be
    # reverted.
    payload_hash, metadata_hash = self._GenerateHashes()

    if not self.signer:
      return (None, None)

    # Sign them.
    # pylint: disable=unpacking-non-sequence
    payload_signatures, metadata_signatures = self._SignHashes(
        [payload_hash, metadata_hash])
    # pylint: enable=unpacking-non-sequence

    # Insert payload and metadata signature(s).
    self._InsertSignaturesIntoPayload(payload_signatures, metadata_signatures)

    # Store metadata signature(s).
    self._StoreMetadataSignatures(metadata_signatures)

    return (payload_signatures, metadata_signatures)

  def _Create(self):
    """Create a given payload, if it doesn't already exist."""

    logging.info('Generating %s payload %s',
                 'delta' if self.payload.src_image else 'full', self.payload)

    # TODO(lamontjones): It may make sense to use a different mem_semaphore here
    # around the calls to self._PrepareImage, rather than wrapping all of it in
    # the mem_semaphor that was created for delta_generator.  In any case, too
    # many gsutil cp commands running in parallel seems to result in higher
    # likelihood of EAGAIN from thread creation.
    #
    # Run delta_generator for the purpose of generating an unsigned payload with
    # considerations for available memory. This is an adaption of the previous
    # version which used a simple semaphore. This was highly limiting because
    # while delta_generator is parallel there are single threaded portions
    # of it that were taking a very long time (i.e. long poles).
    #
    # Sometimes if a process cannot acquire the lock for a long
    # period of time, the builder kills the process for not outputting any
    # logs. So here we try to acquire the lock with a timeout of ten minutes in
    # a loop and log some output so not to be killed by the builder.
    while True:
      acq_result = _mem_semaphore.acquire(timeout=self._SEMAPHORE_TIMEOUT)
      if acq_result.result:
        logging.info('Acquired lock (reason: %s)', acq_result.reason)
        break
      else:
        logging.info('Failed to acquire the lock in 10 minutes (reason: %s)'
                     ', trying again ...', acq_result.reason)
    try:
      # Fetch and prepare the tgt image.
      self._PrepareImage(self.payload.tgt_image, self.tgt_image_file)

      # Fetch and prepare the src image.
      if self.payload.src_image:
        self._PrepareImage(self.payload.src_image, self.src_image_file)

      # Setup parameters about the payload like whether it is a DLC or not. Or
      # parameters like the APPID, etc.
      self._PreparePartitions()

      # Generate the unsigned payload.
      self._GenerateUnsignedPayload()
    finally:
      _mem_semaphore.release()

    # Sign the payload, if needed.
    _, metadata_signatures = self._SignPayload()

    # Store hash and signatures json.
    self._StorePayloadJson(metadata_signatures)

  def _VerifyPayload(self):
    """Checks the integrity of the generated payload.

    Raises:
      PayloadVerificationError when the payload fails to verify.
    """
    if self.signer:
      payload_file_name = self.signed_payload_file
      metadata_sig_file_name = self.metadata_signature_file
    else:
      payload_file_name = self.payload_file
      metadata_sig_file_name = None

    is_delta = bool(self.payload.src_image)

    logging.info('Applying %s payload and verifying result',
                 'delta' if is_delta else 'full')

    # This command checks both the payload integrity and applies the payload
    # to source and target partitions.
    cmd = ['check_update_payload', path_util.ToChrootPath(payload_file_name),
           '--check', '--type', 'delta' if is_delta else 'full',
           '--disabled_tests', 'move-same-src-dst-block',
           '--part_names']
    cmd.extend(self.partition_names)
    cmd += ['--dst_part_paths']
    cmd.extend(path_util.ToChrootPath(x) for x in self.tgt_partitions)
    if metadata_sig_file_name:
      cmd += ['--meta-sig', path_util.ToChrootPath(metadata_sig_file_name)]

    cmd += ['--metadata-size', str(self.metadata_size)]

    if is_delta:
      cmd += ['--src_part_paths']
      cmd.extend(path_util.ToChrootPath(x) for x in self.src_partitions)

    # We signed it with the private key, now verify it with the public key.
    if self._public_key:
      cmd += ['--key', path_util.ToChrootPath(self._public_key)]

    self._RunGeneratorCmd(cmd)

  def _UploadResults(self):
    """Copy the payload generation results to the specified destination."""

    logging.info('Uploading payload to %s.', self.payload.uri)

    # Deliver the payload to the final location.
    if self.signer:
      urilib.Copy(self.signed_payload_file, self.payload.uri)
    else:
      urilib.Copy(self.payload_file, self.payload.uri)

    # Upload payload related artifacts.
    urilib.Copy(self.log_file, self._LogsUri(self.payload.uri))
    urilib.Copy(self.description_file, self._JsonUri(self.payload.uri))

  def Run(self):
    """Create, verify and upload the results."""
    logging.info('* Starting payload generation')
    start_time = datetime.datetime.now()

    self._Create()
    if self._verify:
      self._VerifyPayload()
    self._UploadResults()

    end_time = datetime.datetime.now()
    logging.info('* Finished payload generation in %s', end_time - start_time)

def CreateAndUploadPayload(payload, sign=True, verify=True):
  """Helper to create a PaygenPayloadLib instance and use it.

  Mainly can be used as a single function to help with parallelism.

  Args:
    payload: An instance of gspaths.Payload describing the payload to generate.
    sign: Boolean saying if the payload should be signed (normally, you do).
    verify: whether the payload should be verified (default: True)
  """
  # We need to create a temp directory inside the chroot so be able to access
  # from both inside and outside the chroot.
  with chroot_util.TempDirInChroot() as work_dir:
    PaygenPayload(payload, work_dir, sign=sign, verify=verify).Run()


def GenerateUpdatePayload(tgt_image, payload, src_image=None, work_dir=None,
                          private_key=None, check=None,
                          out_metadata_hash_file=None):
  """Generates output payload and verifies its integrity if needed.

  Args:
    tgt_image: The path (or uri) to the image.
    payload: The path (or uri) to the output payload
    src_image: The path (or uri) to the source image. If passed, a delta payload
        is generated.
    work_dir: A working directory inside the chroot. The None, caller has the
        responsibility to cleanup this directory after this function returns.
    private_key: The private key to sign the payload.
    check: If True, it will check the integrity of the generated payload.
    out_metadata_hash_file: The output metadata hash file.
  """
  tgt_image = gspaths.Image(uri=tgt_image)
  src_image = gspaths.Image(uri=src_image) if src_image else None
  payload = gspaths.Payload(tgt_image=tgt_image, src_image=src_image,
                            uri=payload)
  with chroot_util.TempDirInChroot() as temp_dir:
    work_dir = work_dir if work_dir is not None else temp_dir
    paygen = PaygenPayload(payload, work_dir, sign=private_key is not None,
                           verify=check, private_key=private_key)
    paygen.Run()

    # TODO(ahassani): These are basically a hack because devserver is still need
    # the metadata hash file to sign it. But signing logic has been moved to
    # paygen and in the future this is not needed anymore.
    if out_metadata_hash_file:
      shutil.copy(paygen.metadata_hash_file, out_metadata_hash_file)


def GenerateUpdatePayloadPropertiesFile(payload, output=None):
  """Generates the update payload's properties file.

  Args:
    payload: The path to the input payload.
    output: The path to the output properties json file. If None, the file will
        be placed by appending '.json' to the payload file itself.
  """
  if not output:
    output = payload + '.json'

  with chroot_util.TempDirInChroot() as work_dir:
    paygen = PaygenPayload(None, work_dir)
    properties_map = paygen.GetPayloadPropertiesMap(payload)
    properties_json = json.dumps(properties_map, sort_keys=True)
    osutils.WriteFile(output, properties_json)
