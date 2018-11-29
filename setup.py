from setuptools import setup, find_packages
from codecs import open
from os import path

import bids_neuropoly as bn

here = path.abspath(path.dirname(__file__))

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('test-requirements.txt') as f:
    test_requirements = f.read().splitlines()

setup(
    name='bids_neuropoly',
    version=bn.__version__,
    description='An open-source BIDS parser.',
    url='https://github.com/neuropoly/bids_neuropoly',
    author='Christian S. Perone',
    author_email='christian.perone@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=requirements,
    tests_require=test_requirements,
    #entry_points={
        #'console_scripts': [
        #    'cmdname=bn.mod:function',
        #],
    #},
)