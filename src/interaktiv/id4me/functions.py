from Products.CMFPlone.utils import safe_unicode
from plone import api
from interaktiv.id4me.registry.id4me import IID4meSchema


def save_authority_registration(auth_name, auth_content):
    ia_data = api.portal.get_registry_record(
        name="ia_data",
        interface=IID4meSchema
    )

    auth_name = safe_unicode(auth_name)

    if ia_data is None:
        ia_data = dict()

    ia_data[auth_name] = safe_unicode(auth_content)

    api.portal.set_registry_record(
        name="ia_data",
        interface=IID4meSchema,
        value=ia_data
    )


def load_authority_registration(auth_name):
    ia_data = api.portal.get_registry_record(
        name="ia_data",
        interface=IID4meSchema
    )

    if auth_name in ia_data:
        return ia_data[auth_name].encode('UTF-8')

    return None
