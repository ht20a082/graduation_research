from django.urls import path

from . import views

urlpatterns = [
    path('synthesized/', views.ListSynthesizedView.as_View(), name='synthesized-main'),
    path('image/', views.ListImageView.as_View(), name='image-main'),
]