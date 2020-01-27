from django.urls import path
from news import views

urlpatterns = [
    path("create/", views.NewsCreateView.as_view(), name="create_news"), # the path should also in order as static should be first and then dynamic
    path("update/<pk>", views.NewsUpdateView.as_view(), name="update_news"),
    path("delete/<pk>", views.NewsDeleteView.as_view(), name="delete_news"),
    path("<category_id>/", views.CategoryNewsView.as_view(), name="category_news" ), # target header.html url link
    path("<pk>/<slug>/", views.NewsDetail.as_view(), name="single_news"),
    path("<pk>/<slug>/feedback/", views.news_feedback, name="feedback_news"),
]
# Class-based views should be written like this... 
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')