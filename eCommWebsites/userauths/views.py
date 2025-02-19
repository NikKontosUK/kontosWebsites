from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm

from django.contrib.auth import login,authenticate
from django.contrib import messages

# Create your views here.
def Register_view(request):
    if request.method == "POST":
        print(request.POST)  # Log the POST data
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            email = form.cleaned_data.get("username")
            messages.success(request, f"Hey {email}, your account was created successfully!")
            new_user = authenticate(email=form.cleaned_data["email"],
                                    password=form.cleaned_data["password1"])
            login(request, new_user)
            return redirect("core:index")
        else:
            print(form.errors)  # Log any form errors
    else:
        form = UserRegisterForm()

    context = {
        "form": form
    }

    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        