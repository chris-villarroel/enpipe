from setuptools import setup, find_packages

setup(
    name="epipe",
    version="0.4",
    packages=find_packages(),
    author="Christian Villarroel",
    author_email="villarroel.cvd@gmail.com",
    description="A utility package for ...",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "PyYAML"
        # Add other dependencies as needed
    ],
)

