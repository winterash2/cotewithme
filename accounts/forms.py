from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CreateUserForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    first_name = forms.Textarea()
    last_name = forms.Textarea()

    class Meta:
        model = User
        fields = ("username", "last_name", "first_name", "email", "password1", "password2")

        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'text_input'}),
        #     'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'text_input'}),
        #     'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'text_input'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

