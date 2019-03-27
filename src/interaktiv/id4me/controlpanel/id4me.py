# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_hasattr
from plone.registry.interfaces import IRegistry
from interaktiv.id4me.registry.id4me import IID4meSchema
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implementer
from zope.site.hooks import getSite


@implementer(IID4meSchema)
class ID4meControlPanelAdapter(object):
    adapts(IPloneSiteRoot)

    def __init__(self, context):
        self.context = context
        self.portal = getSite()
        registry = getUtility(IRegistry)
        self.encoding = 'utf-8'
        self.id4me_settings = registry.forInterface(
            IID4meSchema
        )

    def get_client_name(self):
        return self.id4me_settings.client_name

    def set_client_name(self, value):
        if safe_hasattr(self.id4me_settings, 'client_name'):
            self.id4me_settings.client_name = value

    client_name = property(get_client_name, set_client_name)

    def get_preferred_client_id(self):
        return self.id4me_settings.preferred_client_id

    def set_preferred_client_id(self, value):
        if safe_hasattr(self.id4me_settings, 'preferred_client_id'):
            self.id4me_settings.preferred_client_id = value

    preferred_client_id = property(
        get_preferred_client_id,
        set_preferred_client_id
    )
