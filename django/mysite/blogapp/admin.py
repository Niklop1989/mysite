from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from .models import Article,Category,Tag,Author



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    
    #list_display = "pk",'name','price','discount','description'
    list_display = "pk",'title',"content","pub_date"


@admin.register(Category)
class ArticleAdmin(admin.ModelAdmin):
    
    #list_display = "pk",'name','price','discount','description'
    list_display = "name",

@admin.register(Tag)
class ArticleAdmin(admin.ModelAdmin):
    
    #list_display = "pk",'name','price','discount','description'
    list_display = "name",

@admin.register(Author)
class ArticleAdmin(admin.ModelAdmin):
    
    #list_display = "pk",'name','price','discount','description'
    list_display = "name","bio"
                