import setuptools
from os.path import join, dirname

version = "0.1.4"

with open(join(dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as fin:
    requirements = fin.read().splitlines()

setuptools.setup(
    name='tinkoff_voicekit_client',
    version=version,
    license="Apache License Version 2.0",
    author="Tinkoff Speech Team",
    python_requires=">=3.6",
    description='Python Tinkoff Speech API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
)
