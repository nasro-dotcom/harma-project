from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from matching.models import Match
from .models import Message


@login_required
def conversation(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.user not in (match.user1, match.user2):
        return HttpResponseForbidden("Not your conversation.")

    other_user = match.other_user(request.user)

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            Message.objects.create(match=match, sender=request.user, text=text)
        return redirect("conversation", match_id=match.id)

    Message.objects.filter(match=match).exclude(sender=request.user).update(is_read=True)
    msgs = match.messages.select_related("sender").all()

    return render(
        request,
        "chat/conversation.html",
        {"match": match, "other_user": other_user, "chat_messages": msgs},
    )
