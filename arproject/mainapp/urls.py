from django.urls import path

from . import views

urlpatterns = [
    path('', views.Top_view.as_view(), name='top'),
    path('image/', views.ListImageView.as_view(), name='image-main'),
    path('image/create/', views.CreateImageView.as_view(), name='image-create'),
    path('image/detail/<int:pk>/', views.DetailImageView.as_view(), name='image-detail'),
]