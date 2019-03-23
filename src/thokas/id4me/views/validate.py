# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from thokas.id4me.utilities.authentication import get_authentication_utility
from zExceptions import BadRequest


class ID4meValidateView(BrowserView):
    template = ViewPageTemplateFile('templates/validate.pt')

    @property
    def auth_util(self):
        return get_authentication_utility()

    def __call__(self):
        if 'code' not in self.request.form:
            raise BadRequest('no code given')

        code = self.request.form.get('code')
        state = self.request.form.get('state')

        self.auth_util.validate_authentication(code, state)

        return self.template(self)
