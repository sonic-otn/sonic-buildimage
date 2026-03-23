from setuptools import setup

setup(
    name='sonic-pm',
    version='1.0',
    description='OTN PM daemon for SONiC',
    license='Apache 2.0',
    author='Koshy Mathew',
    author_email='koshy.mathew@molex.com',
    url='https://github.com/sonic-net/sonic-buildimage',
    scripts=[
        'scripts/sonic-pm',
    ],
    setup_requires=[
        'pytest-runner',
        'wheel',
    ],
    install_requires=[
        'sonic-py-common',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Networking',
    ],
    keywords='sonic SONiC OTN PM pmon',
)
