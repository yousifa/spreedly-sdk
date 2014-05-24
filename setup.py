from distutils.core import setup


setup(
    name='spreedly-sdk',
    version='0.1',
    author='calvin',
    author_email='dani.pyc@gmail.com',
    packages=['spreedly'],
    scripts=[],
    url='https://github.com/calvinpy',
    license='Apache Software License',
    description='The spreedly SDK provides Python APIs to create,'
        'process and manage transactions',
    install_requires=['requests', 'lxml', 'xmltodict'],
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
    keywords="spreedly sdk",
)
