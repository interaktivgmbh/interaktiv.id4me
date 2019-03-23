# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from thokas.id4me.utilities.authentication import get_authentication_utility
from zExceptions import BadRequest


class ID4meLoginView(BrowserView):
    template = ViewPageTemplateFile('templates/login.pt')

    @property
    def authentication_util(self):
        return get_authentication_utility()

    def __call__(self):
        if 'submit' in self.request.form:
            agent_identifier = self.request.form.get('identifier', '')
            if not agent_identifier:
                raise BadRequest('no agent identifier given')
            url = self.authentication_util.generate_authentication_url()
            self.request.response.redirect(url)

        return self.template(self)
