from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path("update/<int:todo_id>", views.update_todo, name="update_todo"),
    path("complete/<int:todo_id>", views.complete_todo, name="complete_todo"),
    path("delete/<int:todo_id>", views.delete_todo, name="delete_todo")
]
