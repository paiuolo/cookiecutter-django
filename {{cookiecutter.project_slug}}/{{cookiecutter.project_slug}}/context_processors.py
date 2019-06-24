from django.conf import settings


def emails_domain_settings(request):
    return {
        "EMAILS_DOMAIN": settings.EMAILS_DOMAIN,
        "EMAILS_SITE_NAME": settings.EMAILS_SITE_NAME
    }

def get_repository_rev(request):
    return {
        "REPOSITORY_REV": settings.REPOSITORY_REV
    }
