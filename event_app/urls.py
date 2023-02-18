from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='home'),
    path('login',views.login_view,name='login'),
    path('list_event',views.list_events,name='list_event'),
    path('add_event/',views.add_event,name='add_event'),
    path('delete_event',views.delete_event,name='delete_event'),
    path('update_event/<int:pk>/',views.update_event,name='update_event'),
    path('updatedrop/',views.event_drop,name='drop_event'),
    path('updatedrag/',views.event_drag,name='drag_event'),
    path('logout',views.logout_view,name='logout'),

    
    
]