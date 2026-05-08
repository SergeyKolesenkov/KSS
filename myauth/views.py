from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import request
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from django.views import View
from .models import Profile
from django.utils.translation import gettext_lazy as _, ngettext


class HelloView(View):
    welcome_message = _('Hello world!')
    def get(self, request: HttpRequest) -> HttpResponse :
        items_str = request.GET.get('items') or 0
        items = int(items_str)
        products_line = ngettext(
            'one product',
            '{count} products',
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f'<h1>{self.welcome_message}</h1>'
            f'\n<h2>{products_line}</h2>'
        )


class AboutMeView(UpdateView):
    template_name = 'myauth/about-me.html'
    model = Profile
    fields = ('avatar',)
    success_url = reverse_lazy('myauth:about-me')

    # def get_object(self, queryset=None):
    #     return get_object_or_404(User, username=self.kwargs['username'])

    def get_object(self, queryset=None):
        # username = self.kwargs.get('username')
        return self.request.user.profile if self.request.user.is_authenticated else None
        # if username is not None:
        #     queryset = self.get_queryset()
        #     return queryset.filter(user__username=username)

class MyLoginView(LoginView):
    next_page = reverse_lazy('myauth:about-me')


        # def profile_edit(request):
    #     if request.method == 'POST':
    #         form = ProfileForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save()
    #             return reverse_lazy('myauth:about-me')
    #         else:
    #             form = ProfileForm()
    #         return render(request, 'about-me.html', {'form':form})


# class AboutMeView(TemplateView):
#     template_name = 'myauth/about-me.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response

# def login_view(request: HttpRequest) -> HttpResponse:
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             return redirect('/admin/')
#
#         return render(request, 'myauth/login.html')
#
#     username = request.POST['username']
#     password = request.POST['password']
#
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect('/admin/')
#
#     return render(request, 'myauth/login.html', {'error': 'Invalid login credentials'})

# def logout_view(request: HttpRequest):
#     logout(request)
#     return redirect(reverse('myauth:login'))

class MyLogoutView(LogoutView):
    success_url = 'myauth:login'

    def get_success_url(self):
        return reverse_lazy(self.success_url)

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r}')

@permission_required('myauth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')

class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})

@permission_required('admins')
def users_list(request):
    users_list = Profile.objects.all()

    context = {
        "users_list": users_list,
        }
    return render(request, 'myauth/users_list.html', context)

class UserDetailsView(DetailView):
    template_name = 'myauth/user_details.html'
    model = Profile
    fields = ('avatar')
    success_url = reverse_lazy('myauth:user_details')

    # def test_func(self):
    #     profile = self.get_object()
    #     return profile.user == self.request.user
    # def get_object(self, queryset=None):

class UserUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'myauth/user_edit.html'
    model = Profile
    fields = ('avatar',)
    # success_url = reverse_lazy('myauth:user_edit')

    def test_func(self):
        profile = self.get_object()
        return profile.user == self.request.user or self.request.user.is_staff

    def get_success_url(self):
        profile = self.get_object()
        return reverse(
            'myauth:user_details',
            kwargs={'pk':profile.pk},
        )
