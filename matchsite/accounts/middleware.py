from django.shortcuts import redirect
from django.urls import reverse


# URL name prefixes a logged-in-but-incomplete user is still allowed to hit
# (their own profile edit page, logging out, the Google OAuth dance itself,
# and the Django admin for you as superuser).
ALLOWED_PATH_PREFIXES = ("/profile/edit/", "/logout/", "/accounts/", "/admin/", "/static/", "/media/")


class RequireCompleteProfileMiddleware:
    """
    Username/password signup already collects birth_date + gender before
    the account exists (see accounts.forms.RegistrationForm), so those
    users are always complete. Google sign-in skips that form entirely,
    so this middleware catches anyone (typically a Google sign-in) whose
    Profile has no birth_date yet and forces them to /profile/edit/ first
    — the 18+ check lives in ProfileForm.clean_birth_date, so they can't
    get past this without confirming they're an adult.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if (
            user
            and user.is_authenticated
            and not user.is_superuser
            and not request.path.startswith(ALLOWED_PATH_PREFIXES)
        ):
            profile = getattr(user, "profile", None)
            if profile is None or not profile.birth_date or not profile.gender:
                return redirect(reverse("profile_edit"))

        return self.get_response(request)
