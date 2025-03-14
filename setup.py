from setuptools import setup, find_packages

""" Sets up the whole project.
Allows all classes to talk to each other (even if they are further up in the hierarchy).
This prevents us from having to maticulously run an system appendature line in every project file.
However, this does mean that no class can be protected from external manipulation.

Regardless, this fix is much better.
"""
setup(
    name='MystiWord',
    version='0.1',
    packages=find_packages(),
    author='Rishi Sahasrabuddhe',
    url='https://github.com/RishiS-HSCProjects/11AT1-MystiWord'
)
