#!/usr/bin/env python3

from setuptools import setup
import yaml

def readme():
    return ''

with open('setup.yml', 'r') as f:
    cfg = yaml.load(f)
    setup(**cfg)

