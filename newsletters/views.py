from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from .models import NewsLetterUser, Newsletter
from .forms import NewsLetterUserSignUpForm, NewsLetterUserUnsubscribeForm, NewsLetterCreationForm

# Create your views here.


def newsletter_signup(request):
    form = NewsLetterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsLetterUser.objects.filter(email=instance.email).exists():
            messages.warning(request, 'El correo que ingresaste ya se encuentra registrado.',
                             'alert alert-danger alert-dismissible fade show card_round mb-4')
            return redirect('newsletters:newsletter_signup')
        else:
            instance.save()
            messages.success(request, 'Felicitaciones, te has subscrito exitosamente.',
                             'alert alert-success alert-dismissible fade show card_round mb-4')
            subject = 'Gracias por Subscribirte a Doctrina EC'
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            with open(settings.BASE_DIR + '/templates/newsletters/sign_up_email.html') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(
                subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template(
                'newsletters/sign_up_email.html').render()
            message.attach_alternative(html_template, 'text/html')
            message.send()
            return redirect('newsletters:newsletter_signup')

    context = {
        'form': form
    }
    template = 'newsletters/sign_up.html'
    return render(request, template, context)


def newsletter_unsubscribe(request):
    form = NewsLetterUserUnsubscribeForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsLetterUser.objects.filter(email=instance.email).exists():
            NewsLetterUser.objects.filter(email=instance.email).delete()
            messages.success(request, 'Lamentamos que te vayas. Recuerda que estaremos esperándote nuevamente.',
                             'alert alert-warning alert-dismissible fade show card_round mb-4')
            subject = 'Lamentamos perderte de Doctrina EC'
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            with open(settings.BASE_DIR + '/templates/newsletters/sign_up_email.html') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(
                subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template(
                'newsletters/sign_up_email.html').render()
            message.attach_alternative(html_template, 'text/html')
            message.send()
            return redirect('newsletters:newsletter_signup')
        else:
            messages.warning(request, 'El correo que ingraste no se encuentra registrado.',
                             'alert alert-danger alert-dismissible fade show card_round mb-4')
            return redirect('newsletters:newsletter_unsubscribe')

    context = {
        'form': form
    }
    template = 'newsletters/unsubscribe.html'
    return render(request, template, context)


@login_required
def control_newsletter(request):
    if request.user.is_superuser:

        form = NewsLetterCreationForm(request.POST or None)

        if form.is_valid():
            instance = form.save()
            newsletter = Newsletter.objects.get(id=instance.id)

            if newsletter.status == 'Publicado':
                subject = newsletter.subject
                html_content = newsletter.body
                from_email = settings.EMAIL_HOST_USER

                for email in newsletter.email.all():
                    message = EmailMultiAlternatives(
                        subject=subject, from_email=from_email, to=[email.email])
                    message.attach_alternative(html_content, 'text/html')
                    message.send()

        context = {
            'form': form,
        }
        template = 'control_panel/control_newsletter.html'
        return render(request, template, context)

    else:
        messages.warning(request, 'No cuentas con los permisos necesarios para acceder a ésta función. Por favor contacta al administrador del sitio.',
                         'alert alert-danger alert-dismissible fade show card_round mb-4')
        return redirect('home')


@login_required
def control_newsletter_list(request):
    if request.user.is_superuser:

        newsletters = Newsletter.objects.all()

        paginator = Paginator(newsletters, 10)
        page = request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        index = items.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >= 5 else 0
        end_index = index + 5 if index <= max_index - 5 else max_index
        page_range = paginator.page_range[start_index:end_index]

        context = {
            'items': items,
            'page_range': page_range,
        }
        template = 'control_panel/control_newsletter_list.html'
        return render(request, template, context)

    else:
        messages.warning(request, 'No cuentas con los permisos necesarios para acceder a ésta función. Por favor contacta al administrador del sitio.',
                         'alert alert-danger alert-dismissible fade show card_round mb-4')
        return redirect('home')


@login_required
def control_newsletter_detail(request, pk):
    if request.user.is_superuser:

        newsletter = get_object_or_404(Newsletter, pk=pk)

        context = {
            'newsletter': newsletter,
        }

        template = 'control_panel/control_newsletter_detail.html'

        return render(request, template, context)

    else:
        messages.warning(request, 'No cuentas con los permisos necesarios para acceder a ésta función. Por favor contacta al administrador del sitio.',
                         'alert alert-danger alert-dismissible fade show card_round mb-4')
        return redirect('home')


@login_required
def control_newsletter_edit(request, pk):
    if request.user.is_superuser:

        newsletter = get_object_or_404(Newsletter, pk=pk)

        if request.method == 'POST':
            form = NewsLetterCreationForm(request.POST, instance=newsletter)

            if form.is_valid():
                newsletter = form.save()

                if newsletter.status == 'Publicado':
                    subject = newsletter.subject
                    html_content = newsletter.body
                    from_email = settings.EMAIL_HOST_USER
                    for email in newsletter.email.all():
                        message = EmailMultiAlternatives(
                        subject=subject, from_email=from_email, to=[email.email])
                        message.attach_alternative(html_content, 'text/html')
                        message.send()
                    return redirect('control_panel:control_newsletter_detail', pk=newsletter.pk)
        else:
            form = NewsLetterCreationForm(instance=newsletter)

        context = {
            'form': form,
        }

        template = 'control_panel/control_newsletter.html'

        return render(request, template, context)

    else:
        messages.warning(request, 'No cuentas con los permisos necesarios para acceder a ésta función. Por favor contacta al administrador del sitio.',
                         'alert alert-danger alert-dismissible fade show card_round mb-4')
        return redirect('home')


@login_required
def control_newsletter_delete(request, pk):
    if request.user.is_superuser:
        newsletter = get_object_or_404(Newsletter, pk=pk)

        if request.method == 'POST':
            form = NewsLetterCreationForm(request.POST, instance=newsletter)

            if form.is_valid():
                newsletter.delete()
                messages.success(request, 'El boletín ha sido borrado correctamente.',
                                 'alert alert-success alert-dismissible fade show card_round mb-4')
                return redirect('control_panel:control_newsletter_list')

        else:
            form = NewsLetterCreationForm(instance=newsletter)

        context = {
            'form': form,
        }

        template = 'control_panel/control_newsletter_delete.html'

        return render(request, template, context)

    else:
        messages.warning(request, 'No cuentas con los permisos necesarios para acceder a ésta función. Por favor contacta al administrador del sitio.',
                         'alert alert-danger alert-dismissible fade show card_round mb-4')
        return redirect('home')
