from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from news.models import Author
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from django.views.generic.detail import DetailView


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('account_login')
    template_name = 'account/signup.html'
    success_message = "Ваш профиль создан"


class AccountUserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account_update_user.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Авторы').exists()
        context['is_your_id'] = int(self.request.user.id)
        context['path'] = int(self.request.path.split('/')[-1])
        return context


@login_required
def set_me_author(request):
    user = request.user
    common_users = Group.objects.get(name="Авторы")
    if not request.user.groups.filter(name="Авторы").exists():
        common_users.user_set.add(user)
        Author.objects.create(user=user)

    return redirect('/news/')


