from setuptools import setup

setup(
    name='easyasyncio',
    version='6.3.0-alpha',
    packages=['easyasyncio'],
    url='https://github.com/RaphaelNanje/easyasyncio.git',
    license='MIT',
    author='Raphael Nanje',
    author_email='rtnanje@gmail.com',
    description='A library that makes asyncio simple',
    install_requires=[
        'logzero',
        'aiohttp',
        'requests',
        'easyfilemanager @ git+ssh://git@github.com/RaphaelNanje/easyfilemanager.git#egg=easyfilemanager',
        'asciimatics'
    ],
    python_requies='~=3.6'
)
