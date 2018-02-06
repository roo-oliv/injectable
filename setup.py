from setuptools import setup

deps = [
    'typing',
    'lazy_object_proxy',
]

setup_deps = deps + [
    'pytest-runner',
]

test_deps = deps + [
    'testfixtures',
    'pytest',
    'pytest-cov',
    'coveralls',
]

extras = {
    'test': test_deps,
}

setup(
    name='injectable',
    version='0.2.0',
    packages=['tests', 'injectable'],
    url='https://github.com/allrod5/injectable',
    license='MIT',
    author='Rodrigo Martins de Oliveira',
    author_email='allrod5@hotmail.com',
    description='Clean dependency injection and lazy initialization support',
    keywords='injection dependency-injection lazy circular-dependency ioc',
    requires=deps,
    setup_requires=setup_deps,
    test_requires=test_deps,
    extras_require=extras,
)
