from distutils.core import setup

#cc = """License :: OSI Approved :: BSD License
#Operating System :: OS Independent
#Development Status :: 3 - Alpha
#Environment :: Console
#Intended Audience :: Developers
#Topic :: Software Development :: User Interfaces
#Topic :: Software Development :: Libraries :: Python Modules
#Topic :: System :: Logging
#Topic :: System :: Shells
#"""

setup(
	name = 'batchcli',
	packages = ['batchcli'],
	version = '0.2',
	description = 'A simple API to run tasks in batch mode and track progress on CLI.',
	url = 'https://github.com/siasi/batchcli',
	author = 'Stefano Iasi',
	author_email = 'siasi@cisco.com'
#	classifiers = cc
	)
