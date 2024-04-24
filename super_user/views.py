from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import QuerySet, Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required


@login_required
def superuser_home(request):
    if not request.user.is_superuser:
        from hotel_management.views import home
        return redirect(home)

    if request.method == 'POST':
        query = request.POST.get('query')
        users = []
        if query:
            users = User.objects.filter(
                # Aquí puedes agregar los campos en los que deseas buscar coincidencias Puedes usar | (pipe) para
                # combinar múltiples filtros, lo que busca resultados que coincidan con cualquiera de los campos
                username__icontains=query,
            )
        else:
            groups_names = ['Receptionist', 'Restaurant', 'Cleaning']
            users = User.objects.filter(groups__name__in=groups_names)
        header = _('SuperUser - Search results for') + ' "' + query + '"'
    else:
        query = ''
        groups_names = ['Receptionist', 'Restaurant', 'Cleaning']
        users = User.objects.filter(groups__name__in=groups_names)
        header = _('SuperUser')

    return render(request, 'super_user/super_user_home.html', {'query': query,
                                                               'header': header, 'users': users})
