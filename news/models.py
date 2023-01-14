from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    """ Модель описывает Автора """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг автора')

    def __repr__(self):
        return f"Author (user.name='{self.user}', rating='{self.rating}')"

    def __str__(self):
        return f"{self.user}"

    def update_rating(self):
        """
            суммарный рейтинг каждой статьи автора умножается на 3;
            суммарный рейтинг всех комментариев автора;
            суммарный рейтинг всех комментариев к статьям автора.
        """
        posts_rating = self.posts.aggregate(result=Sum('rating')).get('result')
        comments_rating = self.user.comments.aggregate(result=Sum('rating')).get('result')
        print(f"===== {self.user}: обновляем рейтинг автора =====")
        print(f"Рейтинг постов = {posts_rating}")
        print(f"Рейтинг комментов = {comments_rating}")
        self.rating = 3 * posts_rating + comments_rating
        self.save()
        print(f"Рейтинг = 3 * {posts_rating} + {comments_rating} = {self.rating}")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Category(models.Model):
    """ Категории новостей / статей — темы, которые
        они отражают(спорт, политика, образование и т.д.).
        Здесь категории, то же что тэги. Их можно добавлять любое количество."""
    name = models.CharField(unique=True, max_length=128, verbose_name='Название категории')
    """ Подписаться на рассылку """
    subscribers = models.ManyToManyField(User, related_name='categories', verbose_name='Подписчики')

    def __repr__(self):
        return f"Category (name='{self.name}')"

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    """ Модель содержит в себе статьи и новости, которые создают пользователи.
        Каждый объект может иметь одну или несколько категорий. """
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOISES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')
    post_type = models.CharField(max_length=2, choices=CATEGORY_CHOISES, default=ARTICLE, verbose_name='Тип поста')
    category = models.ManyToManyField(Category, through="PostCategory", verbose_name='Категория поста')
    title = models.CharField(max_length=128, verbose_name='Название поста')
    text = models.TextField(verbose_name='Текст поста')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг поста')

    def __repr__(self):
        return f"Post (author.user.name='{self.author.user}', title='{self.title}', rating='{self.rating}'," \
               f"post_type='{self.post_type}')"

    def like(self):
        """ Увеличить на единицу значение 'Post.rating'. """
        self.rating += 1
        self.save()

    def dislike(self):
        """ Уменьшить на единицу значение 'Post.rating'. """
        self.rating -= 1
        self.save()

    def preview(self, length=124) -> str:
        """ Вернуть превью статьи. """
        return f"{self.text[:length]}..." if len(self.text) > length else self.text

    def __str__(self):
        """ Отображение названия поста и краткого текста поста """
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        """ Вернуть url, зарегистрированный для отображения одиночного товара """
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class PostCategory(models.Model):
    """ Промежуточная модель для связи «многие ко многим». """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.post.title} | {self.category.name}'

    class Meta:
        verbose_name = "Пост с категориями"
        verbose_name_plural = "Посты с категориями"


class Comment(models.Model):
    """ Под каждой новостью/статьёй можно оставлять комментарии. """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Текст комментария')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания комментария')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг комментария')

    def like(self):
        """ Увеличить на единицу значение 'Comment.rating'. """
        self.rating += 1
        self.save()

    def dislike(self):
        """ Уменьшить на единицу значение 'Comment.rating'. """
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'ID comment: {self.id}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
