from django.shortcuts import render, redirect
from .models import Profile, Ciphers
from django.contrib import messages
from .forms import CiphersForm

def home(request):
    if request.user.is_authenticated:
        form = CiphersForm(request.POST or None)
        if request.method=="POST":
            if form.is_valid():
                cipher = form.save(commit=False)
                cipher.user = request.user
                cipher.save()
                messages.success(request, ("Your whisper has been heard!"))
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
