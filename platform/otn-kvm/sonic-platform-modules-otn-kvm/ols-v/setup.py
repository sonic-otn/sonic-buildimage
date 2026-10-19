from setuptools import setup

setup(
    name='sonic_platform',
    version='1.0',
    description='SONiC platform API implementation on OTN-KVM Platforms',
    license='Apache 2.0',
    author='Molex',
    author_email='lu.mao@molex.com',
    url='https://github.com/Azure/sonic-buildimage',
    maintainer='Molex',
    maintainer_email='lu.mao@molex.com',
    packages=['sonic_platform'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    keywords='sonic SONiC OTN platform PLATFORM',
)

