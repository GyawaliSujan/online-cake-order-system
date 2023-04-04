from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator

from six import wraps


def admin_only_access(f):
    # requires kwarg = school_id

    @wraps(f)
    def wrapper(request, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/accounts/login/')
        if not request.user.is_superuser:
            return redirect('/')
        request.is_admin = True
        return f(request, **kwargs)
    return wrapper


class AdminOnlyAccessMixin(object):
    # requires kwarg = school_id

    @method_decorator(admin_only_access)
    def dispatch(self, request, *args, **kwargs):
        return super(PrincipalOnlyAccessMixin, self).dispatch(request, *args, **kwargs)
