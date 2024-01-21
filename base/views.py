from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import User, Article, Topic, Message
from .forms import ArticleForm, UserForm, MyUserCreationForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'auuu')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}

    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    articles = Article.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q)|
        Q(author__username__icontains=q)

    )

    context = {"articles": articles}
    return render(request, 'base/home.html', context)

def article(request, pk):
    article = Article.objects.get(id=pk)
    article_messages = article.message_set.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            article=article,
            body=request.POST.get('body')
        )
        return redirect('article', pk=article.id)

    context = {'article': article, 'article_messages': article_messages}
    return render(request, 'base/article.html', context)

@login_required(login_url='login')
def createArticle(request):
    form = ArticleForm()
    if not request.user.is_author :
        return HttpResponse('Your are not allowed here!!')
    #topics = Topic.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('home')

        #topic_name = request.POST.get('topic')
        #topic, created = Topic.objects.get_or_create(name=topic_name)

        # Article.objects.create(
        #     author=request.user,
        #     topic=request.POST.get('topic'),
        #     tilte=request.POST.get('title'),
        #     description=request.POST.get('description'),
        #     body=request.POST.get('body'),
        # )
        # return redirect('home')

    context = {'form': form}
    return render(request, 'base/article_form.html', context)

@login_required(login_url='login')
def editArticle(request, pk):
    article = Article.objects.get(id=pk)
    form = ArticleForm(instance=article)
#     topics = Topic.objects.all()
    if request.user != article.author:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
#         topic_name = request.POST.get('topic')
#         topic, created = Topic.objects.get_or_create(name=topic_name)
#         room.name = request.POST.get('name')
#         room.topic = topic
#         room.description = request.POST.get('description')
#         room.save()
#         return redirect('home')
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/article_form.html', context)


@login_required(login_url='login')
def deleteArticle(request, pk):
    article = Article.objects.get(id=pk)

    if request.user != article.author:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        article.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': article})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('article',message.article.pk)
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/update-user.html', {'form': form})


# def topicsPage(request):
#     q = request.GET.get('q') if request.GET.get('q') != None else ''
#     topics = Topic.objects.filter(name__icontains=q)
#     return render(request, 'base/topics.html', {'topics': topics})


# def activityPage(request):
#     room_messages = Message.objects.all()
#     return render(request, 'base/activity.html', {'room_messages': room_messages})