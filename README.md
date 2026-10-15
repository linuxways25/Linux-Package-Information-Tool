LPIT — Linux & Android Package Information Tool

Inspect packages. Understand your system. Work smarter.

LPIT is a lightweight Python-based utility designed to help users inspect and understand software packages across supported Linux distributions and Android environments, including Termux.

Built for Linux enthusiasts, system administrators, developers, and platform engineers, LPIT aims to make package information easier to access through a clean, user-friendly command-line interface.

---

Project Information

""Version" (https://img.shields.io/badge/version-3.0-38BDF8?style=flat-square)" (https://github.com/linuxways25)
""Python" (https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)" (https://www.python.org/)
""Dependencies" (https://img.shields.io/badge/dependencies-zero-22C55E?style=flat-square)" (#requirements)
""Platform" (https://img.shields.io/badge/platform-Linux%20%7C%20Android-86EFAC?style=flat-square)" (#supported-platforms)
""License" (https://img.shields.io/badge/license-MIT-blue?style=flat-square)" (LICENSE)

Attribute| Details
Project| LPIT
Full name| Linux & Android Package Information Tool
Version| 3.0
Language| Python 3.10+
Interface| Command-line interface (CLI)
Dependencies| Zero external Python dependencies
Platforms| Supported Linux systems and Android/Termux
License| MIT, provided the repository includes the corresponding license

Table of Contents

- "Overview" (#overview)
- "Key Objectives" (#key-objectives)
- "Supported Platforms" (#supported-platforms)
- "Requirements" (#requirements)
- "Installation" (#installation)
- "Usage" (#usage)
- "Android and Termux" (#android-and-termux)
- "Troubleshooting" (#troubleshooting)
- "Security and Privacy" (#security-and-privacy)
- "Project Roadmap" (#project-roadmap)
- "Contributing" (#contributing)
- "License" (#license)
- "Project Maintainer" (#project-maintainer)

---

Overview

Linux systems use different package managers and package databases. Finding information about installed software can therefore require different commands on different distributions.

LPIT aims to provide a consistent interface for inspecting package information while respecting the package-management tools native to each supported operating system.

Whether you work with Arch Linux, Debian, Fedora, Ubuntu, openSUSE, or Android through Termux, LPIT is intended to make package inspection simpler and more approachable.

«Design philosophy: Minimal. Fast. Open.»

Key Objectives

- Simplicity: Make package information accessible through an approachable CLI.
- Portability: Support multiple operating-system environments where compatible package tools are available.
- Lightweight operation: Avoid unnecessary third-party Python dependencies.
- Maintainability: Keep the implementation readable, modular, and easy to extend.
- User friendliness: Provide clear output and actionable error messages.
- System awareness: Detect the available environment and use appropriate package-management interfaces.

Supported Platforms

LPIT is designed for cross-platform package inspection. Actual support depends on the package managers and interfaces implemented in the current release.

Platform| Package ecosystem
Arch Linux and derivatives| pacman
Debian and Ubuntu| APT / dpkg
Fedora| DNF / RPM
RHEL-compatible distributions| DNF / RPM
openSUSE| Zypper / RPM
Android with Termux| pkg / apt

Note: The table describes the intended platform scope. Verify each backend against the current source code and target environment before treating it as fully supported.

Requirements

- Python 3.10 or newer.
- A supported operating system or Android/Termux environment.
- The relevant package-management utility for the target system.
- Appropriate permissions to access the requested package information.

LPIT requires no external Python packages if the implementation remains standard-library-only.

Installation

Option 1 — Clone the repository

Replace the repository URL below if LPIT uses a different repository name.

git clone https://github.com/linuxways25/LPIT.git
cd LPIT

Option 2 — Run the script directly

If the source file is named "lpit.py", run:

python3 lpit.py --help

If the script supports executable permissions, you can also run:

chmod +x lpit.py
./lpit.py --help

Important: Replace "LPIT.git" or "lpit.py" with the actual repository and filename if they differ. The commands above assume those names; they do not confirm the repository's current layout.

Usage

LPIT is intended to provide a consistent entry point for package inspection.

Start by checking the available command-line options:

python3 lpit.py --help

If supported by your installed version, inspect the tool's version:

python3 lpit.py --version

Use the commands shown by the help output for package searches and detailed package information. Exact subcommands and flags should match the implemented CLI.

Example native package commands

These examples demonstrate the underlying package managers, not guaranteed LPIT subcommands.

Environment| Example
Arch Linux| "pacman -Qi python"
Debian / Ubuntu| "dpkg-query -W python3"
Fedora / RHEL| "rpm -qi python3"
openSUSE| "zypper info python3"
Termux| "pkg show python"

Android and Termux

LPIT can be used on Android through the Termux terminal environment, provided the Python runtime and required package interfaces are supported.

Step 1 — Install Termux

Install Termux from a trusted distribution source, such as its official F-Droid listing or project releases.

Project: https://github.com/termux/termux-app

Step 2 — Update packages

pkg update
pkg upgrade

Step 3 — Install Python and Git

pkg install python git

Step 4 — Obtain the LPIT source

git clone https://github.com/linuxways25/LPIT.git
cd LPIT

Step 5 — Run LPIT

python lpit.py --help

Use the actual repository name and script filename if they differ.

Android limitation: Termux does not provide the same package database or system privileges as a conventional Linux distribution. LPIT should inspect Termux-managed packages rather than assume it can query Android's internal application database or system packages.

Troubleshooting

Problem| Suggested action
Python command not found| Install Python and verify with "python3 --version".
Script not found| Check the current directory and the actual script filename.
Package manager unavailable| Confirm the backend exists in the target environment.
Permission denied| Check file permissions and whether the requested operation needs elevated privileges.
Package information unavailable| Verify that the package is installed and its database is accessible.
Termux behaves differently from Linux| Check whether the requested package belongs to Termux or the Android operating system.

Security and Privacy

LPIT is intended to be a lightweight package-inspection utility.

- Prefer read-only package queries wherever possible.
- Avoid executing package installation or removal commands unless explicitly required by a documented feature.
- Do not request root access unnecessarily.
- Do not collect or transmit system information without explicit user awareness.
- Treat command output as potentially environment-specific.
- Validate external command arguments and handle errors safely.

Security properties should be confirmed through source-code review and testing; they should not be inferred solely from the project's description.

Project Roadmap

Potential areas for future development include:

- [ ] Improved package-manager detection.
- [ ] Consistent output across supported distributions.
- [ ] Clear package metadata and version reporting.
- [ ] Better error messages and exit codes.
- [ ] Automated tests for package-manager backends.
- [ ] Expanded Termux compatibility testing.
- [ ] Optional machine-readable JSON output.
- [ ] Comprehensive installation and usage documentation.

Roadmap items are proposals, not claims about features already available.

Contributing

Contributions that improve portability, reliability, documentation, testing, or usability are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make a focused change.
4. Test the change in the relevant environment.
5. Submit a pull request describing the change and its test results.

Please keep contributions readable, dependency-conscious, and compatible with the project's supported Python version.

License

LPIT is intended to be distributed under the MIT License.

See the ""LICENSE"" (LICENSE) file in the repository for the applicable terms. Ensure that the file exists and contains the complete license text before claiming the project is officially MIT-licensed.

Project Maintainer

LinuxWays

GitHub: https://github.com/linuxways25

Part of the LinuxWays ecosystem, focused on Linux, automation, platform engineering, and open-source tooling.

---
LPIT — Inspect packages. Understand your system. Work smarter.