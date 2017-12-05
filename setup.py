from setuptools import setup

setup(
    name='catalog',
    author='Kevin Lazich',
    author_email='dev@kevinlazich.com',
    license='MIT',
    packages=['catalog'],
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy', 'mimesis',
    ],
)