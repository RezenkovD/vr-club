from django.shortcuts import render

from django.http import HttpResponse, Http404, HttpResponseRedirect

from .models import Shortener


from .forms import ShortenerForm


def home_view(request):
    template = "shortener/home.html"
    context = {"form": ShortenerForm()}
    if request.method == "GET":
        return render(request, template, context)
    elif request.method == "POST":
        used_form = ShortenerForm(request.POST)
        if used_form.is_valid():
            long_url = used_form.cleaned_data.get("long_url")
            try:
                shortener = Shortener.objects.get(long_url=long_url)
                short_url = request.build_absolute_uri() + shortener.short_url
                context["new_url"] = short_url
                context["long_url"] = long_url
            except Shortener.DoesNotExist:
                shortened_object = used_form.save()
                new_url = request.build_absolute_uri() + shortened_object.short_url
                long_url = shortened_object.long_url
                context["new_url"] = new_url
                context["long_url"] = long_url
            return render(request, template, context)
        context["errors"] = used_form.errors
        return render(request, template, context)


def redirect_url_view(request, shortened_part):
    try:
        shortener = Shortener.objects.get(short_url=shortened_part)
        shortener.times_followed += 1
        shortener.save()
        return HttpResponseRedirect(shortener.long_url)
    except:
        raise Http404("Sorry this link is broken :(")
