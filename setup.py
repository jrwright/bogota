from setuptools import setup, find_packages
from os import path
from io import open

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# We maintain the version in a dedicated file
exec(open('bogota/version.py').read())

setup(
    name="bogota",
    version=__version__,
    author="James Wright",
    author_email="james.wright@ualberta.ca",
    description="Implementation of models from behavioural game theory, and support for analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrwright/bogota",
    # packages=find_packages(),
    packages=['bogota', 'bogota.data', 'bogota.data.pools'],
    package_data={
        'bogota':['2x2.agg', '2x2.nfg', 'defaults.cfg'],
        'bogota.data.pools':['*.nfg*', '*.agg']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['gambit',
                      'cma',
                      'numpy'],
    extras_require={
        'distributed': ['celery', 'redis'],
        'mcmc': ['pymc']
    }
)
