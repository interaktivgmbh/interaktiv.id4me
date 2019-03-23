from plone import api


# noinspection PyUnusedLocal
def setup_after(context):
    extend_userschema()


def extend_userschema():
    portal_memberdata = api.portal.get_tool('portal_memberdata')

    if not portal_memberdata.hasProperty('id4me_tokens'):
        portal_memberdata.manage_addProperty(
            id="id4me_tokens",
            value="{}",
            type="text"
        )
