from django.contrib.auth.models import User
from django.db import models


class Like(models.Model):
    """One user liking (swiping right on) another."""

    from_user = models.ForeignKey(User, related_name="likes_sent", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="likes_received", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"


class Pass(models.Model):
    """One user passing (swiping left) on another — used to hide them from future browsing."""

    from_user = models.ForeignKey(User, related_name="passes_sent", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="passes_received", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")


class Match(models.Model):
    """Created automatically when two users like each other."""

    user1 = models.ForeignKey(User, related_name="matches_as_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="matches_as_user2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"{self.user1} <-> {self.user2}"

    def other_user(self, user):
        return self.user2 if user == self.user1 else self.user1

    @staticmethod
    def get_or_create_for(user_a, user_b):
        """Always store the pair in a consistent order to keep unique_together meaningful."""
        u1, u2 = sorted([user_a, user_b], key=lambda u: u.pk)
        return Match.objects.get_or_create(user1=u1, user2=u2)
