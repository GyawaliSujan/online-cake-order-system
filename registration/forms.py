
from allauth.account.adapter import get_adapter
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, ResetPasswordKeyForm
from allauth.account.utils import send_email_confirmation
from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .models import Profile


class SignupForm(SignupForm):
    required_css_class = 'required'

    email = forms.EmailField(label=_("E-mail"),
                             widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                            'class': 'form-control',
                                                            'type': 'email',
                                                            'data-required': 'required'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'type': 'password',
                                                                  'data-required': 'required'}),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password',
                                                                  'class': 'form-control',
                                                                  'type': 'password',
                                                                  'data-required': 'required'}),
                                label=_("Password (again)"))

    def clean_password1(self):
        password = self.data['password1']
        if len(password) < 6:
            raise ValidationError('Password must be at least 6 characters')
        return super(SignupForm, self).clean_password1()

    def clean(self, *args, **kwargs):
        self.clean_password1()
        return super(SignupForm, self).clean(*args, **kwargs)


class ResetPasswordForm(ResetPasswordForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                            'class': 'form-control',
                                                            'type': 'text',
                                                            'data-required': 'required'}))


class ResetPasswordKeyForm(ResetPasswordKeyForm):
    password1 = forms.CharField(label=_("New password"),
                                widget=forms.PasswordInput(attrs={'placeholder': 'New password',
                                                                  'class': 'form-control',
                                                                  'type': 'password',
                                                                  'data-required': 'required'}))
    password2 = forms.CharField(label=_("New password confirmation"),
                                widget=forms.PasswordInput(attrs={'placeholder': 'New password confirmation',
                                                                  'class': 'form-control',
                                                                  'type': 'password',
                                                                  'data-required': 'required'}))

    def save(self):
        # TODO: be worried about this code, if we will use multiple email adresses.
        # Probably this may lead to security bug
        for e in self.user.emailaddress_set.all():
            get_adapter().confirm_email(None, e)

        super(ResetPasswordKeyForm, self).save()


class LoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['login'] = forms.CharField(max_length=254,
                                               widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                                             'class': 'form-control',
                                                                             'type': 'text',
                                                                             'data-required': 'required'}),
                                               error_messages={'required': 'Please enter a email.',
                                                               })

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'type': 'password',
                                                                 'data-required': 'required'}),
                               error_messages={'required': 'Please enter a password.'})


class ResendActivationForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                            'class': 'form-control',
                                                            'type': 'text',
                                                            'data-required': 'required'}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        users = get_user_model().objects \
            .filter(Q(email__iexact=email)
                    | Q(emailaddress__email__iexact=email)).distinct()
        if not users.exists():
            raise forms.ValidationError(_("The e-mail address is not assigned"
                                          " to any user account"))
        self.user = users[0]
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):

        send_email_confirmation(request, self.user, signup=False)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'email',
        ]

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email (Required)',
                                             'class': 'form-control',
                                             'type': 'email', }),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name', 'phone', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name (Required)',
                                           'class': 'form-control',
                                           'type': 'text', }),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
