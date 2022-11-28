from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from django.views import View
from .models import Image


class Top_view(TemplateView):
    template_name = 'mainapp/top.html'

class ListSynthesizedView(LoginRequiredMixin, TemplateView):
    template_name = 'mainapp/synthesized_list.html'

class ListImageView(LoginRequiredMixin, ListView):
    template_name = 'mainapp/image_list.html'
    model = Image

class CreateImageView(LoginRequiredMixin, CreateView):
    template_name = 'mainapp/image_create.html'
    model = Image
    fields = ('title', 'height', 'width', 'thumbnail')
    success_url = reverse_lazy('image-main')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

