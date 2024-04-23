from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def superuser_home(request):
    if not request.user.is_superuser:
        from hotel_management.views import home
        return redirect(home)
    
    return render(request, 'super_user/super_user_home.html')


