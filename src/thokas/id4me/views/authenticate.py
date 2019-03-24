# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from thokas.id4me.utilities.authentication import get_authentication_utility
from zExceptions import BadRequest


class ID4meView(BrowserView):
    template = ViewPageTemplateFile('templates/authenticate.pt')

    @property
    def auth_util(self):
        return get_authentication_utility()

    def __call__(self):
        if 'login' in self.request.form:
            self._generate_url('login')
        elif 'register' in self.request.form:
            self._generate_url('register')

        return self.template(self)

    def _generate_url(self, mode):
            agent_identifier = self.request.form.get('identifier', '')
            if not agent_identifier:
                raise BadRequest('no agent identifier given')
            url = self.auth_util.generate_authentication_url(
                agent_identifier,
                mode=mode
            )
            self.request.response.redirect(url)


class ID4meConnectView(ID4meView):
    template = ViewPageTemplateFile('templates/connect.pt')

    def __call__(self):
        if 'connect' in self.request.form:
            self._generate_url('connect')

        return self.template(self)
