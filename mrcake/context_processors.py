from django.conf import settings


def settings_data(request):
    return {
        "PHONE_NUMBERS": settings.PHONE_NUMBERS,
        "CONTACT_EMAIL": settings.CONTACT_EMAIL
    }