from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    def check(user):
        return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'admin'

    decorated = user_passes_test(check, login_url='/login/admin/')(view_func)
    return decorated