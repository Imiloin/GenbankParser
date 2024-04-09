from setuptools import setup, find_packages

setup(
    name="genbankparser",
    version="0.1.0",
    author="Imiloin, Cannizzaro-reaction, xywawawa",
    description="A parser for Genbank files.",
    packages=find_packages(),
    test_suite="tests",
    install_requires=[
        "pytest",
    ],
)
