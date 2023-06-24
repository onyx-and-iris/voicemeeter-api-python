import subprocess
from pathlib import Path


def ex_dsl():
    path = Path.cwd() / "examples" / "dsl" / "."
    subprocess.run(["py", str(path)])


def ex_events():
    path = Path.cwd() / "examples" / "events" / "."
    subprocess.run(["py", str(path)])


def ex_gui():
    path = Path.cwd() / "examples" / "gui" / "."
    subprocess.run(["py", str(path)])


def ex_levels():
    path = Path.cwd() / "examples" / "levels" / "."
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


def test():
    subprocess.run(["tox"])
