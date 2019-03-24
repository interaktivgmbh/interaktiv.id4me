# -*- coding: UTF-8 -*-
# noinspection PyProtectedMember
from plone.app.vocabularies.catalog import CatalogSource
from thokas.id4me import _
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import Interface


class IID4meSchema(Interface):
    client_name = schema.Text(
        title=_(
            u'label_client_name',
            default=u'Client name'
        ),
        required=True
    )

    preferred_client_id = schema.Text(
        title=_(
            u'label_preferred_client_id',
            default=u'Preferred client id'
        ),
        required=False
    )
    logo = schema.Text(
        title=_(
            u'label_custom_logo',
            default=u'Custom Logo'
        ),
        description=_(u'help_custom_logo'),
        required=False,
    )
    policy = schema.Text(
        title=_(
            u'label_policy_url',
            default=u'Policy document URL'
        ),
        required=False,
    )
    tos = schema.Text(
        title=_(
            u'label_tos_url',
            default=u'TOS document URL'
        ),
        required=False,
    )

    ia_data = schema.Dict(
        title=_(
            u'label_list_ia_data',
            default=u'List of all Identity Agents'
        ),
        key_type=schema.Text(
            title=_(
                u'label_ia_key',
                default=u'Identifier of Identity Agent'
            )
        ),
        value_type=schema.Text(
            title=_(
                u"label_ia_data",
                default=u"Data providede from Identity Agent"
            ),
        ),
        default=dict(),
        required=False
    )
