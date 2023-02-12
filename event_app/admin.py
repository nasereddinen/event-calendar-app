from django.contrib import admin
from .models import Event,ColorEvent
from .forms import ColorForm
# Register your models here.
admin.site.register(Event)

@admin.register(ColorEvent)
class MyModel(admin.ModelAdmin):
    form = ColorForm