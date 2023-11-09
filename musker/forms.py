from django import forms
from .models import Ciphers

class CiphersForm(forms.ModelForm):
    body = forms.CharField(required=True,
                          widget=forms.widgets.Textarea(
                              attrs={
                                  "placeholder": "Post your Whisper....",
                                  "class": "form-control",
                                  "style": "background-color: #212529; color: white;"
                              }
                          ),
                          label="",
                          )

    class Meta:
        model = Ciphers
        exclude = ("user",)