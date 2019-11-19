from setuptools import setup, find_packages

from twiddler_config import __version__ as version_string


setup(
    name='twiddler-config',
    version=version_string,
    url='https://github.com/coddingtonbear/twiddler-config',
    description=(
        'Parse a Twiddler configuration file'
    ),
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'twiddler-config = twiddler_config.cmdline:main'
        ],
    },
)
