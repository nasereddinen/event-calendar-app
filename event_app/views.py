from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .forms import loginform,UsersForm
from .models import Event 
from django.http import JsonResponse
import datetime
import json
from datetime import timedelta  
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()
@login_required(login_url='login') 

def index(request):
    user = request.user.id
    form = UsersForm()
    users = User.objects.all().exclude(id=user)
    
    events=Event.objects.filter(shared_with__id = user).order_by('-start_date')

    list_events = []
    for event in events:
        list_events.append(
            {
                'id':event.id,
                'title':event.title,
                'start':datetime.datetime.combine(event.start_date,event.start_time).strftime("%m/%d/%Y, %H:%M:%S"),
                'end':datetime.datetime.combine(event.end_date,event.end_time).strftime("%m/%d/%Y, %H:%M:%S"),
                'description':event.description,
                'location':event.location,
                'className':event.type,
                'allday':0 if event.all_day ==False else 1,
                'followers':list(event.shared_with.all().values('id','username'))
                
            }
        )
    
  
    context={
            
            'list_events':list(list_events),
            'list_users':users,
            'form':form
             
             }
    return render(request,'calendar.html',context)

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
                
            }
        )
        
    return JsonResponse(list_events,safe=False)
 
 
def add_event(request):
        
    if request.method == "POST":
    
        title = request.POST.get('title',None)
        type = request.POST.get('category',None)
        eventid = request.POST.get('eventid',None)
        user = request.user
        all_date = request.POST.get('start-date',None)
        start_time = request.POST.get('start-time',None)
        end_time = request.POST.get('end-time',None)
        location = request.POST.get('event-location',None)
        description = request.POST.get('event-description',None)
        foll = request.POST.getlist('followed_user',None)
        alldays = True if request.POST.get('allday',None) == 'on' else False
        
        if alldays == True:
            start_time=datetime.time(0, 0, 0)
            end_time = datetime.time(0, 0, 0)
        
        #separate the date to start and end date
        
        if all_date:
            full_date = all_date.split('to')
            
            strt_date = datetime.datetime.strptime(full_date[0].rstrip(),"%Y-%m-%d").date()
            ed_date = datetime.datetime.strptime(full_date[-1].strip(),"%Y-%m-%d").date()
            
            
            #check if is an add request or update
            
        if eventid == "":
            event=Event.objects.create(
            type=type,
            title=title,
            owner=user,
            start_date=strt_date,
            end_date=ed_date,
            start_time=start_time,
            end_time = end_time,
            location = location,
            description = description,
            all_day=alldays
            )
            event.shared_with.add(user)
            for user_id in foll:
                fl_usr = User.objects.get(id=user_id)
                event.shared_with.add(fl_usr)
            event.save()
        else:
            eventup = Event.objects.get(id = eventid)
            eventup.title = title
            eventup.type = type
            eventup.all_day = alldays
            eventup.start_date = strt_date
            eventup.start_time = start_time
            eventup.end_date = ed_date
            eventup.end_time = end_time
            eventup.location = location
            eventup.description = description
            eventup.all_day=alldays
            eventup.shared_with.clear()
            for user_id in foll:
                up_usr = User.objects.get(id=user_id)
                eventup.shared_with.add(up_usr)
            eventup.shared_with.add(eventup.owner)
            eventup.save()   

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
    
    event = Event.objects.get(id)
    if request.method == 'POST':
        #get the color object with the id
        event.title = request.POST.get('uptitle',None)
        
        event.start_date = request.POST.get('upstart-date',None)
        event.start_time = request.POST.get('upstart-time',None)
        event.end_date = request.POST.get('upend-date',None)
        event.end_time = request.POST.get('upend-time',None)
        event.location = request.POST.get('upevent-location',None)
        event.description = request.POST.get('updescription-updated',None)
        event.save()
        return JsonResponse({'message':True})
    else:
        
        return JsonResponse({'status':'nothing isn t happen'},status=400)

        

def event_drop(request):
    
    event_id = request.GET.get('id',None)
    print(event_id)
    user = request.user
    date_str=request.GET.get('start-date',None)
    datend_str = request.GET.get('end-date',None)
    print(datend_str)
    #start date
    date_obj = datetime.datetime.strptime(date_str[:24],'%a %b %d %Y %H:%M:%S')
    startf_date = date_obj.strftime('%Y-%m-%d')
    print(startf_date)
    startf_time = date_obj.strftime('%H:%M:%S')
    #end date
    datend_obj = datetime.datetime.strptime(datend_str[:24],'%a %b %d %Y %H:%M:%S')
    endf_date = datend_obj.strftime('%Y-%m-%d')
    print(endf_date)
    endf_time = datend_obj.strftime('%H:%M:%S') 
    
    print(startf_date)
    if event_id:
        event = Event.objects.get(id = event_id)
        event.start_date = startf_date
        event.start_time = startf_time
        event.end_date = endf_date
        event.end_time = endf_time
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
    
   
    title = "dragable event"
    location = 'Drag event'
    description = 'Drag event'
    start_date = request.GET.get('start-date',None)
    print(start_date)
    type= request.GET.get('className',None)
    
    
    date_obj = datetime.datetime.strptime(start_date[:24],'%a %b %d %Y %H:%M:%S')
    startf_date = date_obj.strftime('%Y-%m-%d')
    start_time=datetime.time(0, 0, 0)
    endf_date = datetime.datetime.strptime(startf_date,'%Y-%m-%d')+ datetime.timedelta(days=1)  
    end_date = endf_date.strftime('%Y-%m-%d')
    #create the event oject
    
    event=Event.objects.create(
    type=type,
    title=title,
    owner=user,
    start_date=startf_date,
    end_date=end_date,
    start_time=start_time,
    end_time = start_time,
    location = location,
    description = description,
   
    )
    event.shared_with.add(user)
    event.save()

    return JsonResponse({'status':'success'},status=200)


