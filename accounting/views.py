from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from restaurant.models import RestaurantBill
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


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

    bills = RestaurantBill.objects.filter(paid=True).order_by('-id')
    
    """if bill:
        # Calculate total cart cost
        cart_items = bill.shoppingcart_set.all()
        total = sum(item.item.price * item.quantity for item in cart_items)

        # Get cart resume
        cart_items = bill.shoppingcart_set.all()
        resume = [(item.item, item.quantity, item.item.price * item.quantity) for item in cart_items]
    else:
        return HttpResponseBadRequest"""

    return render(request, 'accounting/bills_home.html', {'bills':bills})


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


@login_required
def invoice_pdf(request):
    context = {}
    html = render_to_string("accounting/restaurant_invoice_pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; invoice.pdf"

    #font_config = FontConfiguration()
    HTML(string=html).write_pdf(response)

    return response
