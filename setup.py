from setuptools import setup, find_packages

import sheepdog_tables


setup(
    name="sheepdog-tables",
    version=sheepdog_tables.__version__,
    author="Alex Hart, Adam Thurlow, Karl Leuschen",
    author_email="exallium@gmail.com, adam@sheepdog.com, karl@sheepdog.com",
    description=("Easy to use tables API for Django"),
    license = "BSD",
    keywords = "tables",
    url = "https://github.com/SheepDogInc/sheepdog_tables",
    packages=find_packages(),
    long_description="",
    include_package_data=True,
    classifiers=
    [
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
