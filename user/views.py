from django.shortcuts import render , redirect
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "user/index.html")


@login_required
def user_profile(request):
    user = request.user  # get the login user
    profile, created = Profile.objects.get_or_create(user=user)  #get or create a user profile

    if request.method == 'POST':
        # Pass the user to the form
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            # Save the user-specific fields first
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Save the profile fields
            form.save()

            return redirect('/')  # Redirect to the same page after saving

    else:
        # Pass the user to pre-fill form
        form = ProfileForm(instance=profile, user=user)

    return render(request, "user/pages/user_profile.html", {
        "form": form,  # The form with both user and profile fields
        "user": user,  # Pass the user data to the template
    })




