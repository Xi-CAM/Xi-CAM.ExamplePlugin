from setuptools import setup, find_namespace_packages
from codecs import open
from os import path

__version__ = '0.1.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xicam.QuickStartPlugin',
    version=__version__,
    description='',
    long_description=long_description,
    url='',
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='Xi-cam',
    packages=find_namespace_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Ian Humphrey',
    author_email='ihumphrey@lbl.gov',
    entry_points={
        'xicam.plugins.GUIPlugin':
            ['quickstart_plugin = xicam.quickstart_plugin:QuickStartPlugin']
    }
)
