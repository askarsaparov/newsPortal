from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages

from news.forms import CreateUserForm, CommentForm, AdminCategoryForm, AdminNewsUpdate
from news.models import News, Category, Comment, Customer
from news.decorators import unauthenticated_user, allowed_users, admin_only


def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    ctx = {
        'form': form,
    }
    return render(request, 'register.html', ctx)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
    ctx = {}
    return render(request, 'login.html', ctx)

def logoutUser(request):
    logout(request)
    return redirect('home')

def profile(request):
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        user = User.objects.get(username=customer.user.username)

        user.username = request.POST.get('username')
        customer.name = request.POST.get('name')
        user.email = request.POST.get('email')
        customer.email = request.POST.get('email')

        customer.save()
        user.save()
        return redirect('home')
    customer = Customer.objects.get(user=request.user)
    user = User.objects.get(username=customer.user.username)
    context = {
        'user': user,
        'customer': customer,
    }
    return render(request, 'profile.html', context)

@allowed_users(allowed_roles=['admin'])
def adminPage(request):
    context = {

    }
    return render(request, 'admin.html', context)

def adminPageCategoryList(request):
    category_list = Category.objects.all()
    context = {
        'category_list': category_list,
    }
    return render(request, 'admin_category/category_list.html', context)

def adminPageCategoryDelete(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('admin_page_category_list')

def adminCreateCategory(request):
    if request.method == 'POST':
        category = Category()
        category.title = request.POST.get('title')
        if len(request.FILES)!=0 :
            category.image = request.FILES['image']

        category.save()
        return redirect('admin_page_category_list')
    context = {

    }
    return render(request, 'admin_category/create_update_category.html', context)

def adminUpdateCategory(request, id):
    model = Category.objects.get(id=id)
    form = AdminCategoryForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('admin_page_category_list')
    context = {
        'model': model,
        'form': form,
    }
    return render(request, 'admin_category/create_update_category.html', context)

def adminPageCommentsNewsList(request):
    newses = News.objects.all()
    context = {
        'newses': newses,
    }
    return render(request, 'admin_comments/news.html', context)

def adminPageCommentsList(request, id):
    news = News.objects.get(id=id)
    comments = Comment.objects.filter(news=news)
    context = {
        'comments': comments,
        'news': news,
    }
    return render(request, 'admin_comments/comments_list.html', context)

def adminPageDeleteComment(request, id):
    comment = Comment.objects.get(id=id)
    id = comment.news.id
    comment.delete()
    return HttpResponseRedirect("/admin2/comments_list/{id}/".format(id=id))

def adminPageCustomersList(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'admin_customer/customers_list.html', context)

def adminPageCustomerDelete(request, id):
    customer = Customer.objects.get(id=id)
    customer.user.delete()
    return redirect('customers_list')

def adminPageNewsList(request):
    newses = News.objects.all()
    context = {
        'newses': newses,
    }
    return render(request, 'admin_news/news_list.html', context)

def adminPageNewsDelete(request, id):
    news = News.objects.get(id=id)
    news.delete()
    return redirect('admin_news_list')

def adminPageCreateNews(request):
    if request.method == 'POST':
        news = News()
        categories = Category.objects.all()
        categorytitle = request.POST.get('category')
        for category in categories:
            if category.title == categorytitle:
                news.category = category
        news.title = request.POST.get('title')
        news.body_text = request.POST.get('body_text')
        if len(request.FILES)!=0:
            news.image = request.FILES['image']

        news.save()
        return redirect('admin_news_list')
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'admin_news/admin_news_create_update.html', context)

def adminPageUpdateNews(request, id):
    model = News.objects.get(id=id)
    form = AdminNewsUpdate(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect('admin_news_list')
    categories = Category.objects.all()
    context = {
        'model': model,
        'categories': categories,
        'form': form,
    }
    return render(request, 'admin_news/admin_news_create_update.html', context)

@admin_only
def homePage(request):
    last_news = News.objects.last()
    latest_news = News.objects.all().order_by('-id')[1:6]
    from_this_category = News.objects.filter(category=last_news.category).order_by('-id')[1:5]
    context = {
        'last_news': last_news,
        'latest_news': latest_news,
        'from_this_category': from_this_category,
    }
    return render(request, 'home.html', context)

def detailNews(request, id):
    news = News.objects.get(id=id)
    if request.user.is_authenticated:
        name = request.user.username
    else:
        name = None
    form = CommentForm(request.POST or None)
    if request.POST and form.is_valid():
        form.instance.news = news
        form.instance.name = request.user
        form.save()
        return HttpResponseRedirect("/detail/{id}/".format(id=news.id))
    comments = Comment.objects.filter(news=news)
    context = {
        'news': news,
        'name': name,
        'comments': comments,
        'form': form,
    }
    return render(request, 'detail.html', context)

class AllNewsPage(ListView):
    model = News
    template_name = 'all_news.html'
    ordering = ['-id']

class AllCategory(ListView):
    model = Category
    template_name = 'category.html'

def categoryNews(request, id):
    model = Category.objects.get(id=id)
    category = News.objects.filter(category=model).order_by('-id')
    context = {
        'category': category,
        'title': model,
    }
    return render(request, 'category_news.html', context)



