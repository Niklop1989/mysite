from django.urls import path
from .views import ArticleListView,ArticleDetailView,LatestArticlesFeed

app_name = 'blogapp'

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list_url'),
    path('articles/<int:pk>/',ArticleDetailView.as_view(),name="article_detail_url"),
    path('articles/latest/feed/',LatestArticlesFeed(),name='article_feed_urls')
]