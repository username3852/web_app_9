from django.contrib import admin
from news.models import News, Category # always use absolute path instead of relative 
# Register your models here. It will display in the admin panel if registered

# admin.site.register(News)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
  list_display = ("author", "title", "updated_at", "created_at",)
  prepopulated_fields = {"slug": ("title",)}
  search_fields = ("content", "title",)
  sortable_by = ("updated_at")


admin.site.register(Category)
