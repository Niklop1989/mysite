from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views import View
from django.views.generic import TemplateView,CreateView,UpdateView,ListView,DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import (login_required,permission_required,
                                            user_passes_test)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy,ngettext
from .models import Profile
from .forms import ProfileForm



class HelloView(View):
    welcome_massage = _("welcome hello world")

    def get(self,request:HttpRequest) ->HttpResponse:
        items_string = request.GET.get('items') or 0
        items = int(items_string)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.welcome_massage}</h1>"
            f"\n<h2>{products_line}</h2>"
        )




class UserListView(ListView):
    template_name = "myauth/list_users.html"
    context_object_name = 'list_users'
    queryset = User.objects.all()

class UserDetailViews(DetailView):
    template_name = "myauth/user_details.html"
    queryset = User.objects.select_related('profile')
    context_object_name = 'user_details'
    

class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'

class AvatarUpdateView(UserPassesTestMixin,UpdateView):
    model = Profile

    template_name = "myauth/avatar_update.html"
    form_class = ProfileForm

    def test_func(self):
        print(self.request.user)
        print(self.request.user.is_staff)
        if self.request.user.is_staff:
            return True
        self.object = self.get_object()
        if self.request.user.pk == self.object.user.pk:
            return True
        return False
    def get_object(self, queryset = None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        user = User.objects.select_related('profile').get(pk=pk)
        try:
            return user.profile
        except Profile.DoesNotExist:
            return Profile.objects.create(user=user)

    def get_success_url(self):
        return reverse("myauth:about_me_url")


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about_me_url')

    # для того чтобы переходить в about-me
    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request,
                            username=username,
                            password=password)
        login(request=self.request,user=user)
        return response

def login_view(request:HttpRequest) ->HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request,'myauth/login.html')
    
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return redirect("/admin/")

    return render(request,"myauth/login.html",context={'error':"invalid login error"})


def logout_view(request:HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))

class MyLogoutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('myauth:login')
    
class MyLogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('myauth:login')

@user_passes_test(lambda u:u.is_superuser)
def set_cookie_view(request:HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz','buzz',max_age=3600)
    return response

from random import random
from django.views.decorators.cache import cache_page
# для чтения cookie
@cache_page(60*2)
def get_cookie_view(reques:HttpRequest) -> HttpResponse:
    value = reques.COOKIES.get('fizz','default_value')
    return HttpResponse(f"Cookie value: {value!r} + {random()}")


# для middleware
@permission_required('myauth.view_profile',raise_exception=True)
def set_session_view(request:HttpRequest)->HttpResponse:
    request.session["foobar"]='spameggs'
    return HttpResponse('Session set')

@login_required
def get_session_view(request:HttpRequest) ->HttpResponse:
    value = request.session.get('foobar','default')
    return HttpResponse(f'Session value: {value!r}')
