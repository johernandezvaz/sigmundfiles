from django.urls import path
from accounts.views import auth, profile

urlpatterns = [
    path('login/', auth.LoginView.as_view(), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    path('register/', auth.RegisterView.as_view(), name='register'),
    path('profile/', profile.ProfileView.as_view(), name='profile'),
    path('profile/edit/', profile.ProfileEditView.as_view(), name='profile_edit'),
    path('', profile.DashboardView.as_view(), name='dashboard'),
]