from django.contrib import admin
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating',)
    list_display_links = ('id', 'user', 'rating')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    list_filter = ('name', 'subscribers',)
    save_as = True


class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', '__str__', 'post_type', 'author', 'date_time', 'rating',)
    list_display_links = ('id', 'title',)
    list_filter = ('post_type',)
    search_fields = ('title',)
    inlines = [CommentInlineAdmin]
    save_on_top = True
    save_as = True
    list_editable = ('post_type',)
    form = PostAdminForm


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'category',)
    list_display_links = ('id', 'post',)


@admin.register(Comment)
class CommentAdminInline(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'date_time', 'rating')
    list_display_links = ('id', 'post',)
