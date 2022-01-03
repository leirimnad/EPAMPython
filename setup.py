from setuptools import setup, find_packages

setup(
    name='department_app',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'importlib; python_version == "2.6"',
    ],
)