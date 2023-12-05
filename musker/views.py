from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Ciphers
from django.contrib import messages
from .forms import CiphersForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


def home(request):
    if request.user.is_authenticated:
        form = CiphersForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                cipher = form.save(commit=False)
                cipher.user = request.user
                cipher.save()
                messages.success(request, ("Your Cipher has been heard!"))
                return redirect('home')

        ciphers = Ciphers.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"ciphers": ciphers, "form": form})
    else:
        ciphers = Ciphers.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"ciphers": ciphers})


# Create your views here.

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("You Must Be Logged In to View This Page..."))
        return redirect('home')


def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get the profile unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow User
        request.user.profile.follows.remove(profile)
        # Save our Profile
        request.user.profile.save()

        # Return Message
        messages.success(request, (f"You Have Successfully Unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You Must Be Logged In to View This Page..."))
        return redirect('home')


def follow(request, pk):
    if request.user.is_authenticated:
        # Get the profile unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow User
        request.user.profile.follows.add(profile)
        # Save our Profile
        request.user.profile.save()

        # Return Message
        messages.success(request, (f"You Have Successfully Followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You Must Be Logged In to View This Page..."))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        ciphers = Ciphers.objects.filter(user_id=pk).order_by("-created_at")

        # Post form logic
        if request.method == "POST":
            # Get the current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to either follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save()

        return render(request, "profile.html", {"profile": profile, "ciphers": ciphers})
    else:
        messages.success(request, ("You Must Be Logged In to View This Page..."))
        return redirect('home')


def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {"profiles": profiles})
        else:
            messages.success(request, ("That's not your profile page"))
            return redirect('home')
    else:
        messages.success(request, ("You Must Be Logged In to View This Page..."))
        return redirect('home')


def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {"profiles": profiles})
        else:
            messages.success(request, ("That's not your profile page"))
            return redirect('home')
    else:
        messages.success(request, ("You Must Be Logged In to View This Page..."))
        return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In! Go Ciphers"))
            return redirect('home')

        else:
            messages.success(request, ("There was an error logging in. Please try again...    "))
            return redirect('login')

    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out. Sorry!"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # second_name = form.cleaned_data['second_name']
            # email = form.cleaned_data['email']
            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered! Welcome!"))
            return redirect('home')

    return render(request, "register.html", {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            login(request, current_user)
            messages.success(request, ("Your Profile Has Been Updated!"))
            return redirect('home')

        return render(request, "update_user.html", {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, ("You Must Be Logged In To View That Page..."))
        return redirect('home')


def cipher_like(request, pk):
    if request.user.is_authenticated:
        cipher = get_object_or_404(Ciphers, id=pk)
        if cipher.likes.filter(id=request.user.id):
            cipher.likes.remove(request.user)
        else:
            cipher.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))


    else:
        messages.success(request, ("You Must Be Logged In To View That Page..."))
        return redirect('home')


def cipher_share(request, pk):
    cipher = get_object_or_404(Ciphers, id=pk)
    if cipher:
        return render(request, "share_cipher.html", {'cipher': cipher})

    else:
        messages.success(request, ("That Cipher Does Not Exist..."))
        return redirect('home')


def delete_cipher(request, pk):
    if request.user.is_authenticated:
        cipher = get_object_or_404(Ciphers, id=pk)
        # Check to see if you own cipher
        if request.user.username == cipher.user.username:
            # delete the cipher
            cipher.delete()
            messages.success(request, ("The Cipher has been deleted!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("You Don't Own That Cipher!"))
            return redirect('home')
    else:
        messages.success(request, ("Please log in to Continue..."))
        return redirect(request.META.get("HTTP_REFERER"))


def edit_cipher(request, pk):
    if request.user.is_authenticated:
        # Grab the Cipher!
        cipher = get_object_or_404(Ciphers, id=pk)
        # Check to see if you own the cipher
        if request.user.username == cipher.user.username:
            form = CiphersForm(request.POST or None, instance=cipher)
            if request.method == "POST":
                if form.is_valid():
                    cipher = form.save(commit=False)
                    cipher.user = request.user
                    cipher.save()
                    messages.success(request, ("Your Cipher has been heard!"))
                    return redirect('home')

            else:
                return render(request, "edit_cipher.html", {'form': form, 'cipher': cipher})

        else:
            messages.success(request, ("You Don't Own That Cipher!"))
            return redirect('home')
    else:
        messages.success(request, ("Please log in to Continue..."))
        return redirect('home')


def search(request):
    if request.method == "POST":
        search = request.POST['search']
        # Search the database
        searched = Ciphers.objects.filter(body__contains=search)
        return render(request, 'search.html', {'search': search, 'searched': searched})
    else:
        return render(request, 'search.html', {})


def search_user(request):
    if request.method == "POST":
        search = request.POST['search']
        # Search the database
        searched = User.objects.filter(username__contains=search)
        return render(request, 'search_user.html', {'search': search, 'searched': searched})
    else:
        return render(request, 'search_user.html', {})
