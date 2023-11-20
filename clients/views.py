from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from .forms import ClientForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .models import Client
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def clients(request):
    client_list = Client.objects.all().order_by('name')
    paginator = Paginator(client_list, 10) 
    page_number = request.GET.get('page')
    clients = paginator.get_page(page_number)
    context = {'clients': clients}
    return render(request, 'clients.html', context)

@login_required
def add_client(request, pk=None):
    if pk is not None:
        client = get_object_or_404(Client, pk=pk)
        form = ClientForm(request.POST or None, request.FILES or None, instance=client)
    else:
        form = ClientForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('settings_clients')

    template = 'add_client.html'
    context = {'form': form, 'editing': pk is not None}
    return render(request, template, context)

from django.views.decorators.http import require_POST
from django.shortcuts import redirect

@login_required
@require_POST
def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('settings_clients')


