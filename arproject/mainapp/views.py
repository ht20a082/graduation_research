from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views import View


class Top_view(TemplateView):
    template_name = 'mainapp/top.html'

class ListSynthesizedView(TemplateView):
    template_name = 'mainapp/synthesized_list.html'

class ListImageView(TemplateView):
    template_name = 'mainapp/image_list.html'
