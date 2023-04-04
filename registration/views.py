from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.views.generic import FormView
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from registration.forms import ResendActivationForm
from django.contrib.auth.models import User
from django.contrib import messages
from allauth.account.views import ConfirmEmailView, LoginView, LogoutView, SignupView, PasswordResetView, \
    PasswordResetDoneView, EmailVerificationSentView, PasswordResetFromKeyView, PasswordResetFromKeyDoneView, EmailView
from allauth.account.utils import complete_signup, perform_login
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.adapter import get_adapter


def profile(request):
    return redirect(reverse('home'))


class ResendActivationView(FormView):

    template_name = 'account/resend_activation.html'
    form_class = ResendActivationForm

    def get_success_url(self):
        return reverse('account_email_verification_sent')

    def form_valid(self, form):
        form.save(self.request)
        return super(ResendActivationView, self).form_valid(form)


class SignupView(SignupView):
    template_name = 'account/signup.html'
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        self.user = form.save(self.request)
        try:
            return complete_signup(
                self.request, self.user,
                False, self.success_url
            )
        except ImmediateHttpResponse as e:
            return e.response

signup = SignupView.as_view()


class LoginView(LoginView):
    template_name = 'students/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        if self.request.school.enterprise:
            context['base_template'] = 'academy/__base_enterprise.html'
        else:
            context['base_template'] = 'academy/__base_student_site.html'
        return context


class LogoutView(LogoutView):
    template_name = 'students/logout.html'


# class SignupView(SignupView):
#     template_name = 'students/signup.html'


# class PasswordResetView(PasswordResetView):
#     template_name = 'students/password_reset.html'

#     def get_form_class(self):
#         return StudentsResetPasswordForm

#     def get_context_data(self, **kwargs):
#         context = super(PasswordResetView, self).get_context_data(**kwargs)
#         if self.request.school.enterprise:
#             context['base_template'] = 'academy/__base_enterprise.html'
#         else:
#             context['base_template'] = 'academy/__base_student_site.html'
#         return context

#     def get_success_url(self):
#         return reverse('students.password.reset.done')


# class PasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'students/password_reset_done.html'

#     def get_context_data(self, **kwargs):
#         context = super(PasswordResetDoneView, self).get_context_data(**kwargs)
#         if self.request.school.enterprise:
#             context['base_template'] = 'academy/__base_enterprise.html'
#         else:
#             context['base_template'] = 'academy/__base_student_site.html'
#         return context


# class StudentsResendActivationView(ResendActivationView):
#     template_name = 'students/resend_activation.html'

#     def get_success_url(self):
#         return reverse('students.email.verify')


# class EmailVerificationSentView(EmailVerificationSentView):
#     template_name = 'students/verification_sent.html'


# class PasswordResetFromKeyView(PasswordResetFromKeyView):
#     template_name = 'students/password_reset_from_key.html'


# class PasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
#     template_name = 'students/password_reset_from_key_done.html'


# class ChangeEmailView(EmailView):
#     template_name = 'student_settings/change_email.html'

#     def get_success_url(self):
#         return reverse('students.change.email')

# students_change_email = StudentsChangeEmailView.as_view()


# class StudentConfirmEmailView(ConfirmEmailView):

#     def get_template_names(self):
#         if self.request.method == 'POST':
#             return ["students/email_confirmed.html"]
#         else:
#             return ["students/email_confirm.html"]


# class EmailVerificationSentView(EmailVerificationSentView):
#     template_name = 'students/verification_sent.html'
