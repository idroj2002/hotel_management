from django.shortcuts import render


def clients_home(request):
    return render(request, 'clients/clients_home.html')