
from django.urls import path
from .views import blog, PostList, SinglePost, Form, Contact, SharePost, search, login_user,logout_user

app_name ="blog"

urlpatterns = [
    path('', blog, name='index'),
    path('post_list/', PostList, name='post_list'),
    path('post_list/<slug:tag_slug>/', PostList, name='post_list_tag'),
    path('post_list/<slug:slug>/<int:id>', SinglePost , name='SingleP'),
    path('form/', Form, name='form'),
    path('contactUs/',Contact, name='contact'),
    path('share/<int:id>/',SharePost, name='share'),
    path('search/', search, name='search'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

]