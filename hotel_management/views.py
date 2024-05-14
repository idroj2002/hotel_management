from django.shortcuts import render, redirect
from django.utils.translation.trans_real import translation
from pyexpat.errors import messages

from administration.views import reservation_list
from hotel_management import settings
from restaurant.views import restaurant_home
from cleaning.views import cleaning_home
from super_user.views import superuser_home
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.conf import settings
from django.contrib import messages
from urllib.parse import urlparse, urlunparse

def is_receptionist(user):
    return user.groups.filter(name='Receptionist').exists()


def is_restaurant(user):
    return user.groups.filter(name='Restaurant').exists()


def is_cleaner(user):
    return user.groups.filter(name='Cleaning').exists()


def home(request):
    is_superuser = request.user.is_superuser
    is_receptionistuser = is_receptionist(request.user)
    is_restaurantuser = is_restaurant(request.user)
    is_cleaneruser = is_cleaner(request.user)
    is_worker = False
    if is_superuser or is_receptionistuser or is_restaurantuser or is_cleaneruser:
        is_worker = True
    if is_worker:
        return render(request, 'home.html', {'is_worker':is_worker, 'is_receptionist':is_receptionistuser, 'is_restaurant':is_restaurantuser, 'is_cleaner':is_cleaneruser, 'is_superuser':is_superuser})
    else:
        return render(request, 'clients/clients_home.html')



def set_language(request):
    if request.method == 'POST' and 'language' in request.POST:
        language = request.POST['language']
        next_url = request.POST.get('next', '/')

        if language in [lang_code for lang_code, _ in settings.LANGUAGES]:
            parsed_url = urlparse(next_url)
            path = parsed_url.path

            parts = path.split('/')
            if len(parts) > 1 and parts[1] in [lang_code for lang_code, _ in settings.LANGUAGES]:
                path = '/'.join(parts[2:]) if len(parts) > 2 else '/'

            if path.startswith('/'):
                path = f'/{language}{path}'
            else:
                path = f'/{language}/{path}'

            new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, path, '', '', ''))

            request.session['django_language'] = language
            translation.activate(language)

            return redirect(new_url)
        else:
            messages.warning(request, _("Invalid language selection."))

    return redirect('/')
