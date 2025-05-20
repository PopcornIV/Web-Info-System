from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-page/', views.admin_view, name='admin'),
    path('manager/', views.manager_view, name='manager'),
    path('menu/', views.menu_view, name='menu'),
    path('orders/', views.orders_view, name='orders'),
    path('qr/', views.qr_view, name='qr'),
    path('staff/', views.staff_view, name='staff'),
    path('signup/', views.signup_view, name='signup'),
    path('submit-order/', views.submit_order_view, name='submit_order'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('update-order/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),

]
