from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from restaurant.models import RestaurantBill
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import QuerySet, Q
from django.utils.translation import gettext_lazy as _
from accounting.models import Offer
from restaurant.models import RestaurantBill, RestaurantItem, ShoppingCart
from administration.models import RestaurantReservation


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

    bills = RestaurantBill.objects.filter(paid=True).order_by('-id')[:20]
    
    query = '-1'
    if request.method == 'POST':
        query = request.POST.get('query')
        if query == "":
            bills = RestaurantBill.objects.filter(paid=True).order_by('-id')
            header = _('Restaurant invoices')
        else:
            bills = RestaurantBill.objects.filter(
                Q(id__icontains=query) |
                Q(reservation__name__icontains=query),
                paid=True
            )
            header = _('Restaurant invoices - Search results for') + ' "' + query + '"'
    else:
        bills = RestaurantBill.objects.filter(paid=True).order_by('-id')
        header = _('Restaurant invoices')

    return render(request, 'accounting/bills_home.html', {'bills':bills, 'header':header})


@login_required
def offers_home(request):
    if not is_accountant(request.user):
        from hotel_management.views import home
        return redirect(home)

    offers = Offer.objects.all()

    return render(request, 'accounting/offers_home.html', {'offers': offers})


@login_required
def taxes_home(request):
    if not is_accountant(request.user):
        from hotel_management.views import home
        return redirect(home)

    return render(request, 'accounting/taxes_home.html')


@login_required
def invoice_pdf(request, reservation_id):
    bill = RestaurantBill.objects.get(reservation_id=reservation_id)

    if bill:
        # Calculate total cart cost
        cart_items = bill.shoppingcart_set.all()
        total = sum(item.item.price * item.quantity for item in cart_items)

        # Get cart resume
        resume = [(item.item, item.quantity, item.item.price * item.quantity) for item in cart_items]
    else:
        return HttpResponseBadRequest

    context = {'items':resume, 'total':total, 'bill':bill}
    html = render_to_string("accounting/restaurant_invoice_pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; invoice.pdf"

    #font_config = FontConfiguration()
    HTML(string=html).write_pdf(response)

    return response
