from django.shortcuts import render
from django.views.generic import TemplateView


def custom_403_csrf(request, reason=""):
    return render(request, "pages/403_csrf.html", status=403)


def custom_404(request, exception):
    return render(request, "pages/404.html", status=404)


def custom_500(request):
    return render(request, "pages/500.html", status=500)


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'
