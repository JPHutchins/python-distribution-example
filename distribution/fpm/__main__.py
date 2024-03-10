# Copyright (c) 2024 JP Hutchins
# SPDX-License-Identifier: Apache-2.0

"""Create packages with FPM."""

import subprocess

fpm_command = (
    "fpm",
    "--force",
    "-s",
    "dir",
    "-t",
    "deb",
    "-p",
    "test.deb",
    "--name",
    "myapp",
    "--license",
    "apache-2.0",
    "--version",
    "0.0.0",
    "--architecture",
    "all",
    "--description",
    "test description",
    "--url",
    "https://github.com/JPHutchins/python-distribution-example",
    "--maintainer",
    "JP Hutchins <jphutchins@gmail.com>",
    "--after-install",
    "distribution/fpm/after-install.sh",
    "--after-remove",
    "distribution/fpm/after-remove.sh",
    "dist/myapp=usr/share/"
)

assert subprocess.run(fpm_command).returncode == 0
