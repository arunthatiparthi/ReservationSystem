from django.contrib import admin
from .models import Bus, Profile

# Register your models here.
class BusAdmin(admin.ModelAdmin):
        exclude = ('rem',)

admin.site.register(Bus, BusAdmin)
admin.site.register(Profile)