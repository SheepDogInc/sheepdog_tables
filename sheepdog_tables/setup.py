from setuptools import setup

import sheepdog_tables

setup(
    name="sheepdog_tables",
    version=sheepdog_tables.__version__,
    author="Alex Hart, Adam Thurlow",
    author_email="alex@sheepdoginc.ca, adam@sheepdog.com",
    description=("Easy to use tables API for Django"),
    license="BSD",
    keywords="tables",
    url="https://github.com/SheepDogInc/sheepdog_tables",
    packages=['sheepdog_tables'],
    long_description="",
    classifiers=[],
)
