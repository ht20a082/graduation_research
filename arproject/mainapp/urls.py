from django.urls import path

from . import views

urlpatterns = [
    path('synthesized/', views.ListSynthesizedView.as_View()),
    path('image/', views.ListImageView.as_View()),
]