from plone import api
from thokas.id4me.registry.id4me import IID4meSchema


def save_authority_registration(auth_name, auth_content):
    ia_data = api.portal.get_registry_record(
        name="ia_data",
        interface=IID4meSchema
    )

    if auth_name not in ia_data:
        ia_data[auth_name] = auth_content
    else:
        raise NotImplementedError('Case of already existing IA entry')

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
        return ia_data[auth_name]
    else:
        raise NotImplementedError('IA not registered')
