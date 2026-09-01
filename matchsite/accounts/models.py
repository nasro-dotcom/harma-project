from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
]


class Profile(models.Model):
    """Extra dating-profile info attached to every User."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    looking_for = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active_seeker = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profile_detail", args=[self.user.username])

    @property
    def age(self):
        if not self.birth_date:
            return None
        from datetime import date

        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )


class ProfilePhoto(models.Model):
    """An extra gallery photo attached to a Profile (in addition to the main cover photo)."""

    profile = models.ForeignKey(Profile, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_photos/gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["uploaded_at"]

    def __str__(self):
        return f"Photo for {self.profile.user.username}"
