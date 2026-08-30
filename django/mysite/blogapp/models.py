from django.db import models
from django.urls import reverse,reverse_lazy


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True,blank=True)
    pub_date = models.DateTimeField(null=True,blank=True,) #auto_now_add=True
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self,):
        return reverse('blogapp:article_detail_url',kwargs={'pk':self.pk})
    

