from django.urls import path, include
from . import views
from .feeds import LatestPostsFeed
from .views import CustomLoginView, register_view, prueba_logging
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import router as blog_api_router

app_name = 'blog'

urlpatterns = [
    # Post views
    path('list_post', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.posts_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('register/', register_view, name='register'),
    path('log-test/', prueba_logging),

    # Autenticación de usuarios
    path('', CustomLoginView.as_view(next_page='blog:post_list'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),


    # Rutas para restablecimiento de contraseña
    path('accounts/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += [
    path('perfil/', views.user_profile, name='user_profile'),
    path('api/', include(blog_api_router.urls)),
]
