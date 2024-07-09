from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:course_id>/enroll/success/', views.enroll_success, name='enroll_success'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('<int:course_id>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('get-lesson-video-url/', views.get_lesson_video_url, name='get_lesson_video_url'),
]