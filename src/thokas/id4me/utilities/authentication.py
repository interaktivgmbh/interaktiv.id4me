# -*- coding: utf-8 -*-
from plone import api
from zope.component import getUtility
from zope.interface import Interface
from thokas.id4me.id4me_functions import save_authority_registration
from thokas.id4me.id4me_functions import load_authority_registration
from thokas.id4me.registry.id4me import IID4meSchema
from id4me_rp_client import (
    ID4meClient, OIDCApplicationType, ID4meClaimsRequest,
    ID4meClaimRequestProperties, OIDCClaim
)
# noinspection PyProtectedMember
from thokas.id4me import _


class IAuthenticationUtility(Interface):
    """ utility to provide methods """


def get_authentication_utility():
    return getUtility(AuthenticationUtility)


class AuthenticationUtility(object):

    def generate_authentication_url(self, agent_identifier):
        client = self.setup_id4me_client()
        ctx = client.get_rp_context(id4me=agent_identifier)

        link = client.get_consent_url(
            ctx,
            state=agent_identifier,
            claimsrequest=ID4meClaimsRequest(
                userinfo_claims=self._generate_claims()
            )
        )

        return link

    def validate_authentication(self, code, state):
        client = self.setup_id4me_client()
        ctx = client.get_rp_context(id4me=state)

        client.get_idtoken(context=ctx, code=code)

    @staticmethod
    def _generate_claims():
        portal = api.portal.get_navigation_root()
        translator = portal.translate
        reasons = {
            'name': translator(_(u'reason_name')),
            'email': translator(_(u'reason_email')),
            'email_verified': translator(_(u'reason_email_verified')),
            'birthdate': translator(_(u'reason_birthdate'))
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

    @staticmethod
    def __get_policy():
        policy_reference = api.portal.get_registry_record(
            name='policy',
            interface=IID4meSchema
        )
        if policy_reference:
            if not policy_reference.isBroken():
                policy = policy_reference.to_object
                if policy:
                    return policy.absolute_url()
        return None

    @staticmethod
    def __get_tos():
        tos_reference = api.portal.get_registry_record(
            name='policy',
            interface=IID4meSchema
        )
        if tos_reference:
            if not tos_reference.isBroken():
                tos = tos_reference.to_object
                if tos:
                    return tos.absolute_url()
        return None

    @staticmethod
    def __get_client_name():
        return api.portal.get_registry_record(
            name='client_name',
            interface=IID4meSchema
        )

    def setup_id4me_client(self):
        portal = api.portal.get_navigation_root()
        validation_url = portal.absolute_url() + '/@@id4me-validate'

        return ID4meClient(
            get_client_registration=load_authority_registration,
            save_client_registration=save_authority_registration,
            app_type=OIDCApplicationType.web,
            validate_url=validation_url,
            client_name=self.__get_client_name(),
            logo_url=self.__get_logo(),
            policy_url=self.__get_policy(),
            tos_url=self.__get_tos(),
            private_jwks_json=ID4meClient.generate_new_private_keys_set()
        )
