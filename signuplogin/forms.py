from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=254, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, 
                                help_text='Enter the same password as above, for verification.')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )

    def save(self, commit=True):
        user_manager = User.objects  # UserManager instance
        user = user_manager.create_user(
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=self.cleaned_data['password1']  # Assuming you want to use password1 for user creation.
        )
        return user