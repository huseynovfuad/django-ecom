from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()


def login_view(request):
    context = {}
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data.get("email"))
            login(request, user)
            return redirect("/")

    context["form"] = form
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


def register_view(request):
    context = {}
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get("password1"))
            new_user.save()

            login(request, new_user)
            return redirect("/")

    context["form"] = form
    return render(request, "accounts/register.html", context)