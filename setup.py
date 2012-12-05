from setuptools import setup, find_packages

PACKAGE_NAME = "reviewbotjslint"
VERSION = "0.1"


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=("A Review Bot tool that runs JSLint, "
                 "the code quality tool for JavaScript"),
    author="Allyshia Sewdat",
    author_email="allyshias@gmail.com",
    packages=find_packages(),
    package_data={
        'reviewbotjslint': ['lib/*.js',]
    },
    entry_points={
        'reviewbot.tools': [
            'jslint = reviewbotjslint.jslint:JSLintTool',
        ],
    },
    install_requires=[
        'reviewbot',
    ], )
