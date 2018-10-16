from setuptools import setup, find_packages
from os import path
from io import open

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# We maintain the version in a dedicated file
execfile('bogota/version.py')

setup(
    name="bogota",
    version=__version__,
    author="James Wright",
    author_email="james.wright@ualberta.ca",
    description="Keras implementation of GameNet and QCH with level0 features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrwright/bogota",
    # packages=find_packages(),
    packages=['bogota', 'bogota.data', 'bogota.data.pools'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy',
                      'gambit']
)
