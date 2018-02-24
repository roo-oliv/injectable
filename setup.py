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
    version='2.0.0',
    packages=['tests', 'injectable'],
    url='https://github.com/allrod5/injectable',
    license='MIT',
    author='Rodrigo Martins de Oliveira',
    author_email='allrod5@hotmail.com',
    description='Clean dependency injection and lazy initialization support',
    keywords=('injection autowiring autowire autowired dependency-injection'
              ' lazy lazy-initialization circular-dependency'
              ' inversion-of-control ioc'),
    requires=deps,
    install_requires=deps,
    setup_requires=setup_deps,
    test_requires=test_deps,
    extras_require=extras,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
