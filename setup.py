from setuptools import setup, find_packages

setup(
    name='discovery',
    version='0.1.0',
    packages=find_packages(),
    license='BSD 2-clause "Simplified" License',
    install_requires=[
	"Babel>=2.6.0",
	"pytz",
    ],
)
