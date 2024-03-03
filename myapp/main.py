# Copyright (c) 2024 JP Hutchins
# SPDX-License-Identifier: Apache-2.0

"""The application entry point."""

import argparse
from importlib.metadata import version
from typing import Final


def app() -> None:
    """The application entry point."""

    parser: Final = argparse.ArgumentParser(description="Example application.")
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="Display the version.",
    )
    parser.add_argument(
        "-i",
        "--input",
        action="store_true",
        default=False,
        help="Await any key before exiting.",
    )

    args: Final = parser.parse_args()

    if args.version is True:
        print(version("myapp"))
        raise SystemExit(0)

    print("Hello, World!")

    if args.input is True:
        input("Press any key to exit...")
