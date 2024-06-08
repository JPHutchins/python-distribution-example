# Copyright (c) 2024 JP Hutchins
# SPDX-License-Identifier: Apache-2.0

"""Create a windows installer for the application."""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Final

from distribution.portable import DIST, make_portable

THIS_DIR: Final = Path(os.path.dirname(os.path.realpath(__file__)))

print("Creating the windows installer...\n")

assert subprocess.run(("dotnet", "clean"), cwd=THIS_DIR).returncode == 0

print("Building the portable application...\n")
result: Final = make_portable()
if isinstance(result, Exception):
    raise result

ENV: Final = os.environ.copy() | {
    "COMPANY_NAME": result.company_name,
    "PRODUCT_NAME": result.product_name,
    "APP_NAME": result.app_name,
    "EXE_NAME": result.exe_name,
    "VERSION": result.version,
    "PORTABLE_PATH": result.portable_path,
    "MSI_NAME": result.app_name_full,
}

print("\nBuilding the windows installer...\n")
assert (
    subprocess.run(
        ("dotnet", "build", "-c", "Release"), env=ENV, cwd=THIS_DIR
    ).returncode
    == 0
)

# copy the MSI to dist
shutil.copy(f"{THIS_DIR / 'bin' / 'Release' / ENV['MSI_NAME']}.msi", DIST)

print()
print(f"The windows installer is at {DIST / ENV['MSI_NAME']}.msi")
