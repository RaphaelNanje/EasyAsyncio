from setuptools import setup

setup(
        name='easyasyncio',
        version='10.0.0',
        packages=['easyasyncio'],
        url='https://github.com/RaphaelNanje/easyasyncio.git',
        license='MIT',
        author='Raphael Nanje',
        author_email='rtnanje@gmail.com',
        description='A library that makes asyncio simple',
        install_requires=[
                'aiohttp==3.6.2',
                'asciimatics',
                'diskcache',
                'easyfilemanager @ https://github.com'
                '/RaphaelNanje/easyfilemanager/archive/v3.0.1.tar.gz'

        ],
        python_requires='~=3.6'
)
