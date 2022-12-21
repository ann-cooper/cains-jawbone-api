import re

from setuptools import find_packages, setup

desc_pattern = re.compile(r"description$(\r|\n){0,2}(.*)(\r|\n){0,2}", re.MULTILINE)

with open("README.md", encoding="utf-8") as f:
    desc = f.read()
    out_desc = re.search(desc_pattern, desc).group(2)

with open("requirements.txt", encoding="utf-8") as rf:
    reqs = rf.read()
    out_reqs = [
        line.split('#')[0].strip() for line in re.split(r'[\n\r]+', reqs) if line
    ]

setup(
    name="cains_jawbone",
    version="0.1.0",
    description="An API to store research abount the Cain's Jawbone puzzle",
    long_description=out_desc,
    author="Ann",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=out_reqs,
)
