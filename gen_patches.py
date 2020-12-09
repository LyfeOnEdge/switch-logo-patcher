#!/usr/bin/env python3

import io
import argparse
import zipfile
from pathlib import Path

import ips
from PIL import Image

# Build Id: offset
patch_info = {
    # AM patches
    "C79F22F18169FCD3B3698A881394F6240385CDB1": 1668164,
    "01890C643E9D6E17B2CDA77A9749ECB9A4F676D6": 1962240,
    "C088ADC91417EBAE6ADBDF3E47946858CAFE1A82": 1962240,
    "3EC573CB22744A993DFE281701E9CBFE66C03ABD": 1716480,

    # Vi patches
    "7B4123290DE2A6F52DE4AB72BEA1A83D11214C71": 1831168,
    "723DF02F6955D903DF7134105A16D48F06012DB1": 1835264,
    "967F4C3DFC7B165E4F7981373EC1798ACA234A45": 1573120,
    "98446A07BC664573F1578F3745C928D05AB73349": 1589504,
    "0767302E1881700608344A3859BC57013150A375": 1593600,
    "7C5894688EDA24907BC9CE7013630F365B366E4A": 1593600,
    "7421EC6021AC73DD60A635BC2B3AD6FCAE2A6481": 1536256,
    "96529C3226BEE906EE651754C33FE3E24ECAE832": 1544448,
    "D689E9FAE7CAA4EC30B0CD9B419779F73ED3F88B": 1655040,
}

def patches(new_logo_file : str, old_logo_file : str = None):
    if not old_logo_file:
        new_logo = Image.open(new_logo_file).convert("RGBA")
        if new_logo.size != (308, 350):
            raise ValueError("Invalid size for the logo")

        new_f = io.BytesIO(new_logo.tobytes())
        new_f.seek(0, 2)
        new_len = new_f.tell()
        new_f.seek(0)

        base_patch = ips.Patch()
        while new_f.tell() < new_len:
            base_patch.add_record(new_f.tell(), new_f.read(0xFFFF))
    else:
        old_logo = Image.open(old_logo_file).convert("RGBA")
        new_logo = Image.open(new_logo_file).convert("RGBA")
        if old_logo.size != (308, 350) or new_logo.size != (308, 350):
            raise ValueError("Invalid size for the logo")
        base_patch = ips.Patch.create(old_logo.tobytes(), new_logo.tobytes())

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, False) as zip_obj:
        for build_id, offset in patch_info.items():
            tmp_p = ips.Patch()
            for r in base_patch.records:
                tmp_p.add_record(r.offset + offset, r.content, r.rle_size)
            zip_obj.writestr(f"{build_id}.ips", bytes(tmp_p))
    zip_buffer.seek(0)
    return zip_buffer.read()

def patches_status(*args, **kwargs):
    try:
        return (True, patches(*args, **kwargs))
    except Exception as e:
        return (False, e)

if __name__ == "__main__":
    print("Generating Patches")
    parser = argparse.ArgumentParser()
    parser.add_argument("patches_dir", help="The directory where the patches.zip will be placed", type=Path)
    parser.add_argument("new_logo", help="The new logo image", type=Path)
    parser.add_argument("-o", "--old_logo", help="The original logo image", type=Path, default=None)
    args = parser.parse_args()
    old_logo = args.old_logo or args.new_logo
    status, val = patches_status(args.new_logo, old_logo)
    if not status:
        print(f"An error occured generating patches.\n{val}")
    else:
        with open(Path(args.patches_dir, "patches.zip"), "wb+") as patches:
            patches.write(val)
    print("Done!")