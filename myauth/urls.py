from django.contrib.auth.views import LoginView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django import forms
from .views import (get_cookie_view,
                    set_cookie_view,
                    set_session_view,
                    get_session_view,
                    # logout_view,
                    MyLogoutView,
                    AboutMeView,
                    RegisterView,
                    # profile_edit,
                    FooBarView,
                    # login_view,
                    MyLoginView,
                    users_list,
                    UserDetailsView,
                    UserUpdateView,
                    HelloView,
                    )
app_name = 'myauth'

# class AboutMeView(forms.Form):
#     files = forms.ImageField(label='изображение')

urlpatterns = [
    # path('login/', login_view, name='login')
    path(
        'login/',
        LoginView.as_view(
            template_name='myauth/login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),

    path('hello/', HelloView.as_view(), name='hello'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('login', MyLoginView.as_view(), name='login'),
    path('list', users_list, name='users_list'),
    path('details/<pk>', UserDetailsView.as_view(), name='user_details'),
    path('edit/<pk>', UserUpdateView.as_view(), name='user_edit'),

    path('cookie/get/', get_cookie_view, name='cookie-get'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),

    path('session/set/', set_session_view, name='session-set'),
    path('session/get/', get_session_view, name='session-get'),

    path('foo-bar/', FooBarView.as_view(), name='foo-bar'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
