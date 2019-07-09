# contrib/

This folder provides some functionality that may not be 100% supported yet. Things here may break
at any time and are not necessarily expected to be updated before the breaking changes are accepted.


## gen_call_scripts, call_templates/ and call_scripts/
The `call_templates` directory contains a set of example json input files for making api calls.
The `call_scripts` directory is an ignored directory generated by the `gen_call_scripts` script.
`gen_call_scripts` will create scripts of the form `service__method` that call their corresponding endpoint.
They look for `service__method_input.json` files and write to `service__method_output.json` in the call_scripts directory.