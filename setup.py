from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='JuniperAutomation',
    version='1.0',
    description='JUNOS scripts used in POC',
    long_description=readme,
    author='Karthikeyan Krish',
    url='https://github.com/indhradhanush/JuniperAutomation',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

