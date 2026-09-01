from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages as django_messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm, RegistrationForm
from .models import Profile, ProfilePhoto


def home(request):
    if request.user.is_authenticated:
        return redirect("discover")
    return render(request, "accounts/home.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                birth_date=form.cleaned_data["birth_date"],
                gender=form.cleaned_data["gender"],
                looking_for=form.cleaned_data["looking_for"],
            )
            login(request, user)
            django_messages.success(request, "Welcome! Complete your profile to get better matches.")
            return redirect("profile_edit")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            for image_file in form.cleaned_data.get("extra_photos") or []:
                ProfilePhoto.objects.create(profile=profile, image=image_file)
            django_messages.success(request, "Profile updated.")
            return redirect("profile_detail", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(
        request,
        "accounts/profile_edit.html",
        {"form": form, "gallery_photos": profile.photos.all()},
    )


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(ProfilePhoto, pk=photo_id, profile__user=request.user)
    if request.method == "POST":
        photo.delete()
        django_messages.success(request, "Photo deleted.")
    return redirect("profile_edit")


@login_required
def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=user)
    return render(request, "accounts/profile_detail.html", {"profile_user": user, "profile": profile})
