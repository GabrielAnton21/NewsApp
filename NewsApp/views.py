from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import requests


@login_required(login_url='login')
def index(request):
    if request.method == 'POST':
        # get the search term
        search_term = request.POST.get('search_term')

        url = f'https://newsapi.org/v2/everything?qInTitle={search_term}&apiKey=39db9d3b16664b1192e2d2258e9bd5ca'

        response = requests.get(url)
        data = response.json()
        totalResults = data['totalResults']
        articles = data['articles']
        return render(request, 'NewsApp_view/index.html', {'articles': articles, 'totalResults': totalResults})
    else:
        return render(request, 'NewsApp_view/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'NewsApp_view/register.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'NewsApp_view/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')