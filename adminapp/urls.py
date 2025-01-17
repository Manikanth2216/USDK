from django.urls import  path
from.import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.index,name='index'),
    path('registration',views.registration,name='registration'),
    path('login',views.login,name='login'),
    path('index',views.index,name='index'),
    path('about',views.about,name='about'),
    path('gallery',views.gallery,name='gallery'),
    path('codes',views.index,name='codes'),
    path('icons',views.index,name='icons'),
    path('admin',views.admin,name='admin'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('a_dashboard',views.a_dashboard,name='a_dashboard'),
    path('simple_upload',views.simple_upload,name='simple_upload'),
    path('view_menu',views.view_menu,name='view_menu'),
    path('edit_menu',views.edit_menu,name='edit_menu'),
    path('logout',views.logout,name='logout'),
    path('a_logout',views.a_logout,name='a_logout'),
    path('add_cart,<str:food_id>',views.add_cart,name='add_cart'),
    path('new_menu',views.new_menu,name='new_menu'),  
    path('myaccount/', views.myaccount, name='myaccount'),
    path('view_cart',views.view_cart,name='view_cart'),
    path('extra_menu',views.extra_menu,name='extra_menu'),
    path('sendfeedback',views.sendfeedback,name='sendfeedback'),
    path('remove_cart/<int:food_id>/', views.remove_cart, name='remove_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('banking_register', views.banking_register, name='banking_register'),
    path('check', views.check, name='check'),
    path('sucess', views.sucess, name='sucess'),
    path('view_orders', views.view_orders, name='view_orders'),
    path('view_feedback',views.view_feedback,name='view_feedback'),
    path('edit_sub_menu/<str:food_id>/',views.edit_sub_menu,name='edit_sub_menu'),
    path('del_sub_menu/<str:food_id>/',views.del_sub_menu,name='del_sub_menu'),
    path('update_order/<str:order_id>/',views.update_order,name='update_order'),
    path('order_status',views.order_status,name='order_status'),
    path('day_revenue',views.day_revenue,name='day_revenue'),
    path('edit_customer/<int:cust_id>/', views.edit_customer, name='edit_customer'),
    path('update_customer/', views.update_customer, name='update_customer'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
