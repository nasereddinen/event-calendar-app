from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .forms import loginform , ColorForm
from .models import Event , ColorEvent
from django.http import JsonResponse
import datetime
import json
from datetime import timedelta  
from django.contrib.auth.decorators import login_required

@login_required(login_url='login') 
def index(request):
    user = request.user.id
    eventcolors = ColorEvent.objects.all()[:4]
    list_events=Event.objects.filter(shared_with__id = user).order_by('-start_date')[:4]
    print(list_events)
    context={
            'list_color':eventcolors,
            'list_events':list_events 
             
             }
    return render(request,'calendar/main_calendar.html',context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "GET":
        form = loginform(request.GET or None)
    elif request.method == "POST":
        form = loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            messages.info(request, f"You are now logged in as {username}.")
            return HttpResponseRedirect(reverse("home"))
        
    context= {
        'form':form
        }
    
    return render(request,"authentication/login.html",context)



def list_events(request):
    
    user = request.user.id
    
    events=Event.objects.filter(shared_with__id = user).order_by('-start_date')
    list_events = []
    for event in events:
        list_events.append(
            {
                'id':event.id,
                'title':event.title,
                'start':datetime.datetime.combine(event.start_date,event.start_time).strftime("%m/%d/%Y, %H:%M:%S"),
                'end':datetime.datetime.combine(event.end_date,event.end_time).strftime("%m/%d/%Y, %H:%M:%S"),
                'color':event.type.color,
                'description': event.description,
                'owner':event.owner.username,
                'location':event.location,
            }
        )
        
    return JsonResponse(list_events,safe=False)
 
 
def add_event(request):
        
    if request.method == "POST":
    
        if request.POST.get('action',None) == 'post':
        
            title = request.POST.get('title',None)
            cat = request.POST.get('event_cat',None)
            user = request.user
            start_date = request.POST.get('start_date',None)
            end_date = request.POST.get('end_date',None)
            start_time = request.POST.get('start_time',None)
            end_time = request.POST.get('end_time',None)
            location = request.POST.get('location',None)
            description = request.POST.get('description',None)
          
        
            type = ColorEvent.objects.get(id = int(cat))
            
            #create the event oject
            
            event=Event.objects.create(
            type=type,
            title=title,
            owner=user,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time = end_time,
            location = location,
            description = description
            )
            event.shared_with.add(user)
            event.save()
    
    
    
        return JsonResponse({'status':'success'})
    else:
        
        return JsonResponse({'status':'nothing isn t happen'})
    
#delete event view


def delete_event(request):
    
    if request.method == 'POST':
        event_id = request.POST.get('event_id',None)
        if event_id:
            event = Event.objects.get(id = event_id)
            event.delete()
            return JsonResponse({'deleted':True})
        else:
            return JsonResponse({'status':'there is no user id'})
    else:
        
        return JsonResponse({'status':'nothing isn t happen'})

#the update event method 

def update_event(request,pk):
    
    '''
    
    update the event  by clicking on the event case in the calendar
    
    '''
    
    event = Event.objects.get(id = pk)
    if request.method == 'POST':
        #get the color object with the id
        color_id = request.POST.get('category',None)
        color = ColorEvent.objects.get(id = color_id )
        event.title = request.POST.get('title',None)
        event.category = color
        event.start_date = request.POST.get('start-date',None)
        event.start_time = request.POST.get('start-time',None)
        event.end_date = request.POST.get('end-date',None)
        event.end_time = request.POST.get('end-time',None)
        event.location = request.POST.get('location',None)
        event.description = request.POST.get('description-updated',None)
        event.save()
        return JsonResponse({'message':True})
    else:
        
        return JsonResponse({'status':'nothing isn t happen'},status=400)

        

def event_drop(request):
    
    event_id = request.GET.get('id',None)
    print(event_id)
    user = request.user
    type = ColorEvent.objects.first()
    
    if event_id:
        event = Event.objects.get(id = event_id)
        event.start_date = request.GET.get('start-date',None)
        event.start_time = request.GET.get('start-time',None)
        event.end_date = request.GET.get('end-date',None)
        event.end_time = request.GET.get('end-time',None)
        event.save()
    
    else:
        title = 'droped event need title'
        location = 'droped event need title'
        description = 'droped event need title'
        start_date = request.GET.get('start-date',None)
        start_time = request.GET.get('start-time',None)
        end_date = request.GET.get('end-date',None)
        end_time = request.GET.get('end-time',None)
        
        
        #create the event oject
        
        event=Event.objects.create(
        type=type,
        title=title,
        owner=user,
        start_date=start_date,
        end_date=end_date,
        start_time=start_time,
        end_time = end_time,
        location = location,
        description = description
        )
        event.shared_with.add(user)
        event.save()

    return JsonResponse({'status':'success'},status=200)

def event_drag(request):
    
    user = request.user
    type = ColorEvent.objects.first()
   
    title = 'droped event need title'
    location = 'droped event need title'
    description = 'droped event need title'
    start_date = request.GET.get('start-date',None)
    start_time = request.GET.get('start-time',None)
    
    

    end_date = datetime.datetime.strptime(start_date,'%Y-%m-%d') + timedelta(days=1)  
    end_time = request.GET.get('end-time',None)
    
    
    #create the event oject
    
    event=Event.objects.create(
    type=type,
    title=title,
    owner=user,
    start_date=start_date,
    end_date=end_date,
    start_time=start_time,
    end_time = end_time,
    location = location,
    description = description
    )
    event.shared_with.add(user)
    event.save()

    return JsonResponse({'status':'success'},status=200)


def add_color(request):
    form= ColorForm()
    if request.method == 'POST':
        form = ColorForm(request.POST)
        if form.is_valid():
            
            form.save()
            return HttpResponseRedirect(reverse('home'))
    context={'form':form}
    return render(request,'calendar/add_color.html',context)