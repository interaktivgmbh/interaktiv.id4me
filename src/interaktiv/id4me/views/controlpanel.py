# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from interaktiv.id4me import _
from interaktiv.id4me.registry.id4me import IID4meSchema
from z3c.form import button
from plone import api
from Products.statusmessages.interfaces import IStatusMessage


class ID4meControlPanelForm(controlpanel.RegistryEditForm):
    id = "ID4meControlPanel"
    label = _(u"ID4me Settings")
    schema = IID4meSchema

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleSave(self, action):
        super(ID4meControlPanelForm, self).handleSave(self, action)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        super(ID4meControlPanelForm, self).handleCancel(self, action)

    @button.buttonAndHandler(_(u"Reset ia data"), name='reset_data')
    def handle_reset_data(self, action):
        api.portal.set_registry_record(
            name='ia_data',
            interface=IID4meSchema,
            value=dict()
        )
        # noinspection PyArgumentList
        IStatusMessage(self.request).addStatusMessage(
            _(u"message_data_resetted"),
            type="info"
        )
        self.request.response.redirect(self.request.getURL())


class ID4meControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ID4meControlPanelForm
