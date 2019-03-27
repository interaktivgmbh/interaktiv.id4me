# -*- coding: UTF-8 -*-
# noinspection PyProtectedMember
from interaktiv.id4me import _
from zope import schema
from zope.interface import Interface
from plone.autoform import directives


class IID4meSchema(Interface):
    client_name = schema.TextLine(
        title=_(
            u'label_client_name',
            default=u'Client name'
        ),
        description=_(
            u'help_client_name',
            default=u''
        ),
        required=True
    )

    preferred_client_id = schema.TextLine(
        title=_(
            u'label_preferred_client_id',
            default=u'Preferred client id'
        ),
        description=_(
            u'help_preferred_client_id',
            default=u''
        ),
        required=False
    )
    logo = schema.TextLine(
        title=_(
            u'label_custom_logo',
            default=u'Custom Logo'
        ),
        description=_(
            u'help_custom_logo',
            default=u''
        ),
        required=False,
    )
    policy = schema.TextLine(
        title=_(
            u'label_policy_url',
            default=u'Policy document URL'
        ),
        description=_(
            u'help_policy_url',
            default=u''
        ),
        required=False,
    )
    tos = schema.TextLine(
        title=_(
            u'label_tos_url',
            default=u'TOS document URL'
        ),
        description=_(
            u'help_tos_url',
            default=u''
        ),
        required=False,
    )

    directives.omitted('ia_data')
    ia_data = schema.Dict(
        title=u'List of all Identity Agents',
        key_type=schema.TextLine(
            title=u'Identifier of Identity Agent'
        ),
        value_type=schema.TextLine(
            title=u"Data provided from Identity Agent",
        ),
        default=dict(),
        required=False
    )

    directives.omitted('user_mapping')
    user_mapping = schema.Dict(
        title=u'List of all Users mapped to their ISS/SUB Keys',
        key_type=schema.TextLine(
            title=u'Key of ISS and SUB combined'
        ),
        value_type=schema.TextLine(
            title=u"ID of User",
        ),
        default=dict(),
        required=False
    )
