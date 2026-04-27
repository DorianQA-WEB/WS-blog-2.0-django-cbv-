from django.urls import path

from .views import ProfileUpdateView, ProfileDetailView
from ..blog.urls import urlpatterns

urlpatterns = [
    path('user/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/<slug:slug>/', ProfileDetailView.as_view(), name='profile_detail')
]
