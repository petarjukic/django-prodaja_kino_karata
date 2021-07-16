from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseNotAllowed
from .models import Ticket, Projection
from .forms import *
from . import models
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count



def obrana_zadnje_vjezbe(request, proj_id):
    
    if Ticket.objects.filter(projection_id=proj_id).count() > 1:
        #print(Ticket.objects.filter(projection_id=proj_id))
        ne = Ticket.objects.filter(projection_id=proj_id)
    else:
        ne = Ticket.objects.filter(projection_id=proj_id)
    
    return render(request, 'obrana_zadnje_vjezbe.html', {'ne':ne})      
    

@login_required
def projection_view(request):
    context={}
    projections = Projection.objects.all()
    context['projections'] = projections
    return render(request, "projection_view.html", context)


@login_required
def buy_ticket(request, projection_id):
    projection = Projection.objects.get(pk=projection_id)
    bought_card = Ticket.objects.filter(projection=projection_id).values_list('seatNumber', flat=True)
    context = {
        "projection": projection,
        "bought_card": bought_card
    }

    if request.method == 'POST':
        seatNumber = request.POST['seatNumber']
        Ticket.objects.create(projection=projection, user=request.user, seatNumber=seatNumber)
        return redirect('buy')
    return render(request, "buy_ticket.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def count_user_projection(request):
    tickets = Projection.objects.all()
    return render(request, 'search_projection.html', {'tickets':tickets})   


@login_required
def counter_projection(request, p_id):
   projections = Projection.objects.all()
   ticket = Ticket.objects.filter(user_id=p_id).count()

   return render(request, 'count_projections.html', {'ticket':ticket})


@login_required
@user_passes_test(lambda u: u.is_superuser) 
def projection_users(request):
    tickets = Ticket.objects.all()
    return render(request, 'projection_users.html', {'tickets':tickets})


@login_required 
def user_tickets(request): 
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'my_tickets.html', {'tickets':tickets})


@login_required
@user_passes_test(lambda u: u.is_superuser) 
def all_users(request):
    users = Person.objects.all()
    return render(request, 'all_users.html', {'users':users})


@login_required
@user_passes_test(lambda u: u.is_superuser) 
def set_superuser(request, person_id): 
    person = Person.objects.get(id=person_id)

    if request.method == 'GET':             
        set_form = SuperUserForm(instance=person)
        return render(request, 'set_superuser.html', {'form':set_form})
    elif request.method == 'POST':
        set_form = SuperUserForm(request.POST, instance=person)
        if set_form.is_valid():
            set_form.save()
            return redirect('insert_projection')
        else:
            return HttpResponseNotAllowed()


@login_required
@user_passes_test(lambda u: u.is_superuser) 
def inster_projection(request):
    if request.method == 'GET':
        projection_form = ProjectionForm()
        return render(request, 'insert_projection.html', {'form':projection_form})
    elif request.method == 'POST':
        projection_form = ProjectionForm(request.POST)
        if projection_form.is_valid():
            projection_form.save()
            return redirect('buy')
        else:
            return HttpResponseNotAllowed()


def home_view(request): 
    projection = Projection.objects.all()
    return render(request, 'home.html', {'projection':projection})
    #return render(request, 'home.html', {})
    


def register(request): 
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            #account = authenticate(email=email, password=raw_password) #kad radin save nije potrebno
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'registration.html', context)


def logout_view(request): 
    logout(request)
    return redirect('home')

