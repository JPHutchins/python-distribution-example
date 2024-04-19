# Python Distribution Example

This repository demonstrates one way of creating a portable Python application
that can be installed and run without any external dependencies.  This is
useful for distributing Python applications to users without a Python
environment, or for distributing a Python application via a package
manager.

## Setup

> These steps only need to be completed on first-time setup.

### Install Dependencies

- Python >=3.10, <3.13
- [Poetry](https://python-poetry.org/docs/): I recommend installing `pipx`
  first and then using `pipx` to install `poetry`.

> Refer to [release.yaml](.github/workflows/release.yaml) for platform-specific
  installer dependencies.  The installer builds for Windows, Linux, and MacOS
  run on GitHub runners, so you don't need to install the requirements unless
  you are troubleshooting a platform-specific installer build script.

### Clone this Repository

> If you'd like to track your own changes in GitHub, then you should
  [fork](https://github.com/JPHutchins/python-distribution-example/fork) this
  repository, and then clone your fork.

```
git clone git@github.com:JPHutchins/python-distribution-example.git
```

### Install the Python venv

- change directory to the root of the cloned repository:
  ```
  cd python-distribution-example
  ```
- install the venv with poetry
  ```
  poetry install
  ```
  > The venv is installed to `/.venv`

## Build

> Make sure to complete the [setup](#setup) first.

### Activate the Development Environment

> This step is required before running or building the app.

```
. ./envr.ps1
```

Now you can run the app within the Python venv:

```
jpsapp --help
```

### Build the `sdist` and `wheel`

```
poetry build
```

The build output is at `dist/`.

### Build the Portable App for Your Host Platform

```
python -m distribution.portable
```

The build output is at `dist/jpsapp-<version>-<platform>-<arch>`, e.g.
`dist/jpsapp-1.0.0-windows-amd64`, as well is in a ZIP archive of the same name.

## Tools Used

- [GitHub Actions](https://github.com/features/actions): automate the build and
  release of the application on GitHub runners
- [envr](https://github.com/JPhutchins/envr): manage environment variables,
  PATH, and Python venv
- [poetry](https://python-poetry.org/): manage Python dependencies and build
- [PyInstaller](https://github.com/pyinstaller/pyinstaller): create a "one-dir"
  portable "executable" of the Python application
- [WiX v4](https://wixtoolset.org/): create a Windows installer, `*.msi`, that
  creates a double-clickable version of the app, adds the app to the system
  PATH, adds an app folder to the Start Menu, and optionally adds a shortcut to
  the desktop
- [FPM](https://github.com/jordansissel/fpm): create `*.deb` and `*.rpm` Linux
  packages that install the app to `/usr/share/` and add a symlink to
  `/usr/bin/*`.
