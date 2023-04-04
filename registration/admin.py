
from allauth.account.utils import send_email_confirmation
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from registration.models import Profile
from django.contrib import messages


class RegistrationProfileMixin(admin.ModelAdmin):

    actions = ['activate_users', 'resend_activation_email']

    def get_actions(self, request):
        return super(RegistrationProfileMixin, self).get_actions(request)

    def activate_users(self, request, queryset):
        """
        Activates the selected users, if they are not already
        activated.

        """
        queryset.update()
        for profile in queryset:
            profile.user.is_active = True
            profile.user.save()

        messages.success(request, 'Users have been activated successfully')
    activate_users.short_description = _("Activate users")

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.
        """
        for profile in queryset:
            send_email_confirmation(request, profile.user, signup=False)
        messages.success(request, 'Emails have been sent successfully')

    resend_activation_email.short_description = _("Re-send activation emails")

admin.site.register(Profile)