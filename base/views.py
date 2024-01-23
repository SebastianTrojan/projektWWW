from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import User, Article, Topic, Message
from .forms import ArticleForm, UserForm, MyUserCreationForm
from django.shortcuts import render

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
    status = request.GET.get('status') if request.GET.get('status') != None else ''

    if status =='':
        articles = Article.objects.filter(
            Q(topic__name__icontains=q) |
            Q(title__icontains=q) |
            Q(description__icontains=q)|
            Q(author__username__icontains=q)
        )
    else:
        articles = Article.objects.filter(
            Q(topic__name__icontains=q) |
            Q(title__icontains=q) |
            Q(description__icontains=q)|
            Q(author__username__icontains=q)&
            Q(is_published=status)

        )
    topics = Topic.objects.all()

    context = {"articles": articles, "topics": topics}
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
    if not request.user.is_author :
        return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            if 'publish_button' in request.POST:
                article.is_published = True
            article.save()

            return redirect('home')
    context = {'form': form}
    return render(request, 'base/article_form.html', context)


@login_required(login_url='login')
def editArticle(request, pk):
    article = Article.objects.get(id=pk)
    form = ArticleForm(instance=article)

    if request.user != article.author:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            if 'publish_button' in request.POST:
                article.is_published = True
            article.save()
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
