import re

from setuptools import find_packages, setup

with open("requirements.txt", encoding="utf-8") as rf:
    reqs = rf.readlines()
    out_reqs = [x.strip() for x in reqs if re.search(r'^\w.*', x)]

setup(
    name="cains_jawbone",
    version="0.1.0",
    description="An API to handle research about the Cain's Jawbone puzzle",
    author="Ann",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=out_reqs,
)
