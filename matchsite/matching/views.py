from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages as django_messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from .models import Like, Match, Pass


@login_required
def discover(request):
    my_profile, _ = Profile.objects.get_or_create(user=request.user)

    already_seen_ids = set(
        Like.objects.filter(from_user=request.user).values_list("to_user_id", flat=True)
    ) | set(
        Pass.objects.filter(from_user=request.user).values_list("to_user_id", flat=True)
    )
    already_seen_ids.add(request.user.id)

    candidates = Profile.objects.exclude(user_id__in=already_seen_ids).filter(is_active_seeker=True)

    if my_profile.looking_for:
        candidates = candidates.filter(gender=my_profile.looking_for)

    next_profile = candidates.order_by("?").first()

    return render(request, "matching/discover.html", {"next_profile": next_profile})


@login_required
def like_profile(request, username):
    if request.method != "POST":
        return redirect("discover")

    target = get_object_or_404(User, username=username)
    if target != request.user:
        Like.objects.get_or_create(from_user=request.user, to_user=target)

        mutual = Like.objects.filter(from_user=target, to_user=request.user).exists()
        if mutual:
            Match.get_or_create_for(request.user, target)
            django_messages.success(request, f"It's a match with {target.username}! 🎉")

    return redirect("discover")


@login_required
def pass_profile(request, username):
    if request.method != "POST":
        return redirect("discover")

    target = get_object_or_404(User, username=username)
    if target != request.user:
        Pass.objects.get_or_create(from_user=request.user, to_user=target)

    return redirect("discover")


@login_required
def matches_list(request):
    matches = Match.objects.filter(user1=request.user) | Match.objects.filter(user2=request.user)
    matches = matches.select_related("user1", "user2").order_by("-created_at")
    match_rows = [(m, m.other_user(request.user)) for m in matches]
    return render(request, "matching/matches_list.html", {"match_rows": match_rows})
