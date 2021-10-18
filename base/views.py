from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

class IndexView(TemplateView):
    template_name="base/index.html"


class Home(TemplateView):
    template_name="base/home.html"
    