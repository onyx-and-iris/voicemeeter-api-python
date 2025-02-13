import os
import subprocess
import sys
from pathlib import Path


def ex_dsl():
    subprocess.run(['tox', 'r', '-e', 'dsl'])


def ex_callbacks():
    scriptpath = Path.cwd() / 'examples' / 'callbacks' / '.'
    subprocess.run([sys.executable, str(scriptpath)])


def ex_gui():
    scriptpath = Path.cwd() / 'examples' / 'gui' / '.'
    subprocess.run([sys.executable, str(scriptpath)])


def ex_levels():
    scriptpath = Path.cwd() / 'examples' / 'levels' / '.'
    subprocess.run([sys.executable, str(scriptpath)])


def ex_midi():
    scriptpath = Path.cwd() / 'examples' / 'midi' / '.'
    subprocess.run([sys.executable, str(scriptpath)])


def ex_obs():
    subprocess.run(['tox', 'r', '-e', 'obs'])


def ex_observer():
    scriptpath = Path.cwd() / 'examples' / 'observer' / '.'
    subprocess.run([sys.executable, str(scriptpath)])


def test_basic():
    subprocess.run(['tox'], env=os.environ.copy() | {'KIND': 'basic'})


def test_banana():
    subprocess.run(['tox'], env=os.environ.copy() | {'KIND': 'banana'})


def test_potato():
    subprocess.run(['tox'], env=os.environ.copy() | {'KIND': 'potato'})


def test_all():
    steps = [test_basic, test_banana, test_potato]
    for step in steps:
        step()
