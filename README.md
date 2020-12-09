# Switch Logo Patcher

Modualized version of [friedkeenan's switch-logo-patcher](https://github.com/friedkeenan/switch-logo-patcher)

As a script it produces a zip containing the patches at the target output location.
As a module it returns a bytestring of the zip.

Creates the IPS patches needed to replace the Switch logo on boot.

The logo you want to change the Switch logo to must be the same size as the original logo, which is 308x350. Anything else and the program won't let you progress.

You don't need to dump the original logo to use this, but if you don't specify the original logo, each patch will be 400+ KiB.

### Usage

```
usage: gen_patches.py [-h] [-o OLD_LOGO] patches_dir new_logo

positional arguments:
  patches_dir           The directory where the generated patches.zip will be
                        dumped
  new_logo              The new logo image

optional arguments:
  -h, --help            show this help message and exit
  -o OLD_LOGO, --old_logo OLD_LOGO
                        The original logo image
```
