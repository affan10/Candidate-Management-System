from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.


def signup_view(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # form.save() returns the user
            login(request, user)
            return redirect('candidates:candidate-list-view')
    else:
        form = UserCreationForm()
    context['form'] = form
    return render(request, 'accounts/signup.html', context)


def login_view(request):
    context = {}
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Check to redirect the user back to the page they were coming from
            return redirect('candidates:candidate-list-view')
    else:
        form = AuthenticationForm()
    context['form'] = form
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home-view')