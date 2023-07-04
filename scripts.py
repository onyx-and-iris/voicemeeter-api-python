import subprocess
import sys
from pathlib import Path


def ex_dsl():
    scriptpath = Path.cwd() / "examples" / "dsl" / "."
    subprocess.run([sys.executable, str(scriptpath)])


def ex_events():
    scriptpath = Path.cwd() / "examples" / "events" / "."
    subprocess.run([sys.executable, str(scriptpath)])


def ex_gui():
    scriptpath = Path.cwd() / "examples" / "gui" / "."
    subprocess.run([sys.executable, str(scriptpath)])


def ex_levels():
    scriptpath = Path.cwd() / "examples" / "levels" / "."
    subprocess.run([sys.executable, str(scriptpath)])


def ex_midi():
    scriptpath = Path.cwd() / "examples" / "midi" / "."
    subprocess.run([sys.executable, str(scriptpath)])


def ex_obs():
    scriptpath = Path.cwd() / "examples" / "obs" / "."
    subprocess.run([sys.executable, str(scriptpath)])


def ex_observer():
    scriptpath = Path.cwd() / "examples" / "observer" / "."
    subprocess.run([sys.executable, str(scriptpath)])


def test():
    subprocess.run(["tox"])
