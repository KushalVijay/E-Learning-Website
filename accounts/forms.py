from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from .models import login_page
User = get_user_model()

class LoginForm(forms.Form):
    class Meta:
        model = login_page
        fields = "__all__"

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:

            raise forms.ValidationError("Invalid credentials")
        login(request, user)
        self.user = user
        return data




class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    student = forms.BooleanField(label='Student',widget=forms.CheckboxInput,required=False)
    teacher = forms.BooleanField(label='Teacher',widget=forms.CheckboxInput,required=False)

    class Meta:
        model = User
        fields = ['username','email']

    def clean_username(self):

        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

