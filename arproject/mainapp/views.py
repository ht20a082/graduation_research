from django.shortcuts import render
from django.views.generic import ListView


class ListSynthesizedView(ListView):
    template_name = 'mainapp/synthesized_list.html'

class ListImageView(ListView):
    template_name = 'mainapp/image_list.html'
