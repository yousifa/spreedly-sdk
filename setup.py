from setuptools import setup
from spreedly import __version__


setup(
    name='spreedly-sdk',
    version=__version__,
    author='calvin',
    author_email='dani.pyc@gmail.com',
    packages=['spreedly'],
    scripts=[],
    test_suite='tests',
    zip_safe=False,
    url='https://github.com/calvinpy',
    license='Apache Software License',
    description='Python Interface to the Spreedly API',
    install_requires=['requests>=1.1.0', 'lxml', 'xmltodict'],
    dependency_links=[
        'https://github.com/kennethreitz/requests',
        'https://github.com/lxml/lxml/',
        'https://github.com/martinblech/xmltodict'],
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='python spreedly rest sdk',
)
