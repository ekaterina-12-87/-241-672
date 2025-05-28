from django.contrib import admin
from .models import Post, esexam  # Импортируем обе модели
from django.utils.translation import gettext_lazy as _


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
 list_display = ['title', 'slug', 'author', 'publish', 'status']
 list_filter = ['status', 'created', 'publish', 'author']
 search_fields = ['title', 'body']
 prepopulated_fields = {'slug': ('title',)}
 raw_id_fields = ['author']
 date_hierarchy = 'publish'
 ordering = ['status', 'publish']


@admin.register(esexam)
class ExamAdmin(admin.ModelAdmin):

 search_fields = ['title', 'users__email']


 date_hierarchy = 'exam_date'

 filter_horizontal = ('users',)


 list_filter = (
  'is_public',
  ('created', admin.DateFieldListFilter),
 )


 list_display = ('title', 'exam_date', 'created', 'is_public')


 fieldsets = (
  (None, {
   'fields': ('title', 'is_public')
  }),
  ('Даты', {
   'fields': ('exam_date', 'created'),
   'classes': ('collapse',)
  }),
  ('Контент', {
   'fields': ('image',)
  }),
  ('Пользователи', {
   'fields': ('users',)
  }),
 )

 readonly_fields = ('created',)

 ordering = ('-created',)


# Register your models here.
