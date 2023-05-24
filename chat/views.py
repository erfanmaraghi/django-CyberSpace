from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ChatMsgSendingForm
from .models import Chat


@login_required()
def chat_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if x := Chat.objects.filter(members__in=[request.user, user]):
        chat = x.first()
    else:
        chat = Chat.objects.create()
        chat.members.add(request.user)
        chat.members.add(user)
        chat.save()

    if request.method == "POST":
        form = ChatMsgSendingForm(request.POST)
        if form.is_valid():
            frm = form.save(commit=False)
            frm.chat = chat
            frm.sender = request.user
            frm.save()
            return redirect("chat:chat_detail", pk=pk)
    form = ChatMsgSendingForm()
    return render(request, 'chat/chat.html', {'chat': chat, 'form': form})


@login_required()
def chats_view(request):
    chats = Chat.objects.filter(members__in=[request.user])
    return render(request, "chat/chats.html", {'chats': chats})


@login_required()
def del_chat(request, pk):
    chat = get_object_or_404(Chat, pk=pk)
    chat.delete()
    return redirect("chat:chat_list")
