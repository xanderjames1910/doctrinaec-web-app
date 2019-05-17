from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Has creado exitosamente tu cuenta. Ahora ya puedes ingresar',
                             'alert alert-success alert-dismissible fade show card_round mb-4')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    template = 'users/register.html'
    return render(request, template, context)


@login_required
def profile(request):
    return render(request, 'users/profile.html')
