from django import forms
from django.contrib.auth import authenticate

from managers.models import Users


class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': ' Full Name', 'class': "form-control form-control-sm"}), max_length=55, required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': ' Last Name', 'class': "form-control form-control-sm"}), max_length=55, required=True)
    company = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': ' Company', 'class': "form-control form-control-sm"}), max_length=55, required=False)
    dob = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': "form-control form-control-sm"}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'password', 'class': "form-control form-control-sm"}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': ' Email',
                                                            'class': "form-control form-control-sm"}),
                             required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': ' Address', 'cols': 20, 'rows': 5,
                                                           'class': "form-control form-control-sm"}),
                              required=False)

    # mobile = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ' Mobile No  *',
    #                                                        'class': "form-control form-control-sm"}),
    #                          help_text='Must include international prefix - e.g. +1 555 555 55555')

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'dob', 'company', 'address', 'password', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = Users.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError('Email is already registered')
        return email


class UserFormLogin(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("user dose not exist")
            pwd = Users.objects.get(email=email)
            if not pwd.check_password(password):
                raise forms.ValidationError("invalid password")
            if not user.is_manager:
                raise forms.ValidationError("Not authorize to access!")
        return self.cleaned_data
