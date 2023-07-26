from django.shortcuts import render, reverse


def base(request):
    signup_url = reverse("account_signup")
    login_url = reverse("account_login")
    return render(
        request, "base/base.html", {"signup_url": signup_url, "login_url": login_url}
    )
