from django.db.models import Count
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Post , Account, Comment
from .forms import AcountForm, ContactForm, ShareForm, CommentForm ,loginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from  django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank , TrigramSimilarity
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def blog(request):
    user = request.user
    return HttpResponse('HI Im There' +" "+ str(user))

def PostList(request,tag_slug=None):
    posts = Post.objects.Published()
    tag = None
    if tag_slug:
        tag = Tag.objects.get(slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 2)  
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # اگر صفحه یک عدد صحیح نبود، اولین صفحه را نمایش بده
        posts = paginator.page(1)
    except EmptyPage:
        # اگر صفحه خارج از محدوده بود، آخرین صفحه را نمایش بده
        posts = paginator.page(paginator.num_pages)
    
    return render(request,'postList.html' , {'posts':posts,'tag':tag})


def SinglePost(request, slug, id):
    post = get_object_or_404(Post, slug=slug, id=id)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            form = CommentForm() # Reset the form after successful submission
        else:
            form = CommentForm(data=request.POST)
    else:
        form = CommentForm()

    ids = post.tags.values_list('id', flat=True)
    print(ids)
    similar_posts = Post.objects.filter(tags__in=ids,status='published').exclude(id=post.id)
    similar_posts = similar_posts.annotate(s_count= Count('tags')).order_by('-s_count','-publish')
    print(similar_posts)

    return render(request, 'singlePost.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'new_comment': new_comment,
        "similar_posts" : similar_posts
    })


def Form(request):
    user = request.user
    try:
        acount = Account.objects.get(user = user)
    except:
        acount = Account.objects.create(user = user)
    if (request.method == 'POST'):
        form = AcountForm(data=request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first']
            user.last_name = form.cleaned_data['last']
            acount.gender = form.cleaned_data['gender']
            acount.address = form.cleaned_data['address']
            acount.age = form.cleaned_data['age']
            user.save()
            acount.save()
            print("valid")
            return redirect('blog:index')
        else:
            print("is not valid")
            form = AcountForm(data=request.POST)
            return render(request , 'acount_form.html' ,{'form' : form , 'acount' :acount} )
    form = AcountForm()
    return render(request , 'acount_form.html' ,{'form' : form , 'acount' :acount})


def Contact(request):
    send = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            phone = form.cleaned_data['phone']
            msg = "name={0} \nemail={1} \nmessage={2}\n phone={3}".format(name,email,message,phone)
            send_mail(subject, msg, 'hassan1383esk@gmail.com', ['hassan2004esk@gmail.com'], fail_silently=False)
            send = True
            return render(request,'contactus.html',{'form':form,'sent':send})



    form = ContactForm()
    return render(request,'contactus.html',{'form' : form,'sent':send},)



def SharePost(request,id):
    post = get_object_or_404(Post, id=id,status='published')
    full_url = request.build_absolute_uri(post.get_abselute_url())
    send = False
    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            to = form.cleaned_data['to']
            message = form.cleaned_data['message']
            subject = '{0}invite you to see {1}'.format(name,post.title)
            msg ='name = {0} \n post = {1} \n message = {2}'.format(name,full_url,message)
            send_mail(subject, msg, 'hassan1383esk@gmail.com', [to], fail_silently=False)
            send = True
            return render(request, 'share.html', {'form': form, 'sent': send})
        else:
            print("is not valid")
            form = ShareForm(data=request.POST)
            return render(request, 'share.html', {'form': form,'sent':send,'post':post})
    form = ShareForm()
    return render(request, 'share.html', {'form': form,'sent':send,'post':post})


def search(request,tag_slug=None):
    posts = Post.objects.Published()
    tag = None
    if request.method == "GET":
        posts = Post.objects.Published()
        tag = None
        query = request.GET.get('search_input')
        if query:
            request.session['search'] = query
        else:
            try:
                query = request.session['search']
            except:
                query = ''
        # search_query = SearchQuery(query)
        search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        # results = Post.objects.Published().annotate(
        #     search=search_vector,
        #     rank=SearchRank(search_vector, search_query)
        # ).filter(search=search_query).order_by('-rank')
        similar = TrigramSimilarity('body', query) + TrigramSimilarity('title', query)
        results = Post.objects.Published().annotate(
            similarity=similar
        ).filter(similarity__gt=0).order_by('-similarity')

        posts = results
        tag = None
        if tag_slug:
            tag = Tag.objects.get(slug=tag_slug)
            posts = posts.filter(tags__in=[tag])
        paginator = Paginator(posts, 1)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # اگر صفحه یک عدد صحیح نبود، اولین صفحه را نمایش بده
            posts = paginator.page(1)
        except EmptyPage:
            # اگر صفحه خارج از محدوده بود، آخرین صفحه را نمایش بده
            posts = paginator.page(paginator.num_pages)

        return render(request, 'postList.html', {'posts': posts, 'tag': tag})




def login_user(request):

    if(request.method == 'POST'):
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request ,username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blog:post_list')
            else : return HttpResponse('not loged in')
    else:
        form = loginForm()
    return  render(request,'account/login.html',{'form':form})


def logout_user(request):
    logout(request)
    return redirect('blog:post_list')