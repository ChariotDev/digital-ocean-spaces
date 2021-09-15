import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_reqs = parse_requirements('requirements.txt')
reqs = install_reqs

setup(
    name='digital_ocean_spaces',
    version='0.1.0',
    author="Jody Doolittle <https://chariot-dev.com>",
    license="MIT",
    url="https://github.com/ChariotDev/digital-ocean-spaces",
    description = 'An MIT licensed python client for Digital Ocean Spaces with a built in shell.',
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['digital_ocean_spaces'],
    package_dir={'digital_ocean_spaces': ''},
    package_data={'digital_ocean_spaces': [
        '*.py',
        'README.md',
        'LICENSE',
        '*.template',
        'utils/*.py'
        ]},
    install_requires=reqs,
)
