# rootifier-cli
Flattens Nokia SROS config like the Juniper "display set" format.

Based on [Rootifier by hellt](https://github.com/hellt/Rootifier). The difference is that this script is meant be used from the CLI.
It also handles a few exceptions to the configuration format the original script does not.
Output of this script should be 100% copy-pasteable in a Nokia SROS device. 

Usage: 
./rootifier-cli.py <router.cfg>

or 

cat <router.cfg> | ./rootifier-cli.py
