# Copyright (c) 2024 JP Hutchins
# SPDX-License-Identifier: Apache-2.0

"""Create packages with FPM."""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Final

from distribution.portable import DIST, make_portable

THIS_DIR: Final = Path(os.path.dirname(os.path.realpath(__file__)))

print("Creating Linux packages with FPM...\n")

print("Building the portable application...\n")
result: Final = make_portable()
if isinstance(result, Exception):
    raise result

print("\nBuilding the Linux packages...")

output_types: Final = ("deb", "rpm")

for output_type in output_types:
    package_name = f"{result.app_name_full}.{output_type}"

    fpm_command = (
        "fpm",
        f"--output-type={output_type}",
        f"--package={package_name}",
        f"--version={result.version}",
    )

    print(f"Creating {package_name}...\n")
    assert subprocess.run(fpm_command, cwd=THIS_DIR).returncode == 0
    print()

    shutil.copy(f"{THIS_DIR / package_name}", DIST)

    print(f"The {output_type} package is at {DIST / package_name}")
    print()
