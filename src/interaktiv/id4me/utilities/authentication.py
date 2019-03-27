# -*- coding: utf-8 -*-
from random import choice

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from id4me_rp_client import (
    ID4meClient, OIDCApplicationType, ID4meClaimsRequest,
    ID4meClaimRequestProperties, OIDCClaim
)
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
# noinspection PyProtectedMember
from interaktiv.id4me import _
from interaktiv.id4me.functions import load_authority_registration
from interaktiv.id4me.functions import save_authority_registration
from interaktiv.id4me.registry.id4me import IID4meSchema
from zope.component import getUtility
# noinspection PyUnresolvedReferences
from zope.globalrequest import getRequest
from zope.interface import Interface
from Products.CMFCore.Expression import Expression, getExprContext


class IAuthenticationUtility(Interface):
    """ utility to provide methods """


def get_authentication_utility():
    return getUtility(IAuthenticationUtility)


class AuthenticationUtility(object):

    def generate_authentication_url(self, agent_identifier, mode):
        client = self.setup_id4me_client()
        ctx = client.get_rp_context(id4me=agent_identifier)

        session = self.__get_session()

        claimsrequest = None
        if mode == 'register':
            claimsrequest = ID4meClaimsRequest(
                userinfo_claims=self._generate_claims()
            )

        link = client.get_consent_url(
            ctx,
            state=mode,
            claimsrequest=claimsrequest
        )

        session.set('id4me_authentication', (
            ctx.nonce,
            agent_identifier
        ))

        return link

    def verify_user_login(self, code):
        client = self.setup_id4me_client()

        session = self.__get_session()

        id4me_authentication = session.get('id4me_authentication', ('', ''))
        del session['id4me_authentication']

        ctx = client.get_rp_context(id4me=id4me_authentication[1])
        ctx.nonce = id4me_authentication[0]

        client.get_idtoken(context=ctx, code=code)

        mapping = self.__get_registry_value('user_mapping')

        unique_key = ctx.iss + ctx.sub

        user = None

        if unique_key in mapping:
            user_id = mapping[unique_key]
            user = api.user.get(userid=user_id)

        return user

    def connect_user_login(self, user, code):
        client = self.setup_id4me_client()

        session = self.__get_session()

        id4me_authentication = session.get('id4me_authentication', ('', ''))
        del session['id4me_authentication']

        ctx = client.get_rp_context(id4me=id4me_authentication[1])
        ctx.nonce = id4me_authentication[0]

        client.get_idtoken(context=ctx, code=code)

        self._set_user_connection(user=user, iss=ctx.iss, sub=ctx.sub)

    def register_user(self, code):
        client = self.setup_id4me_client()

        session = self.__get_session()

        id4me_authentication = session.get('id4me_authentication', ('', ''))
        del session['id4me_authentication']

        ctx = client.get_rp_context(id4me=id4me_authentication[1])
        ctx.nonce = id4me_authentication[0]

        client.get_idtoken(context=ctx, code=code)

        userinfo = client.get_user_info(context=ctx)

        user = self._create_user(userinfo)

        self._set_user_connection(user, ctx.iss, ctx.sub)

        return user

    def _set_user_connection(self, user, iss, sub):
        unique_key = safe_unicode(iss + sub)
        user_id = safe_unicode(user.getId())

        mapping = self.__get_registry_value('user_mapping')

        if unique_key not in mapping:
            mapping[unique_key] = user_id

        api.portal.set_registry_record(
            name='user_mapping',
            interface=IID4meSchema,
            value=mapping
        )

    @staticmethod
    def _create_user(userinfo):
        normalizer = getUtility(IIDNormalizer)
        username = normalizer.normalize(userinfo.get('name'))

        try:
            user = api.user.create(
                email=userinfo.get('email'),
                username=username,
                properties=dict(
                    fullname=userinfo.get('name', '')
                )
            )
        except ValueError:
            email = userinfo.get('email')
            email_name = email.split('@')[0]
            username = normalizer.normalize(
                userinfo.get('name') + email_name
            )
            user = api.user.create(
                email=userinfo.get('email'),
                username=username,
                properties=dict(
                    fullname=userinfo.get('name', '')
                )
            )

        return user

    @staticmethod
    def __get_session():
        portal = api.portal.get()
        sdm = getToolByName(portal, 'session_data_manager')
        session = sdm.getSessionData(create=True)

        return session

    @staticmethod
    def _get_session_value(session, key):
        if hasattr(session, '_container'):
            # noinspection PyProtectedMember
            if key in session._container:
                # noinspection PyProtectedMember
                return session._container[key]
        if key in session:
            return session[key]
        return None

    @staticmethod
    def _generate_random_key():
        # generate list with all alphanumeric lower characters
        letters = [chr(x) for x in range(48, 58) + range(97, 123)]
        # noinspection PyUnusedLocal
        return "".join([choice(letters) for i in range(12)])

    @staticmethod
    def _generate_claims():
        portal = api.portal.get()
        translator = portal.translate
        reasons = {
            'name': translator(_(u'reason_name')),
            'email': translator(_(u'reason_email')),
            'email_verified': translator(_(u'reason_email_verified')),
            'birthdate': translator(_(u'reason_birthdate'))
            # ToDo: extend with picture and locale Claim
        }
        return {
            OIDCClaim.name: ID4meClaimRequestProperties(
                reason=reasons['name']
            ),
            OIDCClaim.email: ID4meClaimRequestProperties(
                essential=True,
                reason=reasons['email']
            ),
            OIDCClaim.email_verified: ID4meClaimRequestProperties(
                reason=reasons['email_verified']
            ),
            OIDCClaim.birthdate: ID4meClaimRequestProperties(
                reason=reasons['birthdate']
            ),
        }

    def __get_logo(self):
        logo = api.portal.get_registry_record(
            name='logo',
            interface=IID4meSchema
        )
        if logo:
            raise NotImplementedError('Logo from ID4me Interface')
        else:
            portal = api.portal.get()
            return portal.absolute_url() + '/@@site-logo'

    def __get_policy(self):
        policy_url = api.portal.get_registry_record(
            name='policy',
            interface=IID4meSchema
        )
        if policy_url:
            return self._evaluate_expression(policy_url)
        return None

    def __get_tos(self):
        tos_link = api.portal.get_registry_record(
            name='policy',
            interface=IID4meSchema
        )
        if tos_link:
            return self._evaluate_expression(tos_link)
        return None

    @staticmethod
    def _evaluate_expression(expression):
        portal = api.portal.get()
        expression = Expression(expression)

        expression_context = getExprContext(context=portal)

        return expression(expression_context)

    def __get_client_name(self):
        client_name = self.__get_registry_value('client_name')
        if not client_name:
            client_name = api.portal.get_registry_record(
                name='plone.site_title'
            )

        return client_name

    def __get_client_id(self):
        return self.__get_registry_value('preferred_client_id')

    @staticmethod
    def __get_registry_value(name):
        return api.portal.get_registry_record(
            name=name,
            interface=IID4meSchema
        )

    def setup_id4me_client(self):
        portal = api.portal.get()
        validation_url = portal.absolute_url() + '/@@id4me-validate'

        return ID4meClient(
            get_client_registration=load_authority_registration,
            save_client_registration=save_authority_registration,
            app_type=OIDCApplicationType.web,
            validate_url=validation_url,
            client_name=self.__get_client_name(),
            preferred_client_id=self.__get_client_id(),
            logo_url=self.__get_logo(),
            policy_url=self.__get_policy(),
            tos_url=self.__get_tos(),
            requireencryption=False,
            private_jwks_json=ID4meClient.generate_new_private_keys_set()
        )
