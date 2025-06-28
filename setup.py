from setuptools import setup, find_packages

setup(
    name='my_python_package',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple Python package that prints Hello World to the log.',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)