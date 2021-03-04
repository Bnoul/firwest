from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView
from .views import LoginView, RegisterView, ProfilePage

app_name = "myapp"
urlpatterns = [
    # например: /myapp/
    path('', views.index, name='index'),
    # например: /myapp/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # например: /myapp/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # например: /myapp/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('', views.index, name="home"),
    path('create/', views.create),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete),
    path('login/', LoginView.as_view(), name='Login'),
    path('account/register/', RegisterView.as_view(), name="register"),
    path('accounts/login/', LoginView.as_view(), name='loginAccount'),
    path('accounts/profile/', ProfilePage.as_view(), name='profile'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change')
]
