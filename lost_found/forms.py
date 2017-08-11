from django import forms
from .models import Lost,Found


class LostForm(forms.ModelForm):
    class Meta:
        model = Lost
        fields = [
            "title",
            "content",
            "image",
        ]

class FoundForm(forms.ModelForm):
    class Meta:
        model = Found
        fields = [
            "title",
            "content",
            "image",
        ]