from setuptools import setup

setup(
    name='spreedly-sdk',
    version='0.1.1',
    author='calvin',
    author_email='dani@aplaza.me',
    packages=['spreedly_sdk'],
    scripts=[],
    test_suite='tests',
    test_require=['mock'],
    zip_safe=False,
    url='https://github.com/calvinpy',
    license='Apache Software License',
    description='Python Interface to the Spreedly API',
    install_requires=['requests>=1.1.0', 'lxml', 'xmltodict', 'python-dateutil'],
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
