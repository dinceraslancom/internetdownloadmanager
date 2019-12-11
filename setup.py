from setuptools import setup, find_packages


requires = [
    'chardet>=3.0.2,<3.1.0',
    'idna>=2.5,<2.9',
    'urllib3>=1.21.1,<1.26,!=1.25.0,!=1.25.1',
    'certifi>=2017.4.17',
    'requests>=2.22.0',
]

with open("README.rst", "r", encoding="utf8") as f:
    readme = f.read()
with open("HISTORY.rst", "r", encoding="utf8") as f:
    history = f.read()


setup(
    name='internetdownloadmanager',
    version='0.0.1',
    package_dir={'internetdownloadmanager': 'internetdownloadmanager'},
    author="Dincer Aslan",
    author_email="dinceraslan.com@gmail.com",
    description="file downloader with many requests",
    long_description=readme,
    url="https://github.com/dinceraslancom/internetdownloadmanager",
    packages=find_packages(),
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=requires,
    classifiers=[
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    project_urls={
        'Source': 'https://github.com/dinceraslancom/internetdownloadmanager',
    },
)
