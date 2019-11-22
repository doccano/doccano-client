from setuptools import setup

setup(
    name='doccano_api_client',
    version='0.1',
    description='A simple API wrapper for the doccano API.',
    long_description='This simple API wrapper allows users to easily get data from and send data to a doccano instance.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Processing :: Linguistic'
    ],
    keywords='doccano api client wrapper',
    url='http://github.com/afparsons/doccano_api_client',
    author='Andrew Parsons',
    author_email='parsonsandrew1@gmail.com',
    license='MIT',
    packages=['src'],
    install_requires=[
        'requests'
    ],
    zip_safe=False
)