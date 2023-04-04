from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as django_login

from registration.models import Profile

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super(AccountAdapter, self).save_user(
            request, user, form, commit)
        self.format_email_subject("Hello From Cake-G")

    def get_login_redirect_url(self, request):
        return '/'

class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = sociallogin.account.extra_data['email'].lower()
            email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, bounce back to the login page
        # account = User.objects.get(email=email).socialaccount_set.first()
        # provider_name = account.provider.capitalize().replace('_oauth2', '')
        # messages.error(request, "A "+provider_name+" account already exists associated to "+email_address.email+". Log in with that instead, and connect your "+sociallogin.account.provider.capitalize()+" account through your profile page to link them together.")
        # raise ImmediateHttpResponse(redirect('/accounts/login'))
        user = email_address.user
        sociallogin.connect(request, user)
