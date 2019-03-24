# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from thokas.id4me import _
from thokas.id4me.registry.id4me import IID4meSchema


class ID4meControlPanelForm(controlpanel.RegistryEditForm):
    id = "ID4meControlPanel"
    label = _(u"ID4me Settings")
    schema = IID4meSchema


class ID4meControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ID4meControlPanelForm
