import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='blossompy',
    version='0.1',
    ##packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Used to run and create basic commands for Human-Robot Interaction with the Blossom Robot',
    long_description=open('README.txt').read(),
    install_requires=['numpy'],
    url='https://github.com/riya-ranjan/blossom-public',
    author='Riya Ranjan',
    author_email='riya.ranjan.00@gmail.com'
)
