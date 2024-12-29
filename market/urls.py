from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import PasswordChangeDoneView,PasswordChangeView


urlpatterns=[
    #path("",RedirectView.as_view(url=('/index/'))),
    path('origin',views.supervisor_page,name="dash"),
    path("Add/",views.AddUser,name="add"),
    path("Edit",views.EditUser,name="edit"),
    path("Delete",views.DeleteUser,name="delete"),
    path("View",views.ViewUser,name="view"),
    path("Edit-success",views.edit_success,name="lounge"),
    path("home",views.customer_page,name="home"),
    path("",views.mirror,name="start"),
    path("users",views.signin,name="login"),
    path("register",views.signup,name="register"),
    path("registeration-success",views.creation_success,name="signup-complete"),
    path("registeration-error",views.creation_failure,name="signup-error"),
    path("change-details",PasswordChangeView.as_view(template_name="pasguru.html",
                                                     success_url="change-details-success"),name="password_change"),
    path("change-details-success",auth_views.PasswordChangeDoneView.as_view(template_name="success_page.html"),name="password_change_done"),
    path("order-room",views.room_service,name="accomodation"),
    path("order-room-not-checked-out",views.room_unavailable,name="try_another"),
    path("order-room-success",views.room_service_success,name="book_room_success"),
    path("order-food",views.food_service,name="dishes"),
    path("order-food-success",views.food_service_success,name="dish_success"),
    path("renew-session",views.user_logout,name="logout"),
    
]