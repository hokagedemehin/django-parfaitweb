from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('store-details/', views.storeDetails, name='store-details'),
    path('update-item/', views.updateItem, name="update-item"),
    path('process-order/', views.processOrder, name='process-order'),
    path('send-email/', views.sendEmail, name='send-email'),
    path('store-parfait/<slug:slugProduct>/', views.storeParfait, name='store-parfait'),
    path('parfaits/', views.parfaitDetails, name='parfait'),
    path('parfait-update/<slug:slugProduct>/', views.ParfaitUpdate, name='parfait-update'),
    path('parfait-delete/<slug:slugProduct>/', views.ParfaitDelete, name='parfait-delete'),
    path('orders/', views.orderDetails, name='orderslist'),
    path('customer/<slug:slugCustomer>', views.customerDetails, name='customers'),
    path('parfaits/create/', views.parfaitCreate, name='parfait-create'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('user/', views.userPage, name='user-page'),
    path('not_user/', views.notUserPage, name='not-user'),
    path('staff-register/', views.StaffPage, name='create-staff'),
    path('profile/', views.ProfilePage, name='profile'),
    path('reset_password/', 
    auth_views.PasswordResetView.as_view(
        template_name='drinks/password_reset.html'), name="password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='drinks/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='drinks/password_reset_form.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='drinks/password_reset_done.html'), name="password_reset_complete"),

]