from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PostManager(models.Manager):
    def Published(self):
        return self.filter(status = 'published')


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = PostManager()
    tags = TaggableManager()
    
    class Meta:
        ordering = ("-publish",)
        
    def get_abselute_url(self):
        return reverse('blog:SingleP',args=[self.slug,self.id])
        
    def __str__(self):
        return self.title
 
    
    
class Account(models.Model):
    gender_choice = (('آقا' , "آقا"),("خانم",'خانم'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    phone = models.CharField(max_length=11 , blank=True ,null=True)
    gender = models.CharField(max_length=5 , choices=gender_choice , default='خانم')
    address = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    age = models.PositiveIntegerField(default=0,blank=True)

    def __str__(self):
        return self.user.get_full_name()
    
    def get_user_id(self):
        return self.user.id
    get_user_id.short_description = 'User ID'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250,)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)

    def short_body(self):
        return self.body[:50]  # نمایش تنها 50 کاراکتر اول از body

    short_body.short_description = 'Short Body'  # عنوان ستون در پنل ادمین
    def __str__(self):
        return self.post.title + ' - ' + self.name + ' - ' + self.body
