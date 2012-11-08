from setuptools import setup, find_packages
import os

data_files = []
for dirpath, dirnames, filenames in os.walk("sheepdog_tables"):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.') or dirname == '__pycache__':
            del dirnames[i]
    if '__init__.py' not in filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name = "sheepdog_tables",
    version = "0.5",
    author = "Alex Hart, Adam Thurlow",
    author_email = "alex@sheepdoginc.ca, adam@sheepdoginc.ca",
    description = ("Easy to use tables API for Django"),
    license = "BSD",
    keywords = "tables",
    url = "https://github.com/SheepDogInc/sheepdog_tables",
    packages=find_packages(),
    include_package_data=True,
    data_files=data_files,
    long_description="",
    classifiers=
        [
            "Environment :: Web Environment",
            "Framework :: Django",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: CoffeeScript",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ]
)
