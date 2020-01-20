import setuptools
from os.path import join, dirname
from os import listdir

version = "0.1.2"

with open(join(dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as fin:
    requirements = fin.read().splitlines()

path_to_dlls = "./tinkoff_voicekit_client/TTS/opuslibwin"
opus_dll = [f"{path_to_dlls}/{opus}" for opus in listdir(path_to_dlls)]

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
    data_files=[('opuslibwin', opus_dll)],
    install_requires=requirements,
)
