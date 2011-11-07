
from setuptools import setup, find_packages

setup(
	name='djangoool',
	version=__import__('djangoool').__version__,
	description='A Django interface for working with ISO 639 languages.',
	author='Justin Locsei',
	author_email='justin.locsei@oberlin.edu',
	url='https://github.com/cilcoberlin/djangoool',
	download_url='https://github.com/cilcoberlin/djangoool/zipball/master',
	packages=find_packages(),
	package_data={'': ["*.*"]},
	include_package_data=True,
	zip_safe=False,
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Framework :: Django'
	]
)
