from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from restaurant.models import RestaurantBill
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import QuerySet, Q
from django.utils.translation import gettext_lazy as _
from accounting.models import Offer
from restaurant.models import RestaurantBill, RestaurantItem, ShoppingCart
from administration.models import RestaurantReservation, HotelReservation
from django.utils import timezone

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

    restaurant_bills = RestaurantBill.objects.filter(paid=True).order_by('-id')[:20]
    room_bills = HotelReservation.objects.filter(
        Q(checkout__isnull=False) & Q(cancelled=False)
    )[:20]

    room_query = ''
    if request.method == 'POST':
        room_query = request.POST.get('room_query')
        if room_query:
            room_bills = HotelReservation.objects.filter(
                Q(id__icontains=room_query) |
                Q(first_name__icontains=room_query) |
                Q(last_name__icontains=room_query),
                Q(checkout__isnull=False),
                Q(cancelled=False)
            )
            room_header = _('Room invoices - Search results for') + ' "' + room_query + '"'
    if not room_query:
        room_header = _('Room invoices')
    
    restaurant_query = ''
    if request.method == 'POST':
        restaurant_query = request.POST.get('restaurant_query')
        if restaurant_query:
            restaurant_bills = RestaurantBill.objects.filter(
                Q(id__icontains=restaurant_query) |
                Q(reservation__name__icontains=restaurant_query),
                paid=True
            )
            restaurant_header = _('Restaurant invoices - Search results for') + ' "' + restaurant_query + '"'
    if not restaurant_query:
        restaurant_header = _('Restaurant invoices')

    return render(request, 'accounting/bills_home.html', {'restaurant_bills':restaurant_bills, 'room_bills':room_bills, 'room_header':room_header, 'restaurant_header':restaurant_header})


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

@login_required()
def calculate_tourist_tax(request):
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (today.replace(month=today.month + 1, day=1) - timedelta(days=1))

    reservations = HotelReservation.objects.filter(
        check_in_date__lte=last_day_of_month,
        check_out_date__gte=first_day_of_month
    ).filter(cancelled=False)

    total_tax = sum(reservation.number_of_nights * reservation.number_of_guests for reservation in reservations)

    context = {
        'total_tax': total_tax,
        'reservations': reservations,
        'today' : today,
    }

    return render(request, 'accounting/tourist_tax.html', context)

