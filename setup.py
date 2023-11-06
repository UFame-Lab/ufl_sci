from setuptools import setup, find_packages


setup(
    name="sci",
    version="1.0.0",
    packages=find_packages(
        include=("sci*",),
    ),
    install_requires=[
        "websockets",
        "redis",
    ]
)