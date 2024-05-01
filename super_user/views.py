from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.db.models import QuerySet, Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required


GROUPS_NAMES = ['Receptionist', 'Restaurant', 'Cleaning', 'All']


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
                username__icontains=query,
            ).distinct()
        else:
            users = User.objects.filter(groups__name__in=GROUPS_NAMES).distinct()
        header = _('SuperUser - Search results for') + ' "' + query + '"'
    else:
        query = ''
        users = User.objects.filter(groups__name__in=GROUPS_NAMES).distinct()
        header = _('SuperUser')

    return render(request, 'super_user/super_user_home.html', {'query': query,
                                                               'header': header, 'users': users})

@login_required
def user_detail(request, user_id):
    if not request.user.is_superuser:
        from hotel_management.views import home
        return redirect(superuser_home)

    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        group_name = request.POST.get('group')
        if group_name in GROUPS_NAMES:
            if group_name == 'All':
                for group_name_iterator in GROUPS_NAMES:
                    if group_name_iterator != 'All':
                        group, created = Group.objects.get_or_create(name=group_name_iterator)
                        user.groups.add(group)
                return render(request, 'super_user/user_detail.html', {'user': user, 'groups': GROUPS_NAMES})

            group, created = Group.objects.get_or_create(name=group_name)
            
            user.groups.clear()
            user.groups.add(group)
            return render(request, 'super_user/user_detail.html', {'user': user, 'groups': GROUPS_NAMES})
        else:
            error_message = _("Invalid group. Please, select a valid group.")
            return render(request, 'super_user/user_detail.html', {'user': user, 'groups': GROUPS_NAMES, 'error_message': error_message})
    else:
        return render(request, 'super_user/user_detail.html', {'user': user, 'groups': GROUPS_NAMES})

@login_required
def clear_groups(request, user_id):
    if not request.user.is_superuser:
        from hotel_management.views import home
        return redirect(superuser_home)  

    user = get_object_or_404(User, pk=user_id)
    user.groups.clear()  
    return redirect(user_detail, user_id=user_id)   