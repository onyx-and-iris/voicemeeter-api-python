import subprocess
from pathlib import Path


def ex_dsl():
    path = Path.cwd() / "examples" / "dsl" / "."
    subprocess.run(["py", str(path)])


def ex_midi():
    path = Path.cwd() / "examples" / "midi" / "."
    subprocess.run(["py", str(path)])


def ex_obs():
    path = Path.cwd() / "examples" / "obs" / "."
    subprocess.run(["py", str(path)])


def ex_observer():
    path = Path.cwd() / "examples" / "observer" / "."
    subprocess.run(["py", str(path)])
