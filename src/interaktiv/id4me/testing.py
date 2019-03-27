# coding=utf-8
import importlib
import os

from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2
from zope.configuration import xmlconfig

os.environ['PLONE_CSRF_DISABLED'] = 'true'


class InteraktivID4meLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    products_to_import = [
        'interaktiv.id4me',
    ]

    def setUpZope(self, app, configuration_context):
        for product_name in self.products_to_import:
            module = importlib.import_module(product_name)
            xmlconfig.file(
                'configure.zcml',
                module,
                context=configuration_context
            )

    def setUpPloneSite(self, portal):
        for product_name in self.products_to_import:
            if product_name == 'interaktiv.id4me':
                continue
            applyProfile(portal, product_name + ':default')

    def tearDownZope(self, app):
        pass


INTERAKTIV_ID4ME_FIXTURE = InteraktivID4meLayer()
INTERAKTIV_ID4ME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(INTERAKTIV_ID4ME_FIXTURE, z2.ZSERVER_FIXTURE),
    name="InteraktivID4meLayer:Functional"
)
