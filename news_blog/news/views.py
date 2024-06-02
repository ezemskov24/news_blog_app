from typing import Dict, Any

from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from .models import News, Tag, NewsViewCount, UserLike


class IndexView(ListView):
    """
    Представление списка новостей на главной странице.
    """
    model = News
    template_name = 'index.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        """
        Получение списка неархивированных новостей,
        с сортировкой по дате создания в порядке убывания.
        """
        return News.objects.filter(archived=False).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запросы.
        Если запрос является AJAX-запросом, возвращает JSON-ответ
        с отрендеренным HTML-кодом новостей и информацией о наличии следующей страницы.
        """
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            news_list = self.get_queryset()
            paginator = Paginator(news_list, self.paginate_by)
            page_number = request.GET.get('page')

            try:
                news_page = paginator.page(page_number)
            except PageNotAnInteger:
                news_page = paginator.page(1)
            except EmptyPage:
                news_page = []

            context = {'news': news_page.object_list}
            news_html = render_to_string(self.template_name, context, request=request)

            has_next = news_page.has_next()

            return JsonResponse({
                'news_html': news_html,
                'has_next': has_next
            })

        return super().get(request, *args, **kwargs)


class NewsDetailView(DetailView):
    """
    View детальной страницы новости
    """
    model = News
    template_name = 'news-details.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Метод для получения контекстных данных, передаваемых в шаблон.
        """
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        context['item_id'] = item.pk
        return context

    def get_object(self, queryset=None):
        """
        Получает объект новости. Подсчитывает количество просмотров и обновляет его в БД.
        """
        obj = super().get_object(queryset=queryset)

        viewed = self.request.session.get('viewed_news', [])
        if obj.pk not in viewed:
            viewed.append(obj.pk)
            self.request.session['viewed_news'] = viewed

            news_view_count = NewsViewCount.objects.get_or_create(news=obj)[0]
            news_view_count.views += 1
            news_view_count.save()

        return obj


class NewsByTagListView(ListView):
    """
    View списка новостей по тегу
    """
    model = News
    template_name = 'news_by_tag.html'
    context_object_name = 'news'

    def get_queryset(self):
        """
        Получение списка новостей, отфильтрованных по заданному тегу.
        """
        tag_name = self.kwargs.get('tag')
        tag = get_object_or_404(Tag, name=tag_name)
        return News.objects.filter(tags=tag)

    def get_context_data(self, **kwargs):
        """
        Получение контекстных данных для передачи в шаблон, включая текущий тег.
        """
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag')
        return context


class NewsStatisticsView(TemplateView):
    """
    View статистики просмотров новостей.
    """
    template_name = 'news_statistics.html'

    def get_context_data(self, **kwargs):
        """
        Получение контекстных данных для передачи в шаблон, включая статистику просмотров.
        """
        context = super().get_context_data(**kwargs)
        context['news_statistics'] = NewsViewCount.objects.all()
        return context


class LikeNewsView(View):
    """
    View для установки лайка на новость.
    """
    def post(self, request, pk):
        """
        Обрабатывает POST-запрос для установки лайка на новость.
        """
        news = get_object_or_404(News, pk=pk)
        user = request.user

        like_obj, created = UserLike.objects.get_or_create(user=user, news=news, defaults={'like': True})

        if created:
            news.likes += 1
            news.save()

        return JsonResponse({"likes": news.likes})


class DislikeNewsView(View):
    """
    View для установки дизлайка на новость.
    """
    def post(self, request, pk):
        """
        Обрабатывает POST-запрос для установки дизлайка на новость.
        """
        news = get_object_or_404(News, pk=pk)
        user = request.user

        like_obj, created = UserLike.objects.get_or_create(user=user, news=news, defaults={'like': False})

        if created:
            news.likes -= 1
            news.save()

        return JsonResponse({"likes": news.likes})
