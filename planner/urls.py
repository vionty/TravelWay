from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),

    # Авторизация
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    # Восстановление пароля
    path(
        'password-reset/',
        views.password_reset,
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    # Поездки
    path(
        'trips/create/',
        views.trip_create,
        name='trip_create'
    ),

    path(
        'trips/<int:trip_id>/',
        views.trip_detail,
        name='trip_detail'
    ),

    path(
        'trips/<int:trip_id>/edit/',
        views.trip_edit,
        name='trip_edit'
    ),

    path(
        'trips/<int:trip_id>/delete/',
        views.trip_delete,
        name='trip_delete'
    ),

    # Направления
    path(
        'trips/<int:trip_id>/destinations/create/',
        views.destination_create,
        name='destination_create'
    ),

    path(
        'destinations/<int:destination_id>/edit/',
        views.destination_edit,
        name='destination_edit'
    ),

    path(
        'destinations/<int:destination_id>/delete/',
        views.destination_delete,
        name='destination_delete'
    ),

    # Места
    path(
        'destinations/<int:destination_id>/places/create/',
        views.place_create,
        name='place_create'
    ),

    path(
        'places/<int:place_id>/edit/',
        views.place_edit,
        name='place_edit'
    ),

    path(
        'places/<int:place_id>/delete/',
        views.place_delete,
        name='place_delete'
    ),

    path(
        'places/<int:place_id>/toggle-visited/',
        views.place_toggle_visited,
        name='place_toggle_visited'
    ),
]
