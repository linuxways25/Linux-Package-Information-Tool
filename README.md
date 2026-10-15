📦 LPIT — Linux & Android Package Information Tool

🔍 Inspect packages. Understand your system. Work smarter.

LPIT is a lightweight Python 3 utility designed to simplify package inspection across supported Linux distributions and Android environments, including Termux.

Built for Linux enthusiasts, system administrators, developers, and platform engineers, LPIT focuses on simplicity, portability, and a clean command-line experience.

<p align="center">
  <img src="https://img.shields.io/badge/LPIT-Version%203.0-38BDF8?style=for-the-badge&logo=linux&logoColor=white" alt="LPIT Version 3.0">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10 or newer">
</p><p align="center">
  <img src="https://img.shields.io/badge/Dependencies-Zero-22C55E?style=flat-square" alt="Zero external dependencies">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Android-86EFAC?style=flat-square&logo=linux&logoColor=black" alt="Linux and Android">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-2563EB?style=flat-square&logo=opensourceinitiative&logoColor=white" alt="MIT License"></a>
</p><p align="center">
  <strong>⚡ Minimal. 🚀 Fast. 🌐 Open.</strong><br>
  <sub>An open-source utility from the LinuxWays ecosystem.</sub>
</p>---

🧭 Table of Contents

- "📖 Overview" (#-overview)
- "✨ Key Features" (#-key-features)
- "🖥️ Supported Platforms" (#️-supported-platforms)
- "⚙️ Requirements" (#️-requirements)
- "📥 Installation" (#-installation)
- "🚀 Usage" (#-usage)
- "📱 Android and Termux" (#-android-and-termux)
- "🛠️ Troubleshooting" (#️-troubleshooting)
- "🔐 Security and Privacy" (#-security-and-privacy)
- "🗺️ Roadmap" (#️-roadmap)
- "🤝 Contributing" (#-contributing)
- "📄 License" (#-license)
- "🌐 LinuxWays" (#-linuxways)

---

📖 Overview

Linux distributions use different package managers, databases, and metadata formats. As a result, inspecting installed software often requires different commands on different systems.

LPIT aims to simplify package inspection through a consistent command-line interface, using the native package-management utilities available in supported environments.

🎯 Project Goals

- Simplify package information lookup.
- Support multiple package-management ecosystems.
- Minimize dependencies and unnecessary overhead.
- Provide readable output and helpful error messages.
- Encourage maintainable, testable Python development.
- Make package inspection more approachable for Linux and Android users.

✨ Key Features

- 📦 Package Inspection — Inspect available package metadata through supported backends.
- 🐧 Linux Compatibility — Target multiple Linux package-management ecosystems.
- 📱 Android Support — Designed for compatible Android/Termux environments.
- 🪶 Lightweight Design — Uses Python's standard library without third-party Python dependencies.
- 🧭 CLI Experience — Provides a command-line interface for package inspection.
- 🔧 Maintainability — Designed for testing, troubleshooting, and future improvements.
- 🔒 Privacy-Conscious Design — Focuses on local package inspection rather than unnecessary data collection.

Feature availability depends on the actual implementation, package-manager backend, and target environment.

🖥️ Supported Platforms

LPIT targets the following package-management ecosystems.

Platform| Package manager
Arch Linux and derivatives| "pacman"
Debian and Ubuntu| "apt" / "dpkg"
Fedora| "dnf" / "rpm"
RHEL-compatible distributions| "dnf" / "rpm"
openSUSE| "zypper"
Android / Termux| "pkg" / "apt"

«Compatibility note: The table describes the intended scope. Verify each backend against the current source code before assuming that every listed platform is fully supported.»

⚙️ Requirements

Before running LPIT, ensure your environment has:

- 🐍 Python 3.10 or newer.
- 💻 A supported Linux distribution or compatible Android/Termux environment.
- 📦 The relevant package-management utility.
- 🔑 Appropriate permissions to access the requested package information.

Check your Python installation:

python3 --version

Check Git, if you plan to clone the source:

git --version

📥 Installation

Option 1 — Clone the repository

Replace "YOUR_REPOSITORY_URL" with the actual URL of your LPIT GitHub repository.

git clone YOUR_REPOSITORY_URL
cd YOUR_REPOSITORY_DIRECTORY

Option 2 — Run from source

If your main Python file is named "lpit.py", run:

python3 lpit.py --help

If the script supports direct execution:

chmod +x lpit.py
./lpit.py --help

Note: The script filename and available options must match the actual project source.

🚀 Usage

Start by checking the available command-line options:

python3 lpit.py --help

If version reporting is implemented:

python3 lpit.py --version

Use the help output to discover the package-query syntax and supported options.

💡 Native Package Inspection Examples

The following commands demonstrate native package-manager usage. They are not LPIT-specific commands.

Environment| Example command
Arch Linux| "pacman -Qi python"
Debian / Ubuntu| "dpkg-query -W python3"
Fedora / RHEL| "rpm -qi python3"
openSUSE| "zypper info python3"
Termux| "pkg show python"

📱 Android and Termux

LPIT can be used in Termux when its Python runtime and required package interfaces are supported.

Step 1 — Install Termux

Get Termux from a trusted source:

- "Official Termux project" (https://github.com/termux/termux-app)

Step 2 — Update packages

pkg update
pkg upgrade

Step 3 — Install Python and Git

pkg install python git

Step 4 — Obtain the LPIT source

Clone the repository using the actual LPIT repository URL, then navigate to its directory.

Step 5 — Run LPIT

python lpit.py --help

«Android limitation: Termux's package database is separate from Android's internal application package database. Access to Android system packages is not implied by Termux support.»

🛠️ Troubleshooting

Problem| Suggested solution
Python not found| Check "python3 --version" and install Python if needed.
Script not found| Verify the current directory and filename.
Package manager unavailable| Confirm the required utility is installed.
Permission denied| Check file permissions and access requirements.
Package information missing| Verify the package and its metadata are available.
Termux behaves differently| Check whether the package belongs to Termux or Android itself.

🔐 Security and Privacy

LPIT is intended to provide lightweight package inspection.

- 🛡️ Prefer read-only package queries.
- 🔑 Avoid unnecessary root privileges.
- 📡 Do not transmit system information without clear user awareness.
- 🧪 Validate external command arguments and handle failures safely.
- 🔍 Review and test the source code before making security claims.

Security and privacy properties must be verified against the implementation rather than assumed from the project description.

🗺️ Project Roadmap

Potential improvements for future releases:

- [ ] 🔎 Improve package-manager detection.
- [ ] 📊 Standardize package metadata output.
- [ ] 🧪 Expand automated testing.
- [ ] 📱 Improve Termux compatibility testing.
- [ ] 🧾 Add optional JSON output.
- [ ] 🛠️ Improve error messages and exit codes.
- [ ] 📚 Expand user documentation.

Roadmap items represent potential future work, not necessarily implemented features.

🤝 Contributing

Contributions that improve LPIT's reliability, portability, documentation, and usability are welcome.

1. 🍴 Fork the repository.
2. 🌿 Create a feature branch.
3. 🛠️ Make your changes.
4. 🧪 Test the changes in the relevant environment.
5. 🚀 Submit a pull request with a clear description.

Please keep contributions readable, maintainable, and compatible with the project's supported Python version.

📄 License

LPIT is intended to use the MIT License.

See ""LICENSE"" (LICENSE) for the applicable terms. Ensure that the file exists and contains the complete MIT License text before publishing the project as MIT-licensed.

🌐 LinuxWays

LinuxWays — Minimal. Fast. Open.

Explore the LinuxWays open-source ecosystem:

- 🐙 GitHub: "github.com/linuxways25" (https://github.com/linuxways25)
- 🐍 Language: "Python" (https://www.python.org/)
- 🐧 Platform: Linux and open-source technologies

LPIT is part of the LinuxWays ecosystem, supporting practical tools for Linux, automation, system administration, and platform engineering.

---

<p align="center">
  <strong>📦 LPIT</strong><br>
  Inspect packages. Understand your system. Work smarter.
</p><p align="center">
  <sub>Built for the command line. Designed for clarity. Inspired by open source.</sub>
</p>