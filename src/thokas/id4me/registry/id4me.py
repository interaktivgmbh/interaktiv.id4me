# -*- coding: UTF-8 -*-
# noinspection PyProtectedMember
from thokas.id4me import _
from zope import schema
from zope.interface import Interface


class IID4meSchema(Interface):
    """"""

    iss_data = schema.List(
        label=_(
            u'label_list_ia_data',
            default=u'List of all Identity Agents'
        ),
        value_type=schema.Text(
            title=_(
                u"label_ia_data",
                default=u"Data providede from Identity Agent"
            ),
            required=False
        ),
        required=False
    )
