from django.contrib import admin
from .models import Post , Account,Comment
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display =('title' , 'slug' ,  'publish' ,'status')
    list_filter = ('status',)
    search_fields=('author' , 'title' , 'slug')
    prepopulated_fields= {'slug' :('title',)}
    raw_id_fields = ('author',)
    list_editable = ('status',)
    
    
@admin.register(Account)
class Account(admin.ModelAdmin):
    list_display=('user', 'get_user_id')


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display=('name','post','active','short_body')
    list_filter=('active','created')
    list_editable=('active',)
    list_select_related = True


