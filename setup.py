from setuptools import setup

setup(
    name='guardium-automation-tool-kit',
    version='1.0',
    packages=['guardiumATK'],
    package_dir={'': 'examples'},
    url='https://github.com/jklahn/guardium-automation-tool-kit',
    license='Apache-2.0 license',
    author='Josh Klahn',
    author_email='klahn@us.ibm.com',
    description='Provides a pythonic foundation to leverage Guardium REST APIs and CLI APIs to automate tasks in Guardium'
)
