from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"type": "password"}))

    class Meta:
        model = User
        fields = ("email", "password")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control form-control-lg"})

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email doesn't exists")
        else:
            user = User.objects.get(email=email)

            if not user.is_active:
                raise forms.ValidationError("User is not activated")

            if not user.check_password(password):
                raise forms.ValidationError("Password or email are wrong")
        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    instagram_username = forms.CharField(label='Instagram Username')
    instagram_password = forms.CharField(label='Instagram Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean(self):
        email = self.cleaned_data.get("email")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not (password1 and password2 and password1 == password2):
            raise forms.ValidationError("Passwords don't match")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists")


        return self.cleaned_data
