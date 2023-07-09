from django.shortcuts import render

from .models import  product
from .scrape_mobile import scrape_mobile
from .scrape_tablet import scrape_tablet
from .scrape_laptop import scrape_laptop
from .scrape_washing_machine import scrape_washing_machine
from .scrape_smart_watch import scrape_smart_watch

def home(request):
    context = {
        'product': product.objects.all()
    }
    return render(request, 'blog/home.html', context)
  
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

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

def search(request):
    query = request.GET.get('query')
    results = None
    
    if query:
        results = product.objects.filter(name__icontains=query).order_by('-id')
        
    
    return render(request, 'blog/search.html', {'results': results, 'query': query})