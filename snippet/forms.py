from django import forms
from .models import CustomUser, Snippet

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ["title", "language", "code"]
        widgets = {
            "code": forms.Textarea(attrs={"id": "code"}),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "image"]
