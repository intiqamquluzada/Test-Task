from django import forms
from .models import Instagram


class InstagramAddForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"type": "password", "class": "form-control"}))
    class Meta:
        model = Instagram
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(InstagramAddForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": "form-control", "placeholder": "Istifadeci adiniz"})

