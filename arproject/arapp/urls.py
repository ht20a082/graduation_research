from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/ar_cam/', views.Ar_camViews, name="ar_cam"),
    path('video_feed/', views.video_feed_view(), name="video_feed"),
]

urlpatterns += staticfiles_urlpatterns()