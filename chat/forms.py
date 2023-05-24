from django import forms
from .models import ChatMsg

classes = "form-control rounded"


class ChatMsgSendingForm(forms.ModelForm):
    class Meta:
        model = ChatMsg
        fields = ('content',)
        widgets = {'content': forms.Textarea(attrs={
            'placeholder': 'Enter your message...',
            'class': classes + "rounded-end-0",
            'style': 'resize:none; bottom:0;',
            'rows': '2'
        })}
