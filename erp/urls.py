from django.urls import path

from . import views 

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('dashboard', views.dashboard), 
    path('register', views.register),
    path('teacher', views.teacher),
    path('admin',views.admin),
    path('teacher-dashboard', views.teacher_dashboard),
    path('admin-dashboard', views.admin_dashboard),
    path('acceptUser',views.acceptUser),
    path('rejectUser',views.rejectUser),
    path('add-teacher', views.add_teacher),
    path('add-admin', views.add_admin),
    #path('accepted',views.accepted),
    path('removeTeacher',views.remove_teacher),
    path('deleteAdmin',views.delete_admin),
  
]