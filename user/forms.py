from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    # Add user fields (editable) to the form
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['address', 'contact', 'profile_pic']  # Include only profile fields

    def __init__(self, *args, **kwargs):
        # Get the current user from kwargs manually
        user = kwargs.pop('user', None)  # Use pop to remove user from kwargs if passed
        super().__init__(*args, **kwargs)

        if user:
            # Set initial values for User fields
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
