from django import forms
from .models import Profile , Comment , Blog
from django.contrib.auth.models import User 
 
class ProfileForm(forms.ModelForm):
    # Add the user model fields that are editable for the Profile form
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['address', 'contact', 'profile_pic']  # Include the profile fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Use pop to remove user from kwargs if passed
        super().__init__(*args, **kwargs)

        # Define custom labels for each field
        labels = {
            'username': 'Enter your username',
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'email': 'Enter your email address',
            'address': 'Enter your address',
            'contact': 'Enter your contact number',
            'profile_pic': 'Upload your profile picture'
        }

        # define custom widgets for placeholder, class, etc.
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'aria-label': 'First Name'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'aria-label': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'aria-label': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'aria-label': 'Email'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Address',
                'aria-label': 'Address'
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Number',
                'aria-label': 'Contact'
            }),
            'profile_pic': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'aria-label': 'Profile Picture'
            })
        }

        # apply the custom labels and widgets to the form fields
        for field_name, label in labels.items():
            if field_name in self.fields:
                self.fields[field_name].label = label

        for field_name, widget in widgets.items():
            if field_name in self.fields:
                self.fields[field_name].widget = widget

        # Set initial values for the User fields
        if user:
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'image']  # Include the required fields

    # Customizing the form widgets and labels
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Blog Title'}),
        'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Blog Content'}),
        'category': forms.Select(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
    }

    labels = {
        'title': 'Blog Title',
        'content': 'Content',
        'category': 'Category',
        'image': 'Blog Image',
    }

    # Optionally, you can add additional validation or cleaning methods here
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters.")
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here...'})
        }