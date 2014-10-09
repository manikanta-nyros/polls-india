from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MyRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super(MyRegistrationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.username
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.email:
            return instance.email
        else:
            return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'password2', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = 0

        if commit:
            user.save()

        return user


class PasswordResetForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['first_name'].widget.attrs['first_name'] = True
            self.fields['last_name'].widget.attrs['last_name'] = True

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.username
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.email:
            return instance.email
        else:
            return self.cleaned_data['email']

    def clean_first_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instace.pk:
            return instance.first_name
        else:
            return self.cleaned_data['first_name']

    def clean_last_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.last_name:
            return instance.last_name
        else:
            return self.cleaned_data['last_name']

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'password2', 'first_name', 'last_name')

    def save(self, commit=True):
        user = Super(MyRegistrationForm, self).save(commit=False)
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        if commit:
            user.save()
            return user
