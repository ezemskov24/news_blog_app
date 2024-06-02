from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse


class Tag(models.Model):
    """
    Модель тега новостей.

    name - Наименование тега;
    """
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news:news_by_tag', args=[self.name])


class News(models.Model):
    """
    Модель новости.

    title - Заголовок новости;
    text - Текст новости;
    image - Изображение новости;
    created_at - Дата и время создания новости;
    archived - Флаг, указывающий на то, что новость в архиве;
    tags - Связанные теги новости;
    likes - Количество лайков новости;
    """
    title = models.CharField(max_length=200, null=False, blank=False)
    text = models.TextField(blank=False)
    image = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        Tag,
        related_name='news',
        blank=True
    )
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('news:news_details', args=[self.pk])

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title


class NewsViewCount(models.Model):
    """
    Модель для отслеживания количества просмотров новостей.

    news - Ссылка на новость;
    views - Количество просмотров новости;
    """
    news = models.OneToOneField(News, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.news.title} - {self.views} views"


class UserLike(models.Model):
    """
    Модель для отслеживания лайков пользователей к новостям.

    user - Пользователь, который поставил лайк;
    news - Новость, которой поставлен лайк;
    like - Флаг, указывающий на то, что это лайк (True) или дизлайк (False);
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    like = models.BooleanField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'news'], name='unique_like')
        ]

