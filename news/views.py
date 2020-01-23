from django.shortcuts import render, get_object_or_404 #(for in case the category_id is changed or error occurs.. it is best practice to handle error)
from django.views import View # vanilla view
from django.views.generic import (TemplateView,
 DeleteView, 
 UpdateView,
 CreateView, 
 ListView,
 DetailView,
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy # for view we cqnnot only use reverse but reverse_lazy 
from django.utils.text import slugify

from news.forms import NewsCreateForm
from news.models import Category, News # to give datas from models


# Create your views here.

class CategoryNewsView(View): 
  def get(self, request, category_id, *args, **kwargs): #vanillas get method has been used
    template_name = "news/categories.html"
    # category = Category.objects.get(pk=category_id) 
    category = get_object_or_404(Category, pk=category_id) # best practice than above 
    category_news_list = News.objects.filter(category=category) #first category is from the news table or model news and another is the variable above
    return render(request, template_name, {"category_news_list": category_news_list, "category": category})

# class CategoryNewsView(ListView):
#   model = News
#   context_object_name = "category_news_list"
#   template_name = "news/categories.html"

#   # queryset = News.object.all()

#   def get_queryset(self): 
#     category_id = self.kwargs["category_id"]
#     category = get_object_or_404(Category, id = category_id)
#     return News.objects.filter(category=category)

class NewsTemplateView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        print(categories)
        category_news_list = {}
        for category in categories:
            # context[category.title] = News.objects.filter(category=category)
            category_news_list[category] = News.objects.filter(category=category)
        context["news_list"] = News.objects.all().order_by("-created_at")[:4]
        context["trending_news"] = News.objects.order_by("-count")
        context["category_news_list"] = category_news_list
        print(context)
        return context

class NewsDetail(DetailView): #basically for the the detail news when clicked the link
    model = News
    template_name = "news/single_news.html"
    context_object_name = "detail_news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.count = self.object.count + 1
        self.object.save()
        context["popular_news"] = News.objects.order_by("-count")[:4] # recently added news first
        return context

# defining the CREATE, UPDATE AND DELETE VIEW

class NewsCreateView(LoginRequiredMixin, CreateView): #the 1st param and 2nd param should be on order like this as it is on the basis of mro
    model = News
    template_name = "news/create.html"
    login_url = reverse_lazy("login") 
    success_url = reverse_lazy("home")
    form_class = NewsCreateForm # we are not creating objects so dont use () while calling class

    def form_valid(self, form): # this fn is built in fn and also the form param is the form that we get after POST i.e user fills the form
        news = form.save(commit=False)
        title = form.cleaned_data["title"]
        slug = slugify(title)
        news.slug = slug
        news.author = self.request.user
        news.save()
        
        return super().form_valid(form) 
 
    def form_invalid(self, form):
        return super().form_invalid(form)

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    template_name = "news/update.html"
    fields = "title", "content", "cover_image", "category"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("home")

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        return self.post(self, request, *args, **kwargs) # we are deleting the news via get request by returning post method