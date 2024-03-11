# Python Distribution Example

This repository demonstrates one way of creating a portable Python application
that can be installed and run without any external dependencies.  This is
useful for distributing Python applications to users without a Python
environment installed or for distributing a Python application via a package
manager.

## Tools Used

- envr: manage environment variables, PATH, and python venv
- poetry: manage python dependencies and build
- PyInstaller: create a "one-dir" "executable" of a python application
- WiX v4: create a Windows installer, `*.msi`, that creates a double-clickable
  version of the app, adds the app to the system PATH, adds an app folder to
  the Start Menu, and optionally adds a shortcut to the desktop
- FPM: create `*.deb` and `*.rpm` Linux packages that install the app
  to `/usr/share/` and add a symlink to `/usr/bin/*`.