from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
import news
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views import View


class PostsList(ListView):
    """ Представление всех постов в виде списка. """
    paginate_by = 3
    model = Post
    ordering = '-date_time'
    template_name = 'posts_list.html'
    context_object_name = 'posts'


class SearchPosts(ListView):
    """ Представление всех постов в виде списка. """
    paginate_by = 3
    model = Post
    ordering = '-date_time'
    template_name = 'post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """ Переопределяем функцию получения списка статей. """
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs) -> dict:
        """ Метод get_context_data позволяет изменить набор данных, который будет передан в шаблон. """
        context = super().get_context_data(**kwargs)
        context['search_filter'] = self.filterset
        return context


class PostDetail(DetailView):
    """ Представление отдельного поста. """
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    """ Представление для создания статьи. """
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить статью"
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = "AR"
        post.author = Author.objects.get(user=str(self.request.user.id))
        post.save()
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    """ Представление для редактирования статьи. """
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать статью"
        return context

    # def dispatch(self, request, *args, **kwargs):
    #     obj = self.get_object()
    #     if obj.user != self.request.user:
    #         raise Http404("Вам не разрешено редактировать этот пост")
    #     return super(ArticleUpdate, self).dispatch(request, *args, **kwargs)


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    """ Представление для удаления статьи. """
    raise_exception = True
    model = Post
    queryset = Post.objects.all()
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = ('news.delete_post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить статью"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    """ Представление для создания новости. """
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = "NW"
        post.author = Author.objects.get(user=str(self.request.user.id))
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить новость"
        return context


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    """ Представление для редактирования новости. """
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать новость"
        return context

    # def dispatch(self, request, *args, **kwargs):
    #     obj = self.get_object()
    #     if obj.user != self.request.user:
    #         raise Http404("Вам не разрешено редактировать этот пост")
    #     return super(NewsUpdate, self).dispatch(request, *args, **kwargs)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    """ Представление для удаления новости. """
    raise_exception = True
    model = Post
    queryset = Post.objects.all()
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = ('news.delete_post',)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить новость"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context


class CategoriesView(ListView):
    model = Post
    template_name = 'post_categories_view.html'
    context_object_name = "categories_list"
    paginate_by = 3

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


class CategoryListView(ListView):
    # paginate_by = 3
    model = Category
    template_name = 'post_categories_list_view.html'
    context_object_name = "categories_list"


@login_required
def add_me_to_category(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей категории'
    # return redirect('categories_list', category)
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def delete_me_to_category(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(user)
    message = 'Вы успешно отписались от новостей категории'
    # return redirect('categories_list', category)
    return render(request, 'unsubscribe.html', {'category': category, 'message': message})


class Search(ListView):
    """Поиск"""
    paginate_by = 3
    model = Post
    context_object_name = 'posts'
    template_name = 'posts_list.html'

    def get_queryset(self):
        return Post.objects.filter(
            text__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

