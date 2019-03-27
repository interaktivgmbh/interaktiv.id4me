# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from id4me_rp_client.id4me_exceptions import ID4meDNSResolverException
from plone import api
from interaktiv.id4me import _
from interaktiv.id4me.utilities.authentication import get_authentication_utility
from zExceptions import Forbidden
from zope.security import checkPermission


class ID4meView(BrowserView):
    template = ViewPageTemplateFile('templates/authenticate.pt')

    @property
    def auth_util(self):
        return get_authentication_utility()

    def __call__(self):
        if 'login' in self.request.form:
            self._generate_url('login')
        elif 'register' in self.request.form:
            if not self.user_can_register():
                raise Forbidden()
            self._generate_url('register')
        elif 'connect' in self.request.form:
            if checkPermission('cmf.SetOwnPassword', self.context):
                self._generate_url('connect')
            else:
                raise Forbidden()

        return self.template(self)

    def _generate_url(self, mode):
        id4me_domain = self.request.form.get('id4me-domain', '')
        messages = IStatusMessage(self.request)
        translator = self.context.translate
        if not id4me_domain:
            messages.add(
                translator(
                    _(u'message_no_domain_provided')
                )
            )
            return None
        try:
            url = self.auth_util.generate_authentication_url(
                id4me_domain,
                mode=mode
            )
            self.request.response.redirect(url)
        except ID4meDNSResolverException:
            messages.add(
                translator(
                    _(
                        u'message_invalid_domain_provided',
                        mapping={u'agent': id4me_domain}
                    )
                )
            )

    @staticmethod
    def is_logged_in():
        return not api.user.is_anonymous()

    @staticmethod
    def user_can_register():
        return api.portal.get_registry_record(name='plone.enable_self_reg')
