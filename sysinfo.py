import platform
from os import environ, name
from typing import TypeVar

import psutil
from tqdm import tqdm
from colorama import init
from termcolor import colored, COLORS
from keyboard import is_pressed

init(True)

CENSORED = "[CENSORED]"
T = TypeVar("T")


def is_secret(thing: str) -> bool:
    """Is it a secret?"""
    if thing == "MUSTCENSORE":
        return True
    try:
        secrets = [
            x.lower().rstrip() for x in environ["secrets"].split(":")
        ]
        return thing.lower().rstrip() in secrets
    except KeyError:
        return False


def censore_if_needed(thing: str, value: T) -> T:
    """Censore if needed."""
    if is_secret(thing):
        if isinstance(value, str):
            return CENSORED
        if isinstance(value, tuple):
            return tuple(CENSORED for _ in range(len(value)))
        raise TypeError(f'Can\'t censore "{thing}"')
    return value


def main(argv=None):
    things = {
        "architecture": censore_if_needed(
            "architecture", platform.architecture()
        ),
        "machine": censore_if_needed("machine", platform.machine()),
        "node": censore_if_needed("node", platform.node()),
        "platform": censore_if_needed(
            "platform", platform.platform()
        ),
        "processor": censore_if_needed(
            "processor", platform.processor()
        ),
        "python_build": censore_if_needed(
            "python_build", platform.python_build()
        ),
        "python_compiler": censore_if_needed(
            "python_compiler", platform.python_compiler()
        ),
        "python_branch": censore_if_needed(
            "python_branch", platform.python_branch()
        ),
        "python_implementation": censore_if_needed(
            "python_implementation", platform.python_implementation()
        ),
        "python_revision": censore_if_needed(
            "python_revision", platform.python_revision()
        ),
        "python_version": censore_if_needed(
            "python_version", platform.python_version()
        ),
        "system_alias": censore_if_needed(
            "system_alias",
            platform.system_alias(
                platform.system(),
                platform.release(),
                platform.version(),
            ),
        ),
        # *** SYSTEM PECIFIC ***
        #       Windows
        "win32_ver": (),
        "win32_edition": "",
        "win32_is_iot": "",
        #         Mac
        "mac_ver": (),
        #        Unix
        "libc_ver": (),
    }

    if platform.system().lower().rstrip() == "windows":
        things["win32_ver"] = censore_if_needed(
            "win32_ver", platform.win32_ver()
        )
        things["win32_edition"] = censore_if_needed(
            "win32_edition", platform.win32_edition()
        )
        things["win32_is_iot"] = censore_if_needed(
            "win32_is_iot", platform.win32_is_iot()
        )

    if platform.system().lower().rstrip().find("mac") != -1:
        things["mac_ver"] = censore_if_needed(
            "mac_ver", platform.mac_ver()
        )

    if platform.system().lower().rstrip().find("unix") != -1:
        things["libc_ver"] = censore_if_needed(
            "libc_ver", platform.libc_ver()
        )

    print(f"OS                   : {name}")

    if things["architecture"]:
        print(
            f"Architecture         : {things['architecture'][1]}"
            f" {things['architecture'][0]}"
        )

    if things["system_alias"]:
        print(
            f"System alias         : {' '.join(things['system_alias'])}"
        )

    if things["win32_ver"]:
        print(
            f"Windows version      : {' '.join(things['win32_ver'])}"
        )

    if things["win32_edition"]:
        print(f"Windows edition      : {things['win32_edition']}")

    if things["win32_is_iot"] not in ("", " ", None):
        print(f"Windows IoT edition  : {things['win32_is_iot']}")

    if things["mac_ver"]:
        print(f"Mac version          : {' '.join(things['mac_ver'])}")

    _libc = (
        " ".join(things["libc_ver"])
        if things["libc_ver"] != ()
        else "N/A"
    )
    print(f"Libc version         : {_libc}")

    print("")

    if things["machine"]:
        print(f"Machine              : {things['machine']}")

    if things["node"]:
        print(f"Node                 : {things['node']}")

    if things["platform"]:
        print(f"Platform             : {things['platform']}")

    if things["processor"]:
        print(f"Processor            : {things['processor']}")

    print("")

    if things["python_build"]:
        print(
            f"Python               : {things['python_build'][0]}"
            f" ({things['python_build'][1]})"
        )

    if things["python_compiler"]:
        print(f"Python compiler      : {things['python_compiler']}")

    if things["python_branch"]:
        print(f"Python branch        : {things['python_branch']}")

    if things["python_implementation"]:
        print(
            f"Python implementation: {things['python_implementation']}"
        )

    if things["python_revision"]:
        print(f"Python revision      : {things['python_revision']}")

    if things["python_version"]:
        print(f"Python version       : {things['python_version']}")

    print("")

    colors = [colored(x, x) for x in COLORS]

    print("; ".join(colors))

    print("\n")
    cpu = tqdm(
        desc="CPU",
        total=100,
        bar_format="{desc}: {percentage:3.0f}% |{bar}|",
        ncols=60,
    )
    ram = tqdm(
        desc="RAM",
        total=psutil.virtual_memory()[0],
        bar_format="{desc}: {percentage:3.0f}% {n} bytes |{bar}|",
        ncols=60,
    )
    while True:
        cpu.n = psutil.cpu_percent(0.5)
        cpu.refresh()
        ram.n = psutil.virtual_memory()[3]
        ram.refresh()
        if is_pressed("q"):
            raise SystemExit


if __name__ == "__main__":
    main()
