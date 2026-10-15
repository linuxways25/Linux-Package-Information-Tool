#!/usr/bin/env python3
"""
LPIT — Linux & Android Package Information Tool
================================================
Read-only package metadata inspector for common Linux distributions and
Android/Termux. Uses only the Python standard library.

Supported backends:
  - Arch Linux and derivatives: pacman
  - Debian/Ubuntu derivatives: dpkg / apt-cache
  - Fedora/RHEL derivatives: rpm / dnf / yum
  - openSUSE/SLES: zypper / rpm
  - Android: pm / dumpsys
  - Termux: dpkg / apt-cache

Requires Python 3.10+. Package queries are read-only; LPIT never installs,
removes, or updates packages.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Sequence


APP_NAME = "LPIT"
APP_VERSION = "3.1.0"
COMMAND_TIMEOUT_SECONDS = 15


class PackageManager(Enum):
    APT = auto()
    DNF = auto()
    YUM = auto()
    ZYPPER = auto()
    PACMAN = auto()
    TERMUX = auto()
    ANDROID_PM = auto()
    UNKNOWN = auto()


@dataclass(frozen=True, slots=True)
class PackageInfo:
    name: str
    version: str = "N/A"
    description: str = "N/A"
    architecture: str = "N/A"
    maintainer: str = "N/A"
    homepage: str = "N/A"
    installed_size: str = "N/A"
    download_size: str = "N/A"
    status: str = "unknown"
    source_pm: str = "unknown"


class ShellExecutor:
    """Run fixed argument-vector commands with a controlled PATH."""

    LINUX_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    TERMUX_PATH = "/data/data/com.termux/files/usr/bin:/system/bin:/system/xbin"
    ANDROID_PATH = "/system/bin:/system/xbin:/vendor/bin"

    @classmethod
    def safe_path(cls) -> str:
        if PlatformDetector.is_termux():
            return cls.TERMUX_PATH
        if PlatformDetector.is_android():
            return cls.ANDROID_PATH
        return cls.LINUX_PATH

    @classmethod
    def run(
        cls,
        command: Sequence[str],
        timeout: int = COMMAND_TIMEOUT_SECONDS,
    ) -> str | None:
        if not command or not command[0] or timeout <= 0:
            return None

        path = cls.safe_path()
        executable = shutil.which(command[0], path=path)
        if executable is None:
            return None

        env = os.environ.copy()
        env["PATH"] = path
        try:
            result = subprocess.run(
                [executable, *command[1:]],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                errors="replace",
                timeout=timeout,
                check=False,
                shell=False,
                env=env,
            )
        except (OSError, subprocess.TimeoutExpired, ValueError):
            return None

        if result.returncode != 0:
            return None
        output = result.stdout.strip()
        return output or None


class PlatformDetector:
    @staticmethod
    def is_termux() -> bool:
        return (
            os.path.isdir("/data/data/com.termux")
            or "TERMUX_VERSION" in os.environ
            or os.path.isfile("/data/data/com.termux/files/usr/bin/pkg")
        )

    @classmethod
    def is_android(cls) -> bool:
        return (
            os.path.exists("/system/build.prop")
            or os.path.exists("/system/bin/pm")
            or "ANDROID_ROOT" in os.environ
            or cls.is_termux()
        )


class DistroDetector:
    @staticmethod
    def _read_os_release() -> dict[str, str]:
        for path in ("/etc/os-release", "/usr/lib/os-release"):
            values: dict[str, str] = {}
            try:
                with open(path, encoding="utf-8") as stream:
                    for line in stream:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        key, value = line.split("=", 1)
                        if key in {"ID", "ID_LIKE", "NAME", "PRETTY_NAME"}:
                            values[key] = value.strip().strip("\"'")
                if values:
                    return values
            except OSError:
                continue
        return {}

    @classmethod
    def detect(cls) -> PackageManager:
        if PlatformDetector.is_termux():
            return PackageManager.TERMUX
        if PlatformDetector.is_android():
            return PackageManager.ANDROID_PM

        release = cls._read_os_release()
        ids = set((release.get("ID", "") + " " + release.get("ID_LIKE", "")).lower().split())

        def available(binary: str) -> bool:
            return shutil.which(binary, path=ShellExecutor.LINUX_PATH) is not None

        # Distribution identity wins over incidental installed utilities.
        if ids & {"arch", "manjaro", "endeavouros", "artix", "garuda"}:
            return PackageManager.PACMAN if available("pacman") else PackageManager.UNKNOWN
        if ids & {"opensuse", "opensuse-leap", "opensuse-tumbleweed", "sles", "sled"} or "suse" in ids:
            if available("zypper"):
                return PackageManager.ZYPPER
            if available("rpm"):
                return PackageManager.DNF  # RPM fallback strategy
            return PackageManager.UNKNOWN
        if ids & {"debian", "ubuntu", "linuxmint", "pop", "elementary", "kali"}:
            return PackageManager.APT if available("dpkg") else PackageManager.UNKNOWN
        if ids & {"fedora", "rhel", "centos", "rocky", "almalinux", "ol"}:
            if available("dnf"):
                return PackageManager.DNF
            if available("yum"):
                return PackageManager.YUM
            return PackageManager.UNKNOWN

        # Conservative fallback for minimal or non-standard installations.
        for pm, binary in (
            (PackageManager.PACMAN, "pacman"),
            (PackageManager.APT, "dpkg"),
            (PackageManager.DNF, "dnf"),
            (PackageManager.YUM, "yum"),
            (PackageManager.ZYPPER, "zypper"),
        ):
            if available(binary):
                return pm
        return PackageManager.UNKNOWN


class PackageQueryStrategy:
    def query(self, package_name: str) -> PackageInfo | None:
        raise NotImplementedError

    @staticmethod
    def make_info(source_pm: str, **values: str) -> PackageInfo:
        allowed = PackageInfo.__dataclass_fields__
        cleaned = {
            key: value
            for key, value in values.items()
            if key in allowed and key != "source_pm"
        }
        return PackageInfo(source_pm=source_pm, **cleaned)


def parse_deb822(raw: str) -> dict[str, str]:
    """Parse the first Debian control paragraph, including continuation lines."""
    fields: dict[str, str] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            if fields:
                break
            continue
        if line.startswith((" ", "\t")) and current_key:
            fields[current_key] += "\n" + line.strip()
        elif ":" in line:
            key, _, value = line.partition(":")
            current_key = key.strip()
            fields[current_key] = value.strip()
        else:
            current_key = None
    return fields


def first_line(value: str | None) -> str:
    if not value:
        return "N/A"
    return value.splitlines()[0].strip() or "N/A"


def query_deb(package_name: str, termux: bool = False) -> PackageInfo | None:
    raw = ShellExecutor.run(["dpkg", "-s", package_name])
    if raw:
        fields = parse_deb822(raw)
        if fields.get("Package"):
            status_field = fields.get("Status", "unknown")
            status = "installed" if status_field.endswith(" installed") else status_field
            size_kb = fields.get("Installed-Size")
            return PackageInfo(
                name=fields.get("Package", package_name),
                version=fields.get("Version", "N/A"),
                description=first_line(fields.get("Description")),
                architecture=fields.get("Architecture", "N/A"),
                maintainer=fields.get("Maintainer", "N/A"),
                homepage=fields.get("Homepage", "N/A"),
                installed_size=f"{size_kb} KB" if size_kb else "N/A",
                status=status,
                source_pm="termux-dpkg" if termux else "dpkg",
            )

    raw = ShellExecutor.run(["apt-cache", "show", package_name])
    if not raw:
        return None
    fields = parse_deb822(raw)
    if not fields.get("Package"):
        return None
    size = fields.get("Size")
    return PackageInfo(
        name=fields.get("Package", package_name),
        version=fields.get("Version", "N/A"),
        description=first_line(fields.get("Description")),
        architecture=fields.get("Architecture", "N/A"),
        maintainer=fields.get("Maintainer", "N/A"),
        homepage=fields.get("Homepage", "N/A"),
        installed_size="N/A",
        download_size=f"{size} bytes" if size else "N/A",
        status="available (not confirmed installed)",
        source_pm="termux-apt-cache" if termux else "apt-cache",
    )


class AptStrategy(PackageQueryStrategy):
    def query(self, package_name: str) -> PackageInfo | None:
        return query_deb(package_name)


class TermuxStrategy(PackageQueryStrategy):
    def query(self, package_name: str) -> PackageInfo | None:
        return query_deb(package_name, termux=True)


class PacmanStrategy(PackageQueryStrategy):
    def query(self, package_name: str) -> PackageInfo | None:
        raw = ShellExecutor.run(["pacman", "-Qi", package_name])
        source = "pacman-local"
        status = "installed"
        if not raw:
            raw = ShellExecutor.run(["pacman", "-Si", package_name])
            source = "pacman-sync"
            status = "available (not installed)"
        if not raw:
            return None

        fields: dict[str, str] = {}
        for line in raw.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                fields[key.strip()] = value.strip()
        if not fields.get("Name"):
            return None
        installed_size = fields.get("Installed Size", "N/A")
        download_size = fields.get("Download Size", "N/A")
        return PackageInfo(
            name=fields.get("Name", package_name),
            version=fields.get("Version", "N/A"),
            description=fields.get("Description", "N/A"),
            architecture=fields.get("Architecture", "N/A"),
            maintainer=fields.get("Packager", "N/A"),
            homepage=fields.get("URL", "N/A"),
            installed_size=installed_size,
            download_size=download_size,
            status=status,
            source_pm=source,
        )


class RpmStrategy(PackageQueryStrategy):
    def query(self, package_name: str) -> PackageInfo | None:
        # Installed RPM database is the most dependable source for installed data.
        query_format = r"%{NAME}\n%{VERSION}-%{RELEASE}\n%{SUMMARY}\n%{ARCH}\n%{PACKAGER}\n%{URL}\n%{SIZE}\n%{INSTALLTIME}"
        raw = ShellExecutor.run(["rpm", "-q", "--queryformat", query_format, package_name])
        if raw and not raw.startswith("package ") and not raw.startswith("error:"):
            values = raw.splitlines()
            if len(values) >= 8:
                try:
                    size_bytes = int(values[6])
                    installed_size = f"{size_bytes:,} bytes"
                except ValueError:
                    installed_size = "N/A"
                return PackageInfo(
                    name=values[0],
                    version=values[1],
                    description=values[2] or "N/A",
                    architecture=values[3] or "N/A",
                    maintainer=values[4] or "N/A",
                    homepage=values[5] or "N/A",
                    installed_size=installed_size,
                    status="installed",
                    source_pm="rpm",
                )

        # Repository metadata fallback.
        for command in (["dnf", "info", "--available", package_name],
                        ["yum", "info", package_name]):
            raw = ShellExecutor.run(command)
            if not raw:
                continue
            fields = self._parse_info(raw)
            if fields.get("Name") or fields.get("Available Packages"):
                name = fields.get("Name", package_name)
                return PackageInfo(
                    name=name,
                    version=fields.get("Version", "N/A"),
                    description=fields.get("Summary", "N/A"),
                    architecture=fields.get("Architecture", "N/A"),
                    maintainer=fields.get("Packager", fields.get("Vendor", "N/A")),
                    homepage=fields.get("URL", "N/A"),
                    installed_size="N/A",
                    download_size=fields.get("Size", "N/A"),
                    status="available (not confirmed installed)",
                    source_pm=command[0],
                )
        return None

    @staticmethod
    def _parse_info(raw: str) -> dict[str, str]:
        fields: dict[str, str] = {}
        for line in raw.splitlines():
            if line and not line[0].isspace() and ":" in line:
                key, _, value = line.partition(":")
                fields[key.strip()] = value.strip()
        return fields


class ZypperStrategy(PackageQueryStrategy):
    def query(self, package_name: str) -> PackageInfo | None:
        # Installed RPM query avoids depending on localized zypper output.
        rpm_info = RpmStrategy().query(package_name)
        if rpm_info and rpm_info.status == "installed":
            return PackageInfo(
                name=rpm_info.name,
                version=rpm_info.version,
                description=rpm_info.description,
                architecture=rpm_info.architecture,
                maintainer=rpm_info.maintainer,
                homepage=rpm_info.homepage,
                installed_size=rpm_info.installed_size,
                download_size=rpm_info.download_size,
                status=rpm_info.status,
                source_pm="rpm (openSUSE/SLES)",
            )

        raw = ShellExecutor.run(["zypper", "--non-interactive", "info", package_name])
        if not raw:
            return None
        fields: dict[str, str] = {}
        for line in raw.splitlines():
            match = re.match(r"^\s*([^:\n]+?)\s*:\s*(.*?)\s*$", line)
            if match:
                fields[match.group(1).strip()] = match.group(2).strip()
        name = fields.get("Name")
        if not name:
            return None
        return PackageInfo(
            name=name,
            version=fields.get("Version", "N/A"),
            description=fields.get("Summary", "N/A"),
            architecture=fields.get("Arch", "N/A"),
            maintainer=fields.get("Vendor", "N/A"),
            homepage=fields.get("URL", fields.get("Homepage", "N/A")),
            installed_size=fields.get("Installed Size", "N/A"),
            download_size=fields.get("Download Size", "N/A"),
            status=fields.get("Status", "available (status unconfirmed)"),
            source_pm="zypper",
        )


class AndroidPmStrategy(PackageQueryStrategy):
    def query(self, package_name: str) -> PackageInfo | None:
        # Exact-match after asking pm to filter; don't trust filtering alone.
        raw = ShellExecutor.run(["pm", "list", "packages", "-f", package_name])
        if not raw:
            return None

        apk_path: str | None = None
        for line in raw.splitlines():
            if not line.startswith("package:") or "=" not in line:
                continue
            path, name = line[len("package:"):].rsplit("=", 1)
            if name.strip() == package_name:
                apk_path = path.strip()
                break
        if not apk_path:
            return None

        details = ShellExecutor.run(["dumpsys", "package", package_name]) or ""
        version_match = re.search(r"\bversionName=([^\s]+)", details)
        version = version_match.group(1) if version_match else "N/A"
        try:
            size_bytes = os.path.getsize(apk_path)
            installed_size = (
                f"{size_bytes / (1024 * 1024):.1f} MB"
                if size_bytes >= 1024 * 1024
                else f"{size_bytes / 1024:.1f} KB"
            )
        except OSError:
            installed_size = "N/A"

        return PackageInfo(
            name=package_name,
            version=version,
            description="Android application package",
            architecture="N/A (APK ABI not inspected)",
            installed_size=installed_size,
            status="installed",
            source_pm="android-pm",
        )


STRATEGIES: dict[PackageManager, type[PackageQueryStrategy]] = {
    PackageManager.APT: AptStrategy,
    PackageManager.DNF: RpmStrategy,
    PackageManager.YUM: RpmStrategy,
    PackageManager.ZYPPER: ZypperStrategy,
    PackageManager.PACMAN: PacmanStrategy,
    PackageManager.TERMUX: TermuxStrategy,
    PackageManager.ANDROID_PM: AndroidPmStrategy,
}


class TerminalRenderer:
    RESET = "\033[0m"
    HEADER = "\033[1;36m"
    LABEL = "\033[0;90m"
    VALUE = "\033[0;37m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[0;33m"
    RED = "\033[1;31m"

    @classmethod
    def _color(cls, text: str, color: str, enabled: bool) -> str:
        return f"{color}{text}{cls.RESET}" if enabled else text

    @classmethod
    def render_package(cls, info: PackageInfo, color: bool = True) -> None:
        width = max(40, min(shutil.get_terminal_size(fallback=(80, 24)).columns, 82))
        title = f" {APP_NAME} · PACKAGE INFORMATION "
        divider = "─" * width
        print()
        print(cls._color(title.center(width), cls.HEADER, color))
        print(cls._color(divider, cls.LABEL, color))

        rows = [
            ("Name", info.name, cls.VALUE),
            ("Version", info.version, cls.GREEN),
            ("Status", info.status, cls.GREEN if info.status == "installed" else cls.YELLOW),
            ("Architecture", info.architecture, cls.VALUE),
            ("Installed size", info.installed_size, cls.VALUE),
            ("Download size", info.download_size, cls.VALUE),
            ("Maintainer / vendor", info.maintainer, cls.VALUE),
            ("Homepage", info.homepage, cls.VALUE),
            ("Description", info.description, cls.VALUE),
            ("Source", info.source_pm, cls.YELLOW),
        ]
        label_width = max(len(label) for label, _, _ in rows)
        for label, value, row_color in rows:
            safe_value = value.replace("\x1b", "")
            print(
                f"  {cls._color(label.rjust(label_width) + ':', cls.LABEL, color)}  "
                f"{cls._color(safe_value, row_color, color)}"
            )
        print(cls._color(divider, cls.LABEL, color))
        print()

    @classmethod
    def error(cls, message: str, color: bool = True) -> None:
        print(cls._color(f"Error: {message}", cls.RED, color), file=sys.stderr)

    @classmethod
    def info(cls, message: str, color: bool = True) -> None:
        print(cls._color(message, cls.YELLOW, color), file=sys.stderr)


class LPITApplication:
    SUPPORTED = "Arch, Debian, Ubuntu, Fedora, RHEL, SUSE, Android and Termux"

    @staticmethod
    def valid_package_name(name: str, pm: PackageManager) -> bool:
        if not name or len(name) > 255 or name.startswith("-"):
            return False
        if pm == PackageManager.ANDROID_PM:
            return re.fullmatch(
                r"[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)+", name
            ) is not None
        return re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9+._:@-]*", name) is not None

    def run(self, argv: Sequence[str] | None = None) -> int:
        parser = argparse.ArgumentParser(
            prog="lpit",
            description=(
                f"{APP_NAME} {APP_VERSION} — inspect package metadata on Linux and Android.\n"
                "Read-only: this tool does not install, remove, or update packages."
            ),
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=(
                "Examples:\n"
                "  lpit bash\n"
                "  lpit curl python3 nginx\n"
                "  lpit com.termux (Termux package)\n"
                "  lpit com.example.app (Android application)\n"
            ),
        )
        parser.add_argument("packages", nargs="+", metavar="PACKAGE",
                            help="one or more package names or Android package IDs")
        parser.add_argument("--version", action="version",
                            version=f"%(prog)s {APP_VERSION}")
        parser.add_argument("--no-color", action="store_true",
                            help="disable coloured terminal output")
        parsed = parser.parse_args(argv)
        color = not parsed.no_color and sys.stdout.isatty() and "NO_COLOR" not in os.environ

        pm = DistroDetector.detect()
        if pm == PackageManager.UNKNOWN:
            TerminalRenderer.error(
                "No supported package manager detected. "
                f"Supported platforms: {self.SUPPORTED}.",
                color=False,
            )
            return 2

        strategy_type = STRATEGIES.get(pm)
        if strategy_type is None:
            TerminalRenderer.error("This platform is not supported.", color=False)
            return 2

        strategy = strategy_type()
        exit_code = 0
        for package in parsed.packages:
            if not self.valid_package_name(package, pm):
                TerminalRenderer.error(f"Invalid package name: {package!r}", color=color)
                exit_code = 1
                continue

            try:
                info = strategy.query(package)
            except Exception as exc:
                # Keep multi-package runs alive; avoid dumping tracebacks to end users.
                TerminalRenderer.error(
                    f"Could not inspect {package!r}: {type(exc).__name__}. "
                    "Run again with a reproducible case and report the details.",
                    color=color,
                )
                exit_code = 1
                continue

            if info is None:
                TerminalRenderer.error(
                    f"Package {package!r} was not found or its metadata is unavailable.",
                    color=color,
                )
                exit_code = 1
                continue

            TerminalRenderer.render_package(info, color=color)

        return exit_code


def main() -> None:
    try:
        raise SystemExit(LPITApplication().run())
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        raise SystemExit(130)


if __name__ == "__main__":
    main()
