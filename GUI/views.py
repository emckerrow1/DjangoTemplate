# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden

from forms import ChangePasswordForm
from models import UserProfile


# Create your views here.
@login_required(login_url="login")
def home(request):
    return render(request,"home.html", {
        })

@login_required(login_url="login")
def profile(request, stix_id):
    try:
        user_profile = UserProfile.objects.get(stix_id=stix_id)
        user = User.objects.get(userprofile__stix_id=user_profile.stix_id)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()

    cpf = ChangePasswordForm(prefix='changepassword')
    if request.method == "POST":
        if "changepassword-password" in request.POST and "changepassword-password_repeat" in request.POST:
                cpf = ChangePasswordForm(request.POST, prefix='changepassword')
                if cpf.is_valid():
                    user = User.objects.get(pk=request.POST["change-password-user-id"])
                    user.set_password(request.POST["changepassword-password"])
                    user.save()
                else:
                    return render(request, "I3GUI/profile.html", {
                        "show_errors":True,
                        "user_profile":user,
                        "password_form":cpf,
                    })
    return render(request, "profile.html", {
            "user_profile":user,
            "password_form":cpf,
        })