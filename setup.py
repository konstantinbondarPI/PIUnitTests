from setuptools import setup, find_packages

setup(
    name="PIUnitTestsRunner",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'piunittestsrunner = PIUnitTests.main:main',  # Entry point
        ],
    },
)