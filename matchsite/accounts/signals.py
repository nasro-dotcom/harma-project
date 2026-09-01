from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from .models import Profile


@receiver(user_signed_up)
def create_profile_for_new_user(request, user, **kwargs):
    """
    Fires for BOTH regular signups and Google sign-ins that go through
    allauth. Our own `accounts.views.register` already creates a full
    Profile with birth_date/gender before this signal would even fire
    for a normal signup, so `get_or_create` here just makes sure a
    Google user (who has no birth_date/gender yet) gets an empty
    Profile — `RequireCompleteProfileMiddleware` then sends them to
    /profile/edit/ to fill in birth date (age 18+ enforced there) and
    gender before they can browse anyone.
    """
    Profile.objects.get_or_create(user=user)
