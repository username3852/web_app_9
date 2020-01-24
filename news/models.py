from django.db import models
from django.contrib.auth.models import User # for author we have this model class named User
from django.urls import reverse
from django.conf import settings

# Django-ORM (Object Relational Mapping)
# the db use the same prefix of  the application name

class Category(models.Model): #for many to many reln and making the category dynamic and best approach then below practice in category
  title = models.CharField(max_length=30)

  class Meta: # this is for verbose in Catoegry class and no need to perform makemigrations for Meta
    verbose_name_plural = "Categories"

  def __str__(self): # it will prints title instead of object1, object2 inside the categories
    return self.title


class News(models.Model): #inherits the Model class from the models package (from django.db)
  title = models.CharField(max_length=255)
  content = models.TextField() #consumes more memory than CharField
  count = models.IntegerField(default=0) #initially 0 at the beginingS
  slug = models.SlugField(max_length = 255, null= True) #to get the same title as in the link
  category = models.ManyToManyField("Category", related_name="news_categories") # "Category" is string reprenting class whether it may be up or down 
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True) # if in case user is deleted it will set null and should be True if null
  created_at = models.DateTimeField(auto_now_add=True) # only once inserted but not updatd later ==> auto_now_add
  updated_at = models.DateTimeField(auto_now=True) #can be updated ==>auto_now
  cover_image = models.ImageField(upload_to="news", null=True) #images cannot be stored in db so we make folder and give link and change in settings
  
  def get_absolute_url(self):
        return reverse("single_news", kwargs={"pk": self.pk, "slug": self.slug})
