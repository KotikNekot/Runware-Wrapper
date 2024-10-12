from setuptools import setup, find_packages

setup(
    name='pyrunware',
    version='0.1.0',
    packages=find_packages,
    install_requires=["aiohttp", "pydantic"],
    author='whynotvoid',
    description='api wrapper for runware https://docs.runware.ai/en/getting-started/introduction',
    url='https://github.com/KotikNekot/Runware-Wrapper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
