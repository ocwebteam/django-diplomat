
try:
	from setuptools import setup
except ImportError:
	from ez_setup import use_setuptools
	use_setuptools()
	from setuptools import setup

setup(
	name='djangoool',
	version=__import__('djangoool').__version__,
	description='A Django interface to the pycountry module.',
	author='Justin Locsei',
	author_email='justin.locsei@oberlin.edu',
	url='http://github.com/cilcoberlin/djangoool/',
	download_url='https://github.com/cilcoberlin/djangoool/zipball/master',
	long_description=open('README.md', 'r').read(),
	packages=[
		'djangoool',
		'djangoool.management',
		'djangoool.management.commands'
	],
	requires=[
		'pycountry'
	],
	install_requires=[
		'pycountry'
	],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Framework :: Django'
	]
)
