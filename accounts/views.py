# from django.shortcuts import render, redirect
# from .models import User, Profile
# from django.contrib.auth import login, logout
#
# # Create your views here.
#
#
# def register_view(request):
#     context = {}
#
#     if request.method == "POST":
#         user = User.objects.create(
#             first_name=request.POST.get("name"),
#             last_name=request.POST.get("surname"),
#             username=request.POST.get("username"),
#         )
#         user.set_password(request.POST.get("password"))
#         user.is_superuser = True
#         user.save()
#
#         login(request, user)
#         return redirect("accounts:register")
#     return render(request, "accounts/register.html", context)
#
#
# def logout_view(request):
#     logout(request)
#     return redirect("accounts:register")