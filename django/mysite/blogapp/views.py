from django.views.generic import ListView,DetailView
from .models import Article
from django.contrib.syndication.views import Feed
from django.urls import reverse,reverse_lazy

class ArticleListView(ListView):
    model = Article
    template_name = 'blogapp/article_list.html'
    # context_object_name = 'art'
    
    #queryset = Article.objects.select_related('author', 'category').prefetch_related('tags').defer('content')
    queryset = Article.objects.filter(
        pub_date__isnull=False).order_by("-pub_date")

class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'detail_article'



class LatestArticlesFeed(Feed):
    title = 'Blog articles(latest)'
    description =  "change atribute"
    link = reverse_lazy('blogapp:article_list_url')  


    def items(self):
        return (
             Article.objects.filter(
            pub_date__isnull=False).order_by("-pub_date")[:5]
        )
    def item_title(self, item:Article):
        return item.title

    def item_description(self, item:Article):
        return item.content[:200]
