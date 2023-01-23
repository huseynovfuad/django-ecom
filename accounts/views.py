from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from services.generator import Generator
from django.conf import settings
from django.contrib import messages

# Create your views here.
User = get_user_model()


def login_view(request):
    context = {}
    form = LoginForm()
    next = request.GET.get("next", None)

    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data.get("email"))
            login(request, user)
            if next:
                return redirect(next)
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
            new_user.is_active = False

            # send activation message
            activation_code = Generator.create_activation_code(size=6, model_=User)
            new_user.activation_code = activation_code
            new_user.save()

            subject = "Activation Message"
            message = f"CODE: {activation_code}"
            from_mail = settings.EMAIL_HOST_USER
            to_mail = [new_user.email]

            send_mail(
                subject, message, from_mail, to_mail, fail_silently=False
            )

            return redirect("accounts:activate", slug=new_user.slug)
        else:
            print(form.errors)

    context["form"] = form
    return render(request, "accounts/register.html", context)


def activate_user_view(request, slug):
    context = {}
    user = get_object_or_404(User, slug=slug)

    if request.method == "POST":
        code = request.POST.get("code", None)

        if code == user.activation_code:
            user.is_active = True
            user.activation_code = None
            user.save()

            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Kod yalnisdir")
            return redirect("accounts:activate", slug=slug)

    return render(request, "accounts/activate.html", context)