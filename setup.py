from setuptools import setup

base_packages = ["requests"]

dev_packages = [
    "black>=19.3b0",
    "flake8>=3.6.0",
    "flake8-annotations==2.1.0",
    "flake8-bandit==2.1.2",
    "flake8-bugbear==20.1.4",
    "flake8-docstrings==1.5.0",
    "darglint==1.4.0",
    "pre-commit>=2.2.0",
    "dataclasses>=0.7,<1; python_version<'3.7'",
    "dataclasses-json>=0.5.0,<1.0.0",
    "types-dataclasses>=0.1.3,<1; python_version<'3.7'",
    "types-requests>=0.1.8,<1",
]

setup(
    name="doccano-client",
    # Semver for this package should match Doccano release tags to denote compatibility
    # up to the minor version (patch version can be more flexible)
    version="1.5.1",  # Tested for compatibility against Doccano >=1.5.0, <=1.5.5
    setup_requires=["setuptools_scm"],
    description="A simple client wrapper for the doccano API.",
    long_description="This simple API wrapper allows users to easily get data \
            from and send data to a doccano instance.",
    keywords="doccano api client wrapper",
    url="https://github.com/doccano/doccano_api_client",
    author="Andrew Parsons",
    author_email="parsonsandrew1@gmail.com",
    license="MIT",
    packages=["doccano_api_client"],
    install_requires=base_packages,
    extras_require={"dev": dev_packages},
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
