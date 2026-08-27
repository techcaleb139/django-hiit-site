from projectapp import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path("profile/", views.profile, name='profile'),
    path('posts/', views.posts, name='posts'),
    path('posts/add/', views.add_post, name='add_post'),
    path('posts/<int:pk>/', views.post, name='post'),
    path('posts/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path("user/form/", views.user_form, name='user_form'),
    path("user/create", views.create_user, name='create_user'),
    path("user/create-custom/", views.customer_create_user, name='customer_create_user'),
    path("user/submit", views.submit_form, name='submit_form'),
    path('student/add/', views.add_student, name='add_student'),
    path('students/', views.students, name='students'),
    path('student/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('student/<int:pk>/delete/', views.delete_student, name='delete_student'),
]

