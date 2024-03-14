from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from userauth.models import User
from userauth.forms import UserRegisterForm, UserProfileForm


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the form if it's valid
            form.save()
            # Authenticate user
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request,
                    f"Hey {user.username}, your account was created successfully.",
                )
                return redirect("home:home")
            else:
                messages.error(request, "Failed to authenticate. Please try again.")
        else:
            # If the form is invalid, handle the error
            messages.error(request, "Form submission error. Please check your inputs.")
    else:
        form = UserRegisterForm()

    context = {"form": form}  # Pass the form object to the template context
    return render(request, "userauth/register.html", context)


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:  # if there is a user
                login(request, user)
                messages.success(request, "You are logged.")
                return redirect("home:home")
            else:
                messages.warning(request, "Username or password does not exist")
                return redirect("userauth:sign-in")
        except:
            messages.warning(request, "User does not exist")

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return redirect("home:home")

    return render(request, "userauth/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("userauth:login")





@login_required
def profile_view(request):
    user = request.user
    
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userauth:profile')  # Redirect to the profile page after successful update
    else:
        form = UserProfileForm(instance=user)  # Populate form with user's current data
    
    context = {
        'form': form,
        'user': user,
    }
    return render(request, "userauth/profile.html", context)

