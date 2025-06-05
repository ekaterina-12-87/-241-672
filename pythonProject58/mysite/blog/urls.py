from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
 # представления поста
 path('', views.home_view, name='home_view'),
 path('room/<int:room_id>/', views.room_detail, name='room_detail'),
path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),

    path('booking/', views.booking_list, name='booking_list'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/add/', views.booking_add, name='booking_add'),
    path('booking/<int:booking_id>/edit/', views.booking_edit, name='booking_edit'),
    path('booking/<int:booking_id>/delete/', views.booking_delete, name='booking_delete'),
]