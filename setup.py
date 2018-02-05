from setuptools import setup

setup(
    name='injectable',
    version='0.1.0',
    packages=['tests', 'injectable'],
    url='https://github.com/allrod5/injectable',
    license='MIT',
    author='rodrigo',
    author_email='allrod5@hotmail.com',
    description='Cleanly expose injectable arguments in Python 3 functions',
    test_requires=['testfixtures', 'pytest']
)
