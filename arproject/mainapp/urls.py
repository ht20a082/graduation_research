from django.urls import path

from . import views

urlpatterns = [
    path('', views.Top_view.as_view(), name='top'),
    path('synthesized/', views.ListSynthesizedView.as_view(), name='synthesized-main'),
    path('image/', views.ListImageView.as_view(), name='image-main'),
]