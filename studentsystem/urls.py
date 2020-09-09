from django.urls import path
from . import views

app_name = 'studentsystem'

urlpatterns = [
    path('register',views.registerForm,name='register'),
    path('schedule',views.schedule,name='schedule'),
    path('', views.login, name='login'),
    path('authenticate', views.authenticate,  name='authenticate'),
    path('menu', views.menu, name='menu'),
    path('viewcurrent', views.viewcurrent, name='viewcurrent'),
    path('details/<slug:course_id>', views.CourseDetails, name='details'),
    path('register/<slug:course_id>',views.registerDirect,name='registerDirect'),
    path('history', views.history, name='history'),
    path('showregistered', views.showregistered, name='showregistered')
]
