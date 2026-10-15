📦 LPIT — Linux & Android Package Information Tool

Universal Package Inspector for Linux & Android

Inspect packages. Understand your system. Work smarter.

""Version" (https://img.shields.io/badge/version-3.0-38BDF8?style=flat-square)" (https://github.com/linuxways25)
""Language" (https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)" (https://www.python.org/)
""Dependencies" (https://img.shields.io/badge/dependencies-zero-22C55E?style=flat-square)" (#-requirements)
""Platform" (https://img.shields.io/badge/platform-Linux%20%7C%20Android-86EFAC?style=flat-square)" (#-supported-platforms)
""License" (https://img.shields.io/badge/license-MIT-blue?style=flat-square)" (LICENSE)

LPIT (Linux & Android Package Information Tool) is a lightweight, Python-based command-line utility designed to help users inspect installed software packages and retrieve useful package information across supported Linux distributions and Android environments.

Built with simplicity, portability, and usability in mind, LPIT provides a unified interface for exploring package information without requiring third-party Python libraries.

Developed under the LinuxWays open-source ecosystem.

---

📑 Table of Contents

- "✨ Key Features" (#-key-features)
- "🎯 Why LPIT?" (#-why-lpit)
- "🖥️ Supported Platforms" (#️-supported-platforms)
- "⚙️ Requirements" (#️-requirements)
- "📥 Installation" (#-installation)
- "🚀 Getting Started" (#-getting-started)
- "💻 Usage Examples" (#-usage-examples)
- "📦 Supported Package Managers" (#-supported-package-managers)
- "🔐 Security and Privacy" (#-security-and-privacy)
- "🛠️ Troubleshooting" (#️-troubleshooting)
- "🗺️ Roadmap" (#️-roadmap)
- "🤝 Contributing" (#-contributing)
- "📜 License" (#-license)
- "👨‍💻 Author" (#-author)

---

✨ Key Features

- Multi-platform support — Designed for compatible Linux distributions and Android environments such as Termux.
- Multiple package ecosystems — Supports package inspection across common Linux package managers and Android package tools.
- Zero third-party Python dependencies — Uses Python's standard library.
- Lightweight design — Suitable for command-line workflows and resource-conscious environments.
- Administrator-friendly — Helps Linux administrators and engineers investigate installed software.
- Beginner-friendly interface — Intended to make package information easier to understand.
- Portable Python implementation — No compiled extension modules required.
- Open-source development — Designed to support learning, experimentation, and community contributions.

«Note: Available features and commands depend on the actual implementation, detected package manager, operating system, and user permissions.»

🎯 Why LPIT?

Linux distributions and Android environments use different package management systems. Finding equivalent information across these environments can require learning different commands and output formats.

LPIT aims to simplify that experience through a single, lightweight Python utility.

Challenge| LPIT's goal
Different package managers| Provide a unified inspection workflow
Complex package commands| Make common operations easier to access
Limited resources| Keep the tool lightweight
Additional Python dependencies| Use the standard library
Multiple operating environments| Support a broader range of package ecosystems

Important: LPIT is a package information and inspection utility, not a replacement for the underlying package manager.

🖥️ Supported Platforms

LPIT is designed for the following environments:

Platform| Package ecosystem| Status
Arch Linux| pacman| Intended support
Debian| APT / dpkg| Intended support
Ubuntu| APT / dpkg| Intended support
Fedora| DNF / RPM| Intended support
RHEL-compatible systems| DNF / RPM| Intended support
SUSE Linux| Zypper / RPM| Intended support
Android| Android package tools| Environment-dependent
Termux| pkg / dpkg| Intended support

Actual support depends on which detection and inspection features are implemented and tested in the current release. Not every package manager provides identical information.

⚙️ Requirements

Before using LPIT, make sure the following requirements are met:

- Python 3 installed on your system.
- Access to a supported package manager or package database.
- A terminal or command-line environment.
- Appropriate permissions to read the required package information.

Check Python

python3 --version

Expected output example:

Python 3.x.x

LPIT is designed to use Python's standard library, so installing additional Python packages should not be necessary.

📥 Installation

Option 1 — Clone the repository

git clone https://github.com/linuxways25/LinuxWays-Package-Information-Tool.git
cd LinuxWays-Package-Information-Tool

Repository note: Replace the repository URL above with the actual LPIT repository URL if its published name differs.

Option 2 — Download the source code

1. Open the LPIT GitHub repository.
2. Select Code → Download ZIP.
3. Extract the downloaded archive.
4. Open a terminal in the extracted directory.

Verify the source file

ls

Locate the main Python script before proceeding.

Run LPIT

If the main script is named "lpit.py", run:

python3 lpit.py --help

If the project uses a different filename, substitute the correct filename.

«Tip: Check the help output first. It shows the arguments and options actually supported by your installed version.»

🚀 Getting Started

Follow these steps to start using LPIT.

Step 1 — Open a terminal

Launch your terminal on Linux or open Termux on Android.

Step 2 — Verify Python

python3 --version

Step 3 — Navigate to the project directory

cd LinuxWays-Package-Information-Tool

Use the directory name created during installation.

Step 4 — View the available options

python3 lpit.py --help

Step 5 — Run a supported operation

Choose a command from the help output and follow its usage instructions.

---

💻 Usage Examples

The following commands illustrate how to inspect packages using the underlying system tools. They are examples of native package-manager commands, not guarantees that LPIT exposes identical command-line options.

Arch Linux

Inspect a package:

pacman -Qi bash

Search installed packages:

pacman -Q

Debian and Ubuntu

Inspect an installed package:

dpkg -s bash

List installed packages:

dpkg -l

Fedora and RHEL

Inspect an installed package:

rpm -qi bash

List installed packages:

rpm -qa

openSUSE

Inspect an installed package:

zypper info bash

Android / Termux

Check installed Termux packages:

pkg list-installed

Inspect a package:

apt show bash

Package availability and output vary by environment.

Using LPIT directly: Run "python3 lpit.py --help" to discover the exact syntax supported by your version. Do not assume that native package-manager options are also LPIT options.

📦 Supported Package Managers

LPIT targets package ecosystems commonly encountered in Linux administration.

Package manager / tool| Ecosystem
pacman| Arch Linux
APT / dpkg| Debian, Ubuntu and derivatives
DNF / RPM| Fedora, RHEL and compatible distributions
Zypper| SUSE Linux
Termux "pkg"| Android / Termux

Package-manager detection, fallback behavior, and the availability of package details depend on the implementation and the environment in which LPIT runs.

🔐 Security and Privacy

LPIT is intended to be a local package inspection utility.

- Local operation: Package information is obtained from the available system environment.
- No third-party Python libraries: The intended implementation relies on the Python standard library.
- Least privilege: Run without root privileges unless a specific operation genuinely requires elevated access.
- Read-only inspection: Package inspection should not change installed packages.
- Command safety: External commands should be executed with argument lists rather than shell-interpolated user input.

Do not treat these design goals as a formal security audit. Review the source code before using LPIT on critical production systems.

🛠️ Troubleshooting

Python is not installed

Install Python using the package manager for your operating system.

On Arch Linux:

sudo pacman -S python

On Debian or Ubuntu:

sudo apt update
sudo apt install python3

On Termux:

pkg update
pkg install python

Permission denied

Try running the tool as your normal user first. Check the permissions of the script:

chmod +x lpit.py

You can then execute it directly if it has a valid Python shebang:

./lpit.py --help

Alternatively:

python3 lpit.py --help

Package manager not detected

Check which package-management commands are available:

command -v pacman
command -v apt
command -v dpkg
command -v dnf
command -v rpm
command -v zypper
command -v pkg

A compatible command being present does not always mean its package database is accessible or that every LPIT feature will work.

No package information returned

- Confirm that the package is installed.
- Verify the package name and spelling.
- Check whether the relevant package database is available.
- Review the tool's help output and error messages.

Termux compatibility problems

Termux is an Android environment, not a conventional desktop Linux distribution. Its filesystem layout, permissions, available commands, and package database differ from those of standard Linux installations.

Use Termux-native package commands when troubleshooting its environment.

---

🗺️ Roadmap

Potential areas for future development include:

- [ ] Improved package-manager detection.
- [ ] Consistent, structured package information across distributions.
- [ ] More informative error messages.
- [ ] JSON output for automation and scripting.
- [ ] Exportable package inventory reports.
- [ ] Optional interactive terminal interface.
- [ ] Expanded automated tests across supported environments.
- [ ] Clear compatibility matrix for each release.
- [ ] Optional graphical user interface.

Roadmap items are proposals, not commitments or features available in the current release.

🧪 Testing

Contributions that improve reliability and portability are welcome.

Suggested test environments:

- Arch Linux or an Arch-based distribution.
- Debian or Ubuntu.
- Fedora or another compatible RPM-based distribution.
- openSUSE.
- Android using Termux.

When reporting a problem, include:

- Operating system and version.
- Python version.
- Package manager.
- Command executed.
- Expected behavior.
- Actual output, with sensitive information removed.

Test package inspection in a disposable environment before relying on it in production.

🤝 Contributing

Contributions are welcome from Linux users, Python developers, system administrators, and open-source enthusiasts.

How to contribute

1. Fork the repository.
2. Create a feature branch.
3. Make a focused change.
4. Test the change on a supported environment.
5. Submit a pull request with a clear description.

Contribution principles

- Keep the code simple and maintainable.
- Prefer Python standard-library functionality.
- Handle missing commands and unsupported platforms gracefully.
- Never execute untrusted shell input.
- Document new options and platform-specific behavior.
- Include regression tests when fixing bugs.

For significant changes, open an issue first to discuss the proposed implementation.

📜 License

LPIT is intended to be distributed under the MIT License.

Before publishing, ensure that the repository contains a valid "LICENSE" file matching the license declared here. If a different license has been selected, update this section and the badge accordingly.

👨‍💻 Author and Project

LinuxWays — Open-Source Engineering

Developed as part of the LinuxWays ecosystem, which focuses on Linux engineering, automation, system administration, security, and platform engineering.

- GitHub: https://github.com/linuxways25
- Project organization: LinuxWays
- Language: Python 3
- Project type: Command-line utility

LinuxWays Philosophy

Minimal. Fast. Open.

Learn deeply. Build boldly. Engineer intelligently.

---

⭐ Support the Project

If LPIT is useful to you:

- Star the repository on GitHub.
- Report bugs and suggest improvements.
- Contribute code, tests, and documentation.
- Share feedback from real-world Linux and Android environments.

Every meaningful contribution helps make open-source tools more reliable, accessible, and useful.

LPIT — One tool. Multiple package ecosystems. Simpler system inspection.