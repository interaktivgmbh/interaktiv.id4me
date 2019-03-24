# -*- coding: utf-8 -*-
import json

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from thokas.id4me.utilities.authentication import get_authentication_utility
from zExceptions import BadRequest, Forbidden


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

        if state == 'login':
            user = self.auth_util.verify_user_login(code, state)
            if user:
                acl_users = getToolByName(self.context, 'acl_users')

                # noinspection PyProtectedMember
                acl_users.session._setupSession(
                    user.getId(),
                    self.request.response
                )

                self.request.response.redirect(
                    api.portal.get_navigation_root(context=self.context)
                )
        elif state == 'register':
            user = self.auth_util.register_user(code, state)
            acl_users = getToolByName(self.context, 'acl_users')

            # noinspection PyProtectedMember
            acl_users.session._setupSession(
                user.getId(),
                self.request.response
            )

            self.request.response.redirect(
                api.portal.get_navigation_root(context=self.context)
            )
        elif state == 'connect':
            if api.user.is_anonymous():
                raise Forbidden()
            user = api.user.get_current()

            self.auth_util.connect_user_login(user=user, code=code)

            self.request.response.redirect(
                api.portal.get_navigation_root(context=self.context)
            )

        return self.template(self)
