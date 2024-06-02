from django.urls import path

from .views import NewsDetailView, NewsByTagListView, NewsStatisticsView, LikeNewsView, DislikeNewsView
from .api_views import NewsListAPIView, NewsCreateAPIView, NewsDeleteAPIView


app_name = 'news'

urlpatterns = [
    path('<int:pk>/', NewsDetailView.as_view(), name='news_details'),
    path('<int:pk>/like/', LikeNewsView.as_view(), name='like_news'),
    path('<int:pk>/dislike/', DislikeNewsView.as_view(), name='dislike_news'),
    path('tag/<str:tag>/', NewsByTagListView.as_view(), name='news_by_tag'),
    path('statistics/', NewsStatisticsView.as_view(), name='news_statistics'),
    path('api/news/', NewsListAPIView.as_view(), name='news-list'),
    path('api/news/create/', NewsCreateAPIView.as_view(), name='news-create'),
    path('api/news/<int:pk>/delete/', NewsDeleteAPIView.as_view(), name='news-delete'),
]
