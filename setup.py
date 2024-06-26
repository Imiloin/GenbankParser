from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="genbankparser",
    version="0.1.0",
    author="Imiloin, Cannizzaro-reaction, xywawawa",
    description="A parser for Genbank files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    test_suite="tests",
    python_requires='>=3.8',
    install_requires=[
        "pytest",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
