try:
    from setuptools import setuptools
except ImportError:
    from disutils.core import setup

config = {
    'description': 'My Project',
    'author': 'My Name',
    'url': 'URL to get it at',
    'download_url': 'WHere to download it.',
    'author_email': 'My email',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}
