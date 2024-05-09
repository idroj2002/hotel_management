from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def is_accountant(user):
    return user.groups.filter(name='Accountant').exists()


@login_required
def accounting_home(request):
    if not is_accountant(request.user):
        from hotel_management.views import home
        return redirect(home)

    return render(request, 'accounting/accounting_home.html')


@login_required
def bills_home(request):
    if not is_accountant(request.user):
        from hotel_management.views import home
        return redirect(home)

    return render(request, 'accounting/bills_home.html')


@login_required
def offers_home(request):
    if not is_accountant(request.user):
        from hotel_management.views import home
        return redirect(home)

    return render(request, 'accounting/offers_home.html')


@login_required
def taxes_home(request):
    if not is_accountant(request.user):
        from hotel_management.views import home
        return redirect(home)

    return render(request, 'accounting/taxes_home.html')