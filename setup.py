from setuptools import setup, find_packages

setup(
    name='Simple-PyDI',
    version="0.9.0",
    description='simple di framework like java spring-framework',
    long_description=open('README.md', encoding="utf8").read(),
    long_description_content_type='text/markdown',
    author='Carl.Zhang',
    author_email='tasse_00@163.com',
    maintainer='Carl.Zhang',
    maintainer_email='tasse_00@163.com',
    license='BSD License',
    packages=find_packages(include=("di*",)),
    install_requires=[],
    platforms=["all"],
    url='https://github.com/Tasse00/pydi',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
