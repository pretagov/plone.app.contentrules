from setuptools import setup, find_packages

version = '2.0b4'

setup(name='plone.app.contentrules',
      version=version,
      description="Plone integration for plone.contentrules",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Markus Fuhrer and Martin Aspeli',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.contentrules',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'five.formlib',
        'kss.core',
        'plone.contentrules',
        'plone.memoize',
        'plone.stringinterp',
        'plone.app.form',
        'plone.app.kss',
        'plone.app.vocabularies',
        'transaction',
        'zope.annotation',
        'zope.browser',
        'zope.component',
        'zope.container',
        'zope.event',
        'zope.formlib',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.publisher',
        'zope.schema',
        'zope.site',
        'zope.traversing',
        'zope.app.publication',
        'Acquisition',
        'Plone',
        'Products.Archetypes',
        'Products.ATContentTypes',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Products.GenericSetup',
        'Products.statusmessages',
        'ZODB3',
        'Zope2 >= 2.12.3',
      ],
      )
