from django.urls import path

from apps.user.views import ProfileView, LoginView, RegisterView

app_name = 'user'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),

    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]
