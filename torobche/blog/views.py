from django.shortcuts import render
from django.http import HttpResponse
from .models import  product
from .scrape_mobile import Mobile, scrape_mobile
from .scrape_tablet import scrape_tablet
from .scrape_laptop import scrape_laptop
from .scrape_washing_machine import scrape_washing_machine
from .scrape_smart_watch import scrape_smart_watch

def home(request):
    return HttpResponse('<h1> Blog Home </h1>')

def about(request):
    return HttpResponse('<h1> Blog About </h1>')

def mobile(request):
    mobiles = scrape_mobile()
    return render(request, 'blog/mobile.html', {'mobiles': mobiles})


def tablet(request):
    tablets = scrape_tablet()
    return render(request, 'blog/tablet.html', {'tablets': tablets})


def laptop(request):
    laptops = scrape_laptop()
    return render(request, 'blog/laptop.html', {'laptops': laptops})


def washing_machine(request):
    washing_machines = scrape_washing_machine()
    return render(request, 'blog/washing_machine.html', {'washing_machines': washing_machines})


def smart_watch(request):
    smart_watches = scrape_smart_watch()
    return render(request, 'blog/smart_watch.html', {'smart_watches': smart_watches})