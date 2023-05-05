from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import register
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]
