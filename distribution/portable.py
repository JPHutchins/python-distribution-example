# Copyright (c) 2024 JP Hutchins
# SPDX-License-Identifier: Apache-2.0

"""Build a portable application for the host platform."""

import json
import os
import platform
import shutil
import subprocess
import zipfile
from importlib.metadata import version
from pathlib import Path
from typing import Final, NamedTuple

import pyinstaller_versionfile  # type: ignore

APP_NAME: Final = "myapp"

VERSION: Final = version(APP_NAME)
APP_NAME_FULL: Final = (
    f"{APP_NAME}-{VERSION}-{platform.system().lower()}"
    f"-{platform.machine().lower()}"
)
REPO_ROOT: Final = Path(os.environ["ENVR_ROOT"])
DIST: Final = Path(REPO_ROOT, "dist")
DIST_PATH: Final = Path(DIST, APP_NAME_FULL)
EXE_NAME: Final[str] = (
    f"{APP_NAME}.exe" if platform.system() == "Windows" else APP_NAME
)


class BuildMetadata(NamedTuple):
    company_name: str
    product_name: str
    version: str
    portable_path: str
    app_name: str = APP_NAME
    app_name_full: str = APP_NAME_FULL
    exe_name: str = EXE_NAME


def make_portable() -> Exception | BuildMetadata:
    """Build a portable application for the host platform."""

    exception: Exception | None = None

    try:
        # build the application
        assert subprocess.run(["poetry", "install"]).returncode == 0
        assert subprocess.run(["poetry", "build"]).returncode == 0

        print()

        # find the sdist archive and unpack it
        archives = list(DIST.glob(rf"{APP_NAME}-{VERSION}.tar.gz"))
        assert len(archives) == 1
        shutil.unpack_archive(archives[0], DIST)

        build_metadata: Final = BuildMetadata(
            company_name="My Example Company",
            product_name="My Example Application",
            version=VERSION,
            portable_path=str(DIST_PATH),
        )

        # create the version file (only used by Windows)
        pyinstaller_versionfile.create_versionfile(
            output_file=f"{REPO_ROOT}/build/exe_version.txt",
            version=VERSION,
            company_name=build_metadata.company_name,
            file_description="An example app packed with PyInstaller + WiX",
            product_name=build_metadata.product_name,
            internal_name=APP_NAME,
            original_filename=EXE_NAME,
            legal_copyright="Copyright (c) Myself and Contributors",
            translations=(1033, 1252),
        )

        pyinstaller_command: Final = (
            "pyinstaller",
            f"--add-data={DIST}/{APP_NAME}-{VERSION}:{APP_NAME}",
            f"--copy-metadata={APP_NAME}",
            "--noconfirm",
            "--contents-directory=src",
            f"--name={APP_NAME}",
            f"--distpath={DIST}",
            f"--workpath={REPO_ROOT}/build",
            "--collect-submodules=shellingham",
            f"{REPO_ROOT}/{APP_NAME}/__main__.py",
        ) + (
            (f"--version-file={REPO_ROOT}/build/exe_version.txt",)
            if platform.system() == "Windows"
            else ()
        )

        # build the executable
        assert subprocess.run(pyinstaller_command).returncode == 0

        # test the executable
        assert (
            "Hello, World!"
            in subprocess.run(
                [f"{DIST}/{APP_NAME}/{EXE_NAME}"], capture_output=True
            ).stdout.decode()
        )
        assert (
            VERSION
            in subprocess.run(
                [f"{DIST}/{APP_NAME}/{EXE_NAME}", "-v"], capture_output=True
            ).stdout.decode()
        )

        # copy the build to the staging folder
        shutil.copytree(Path(DIST, APP_NAME), DIST_PATH, dirs_exist_ok=True)

        # copy the LICENSE
        shutil.copy(Path(REPO_ROOT, "LICENSE"), Path(DIST_PATH, "LICENSE"))

        # make a ZIP archive
        with zipfile.ZipFile(str(DIST_PATH) + ".zip", "w") as zip_file:
            for path, _, files in os.walk(DIST_PATH):
                for file in files:
                    zip_file.write(
                        Path(path, file),
                        Path(path, file).relative_to(DIST_PATH),
                    )

    except Exception as e:
        exception = e

    return exception or build_metadata


if __name__ == "__main__":
    result = make_portable()
    if isinstance(result, Exception):
        raise result
    else:
        print("\nPortable application created succesfully!")
        print()
        print("\tFolder: ", result.portable_path)
        print("\tArchive: ", result.portable_path + ".zip")
        print()
        print(json.dumps(result._asdict()))
