from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.views import View
from .models import Image


class Top_view(TemplateView):
    template_name = 'mainapp/top.html'

class ListSynthesizedView(TemplateView):
    template_name = 'mainapp/synthesized_list.html'

class ListImageView(TemplateView):
    template_name = 'mainapp/image_list.html'
    model = Image

class CreateImageView(CreateView):
    template_name = 'mainapp/image_create.html"
    model = Image

