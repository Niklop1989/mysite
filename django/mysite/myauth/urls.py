from django.urls import path
from .views import (login_view,
                    set_cookie_view,get_cookie_view,
                    set_session_view,get_session_view,
                    MyLogoutView,logout_view,MyLogoutPage,
                    AboutMeView,RegisterView,AvatarUpdateView,UserListView,
                    UserDetailViews,HelloView)
from django.contrib.auth.views import LoginView,LogoutView


app_name = "myauth"

urlpatterns = [
    # path("login/",login_view,name='login'),
    path(
        "login/",
        LoginView.as_view(
            template_name='myauth/login.html',
            redirect_authenticated_user=True
            ),
            name='login'),
    #path('logout/',logout_view,name='logout'),  
    path('logout/',MyLogoutPage.as_view(),name='logout'),  
    path("about_me/", AboutMeView.as_view(), name="about_me_url"),
    path('list_users/',UserListView.as_view(),name='list_users'),
    path('register/',RegisterView.as_view(),name='register_url'),
    path('user_details/<int:pk>/',UserDetailViews.as_view(),name='user_details'),
   
    path('avatar_update/<int:pk>/',AvatarUpdateView.as_view(),name='avatar_update'),

    path('hello/',HelloView.as_view(),name='hello'),


    path('cookie/get/',get_cookie_view,name='cookie-get'),
    path('cookie/set/',set_cookie_view,name='cookie-set'),
    path('session/get/',get_session_view,name='session-get'),
    path('session/set/',set_session_view,name='session-set'), 

]

