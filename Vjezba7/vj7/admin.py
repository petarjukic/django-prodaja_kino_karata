from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Ticket, Projection, Person


admin.site.register(Ticket)
#admin.site.register(Person)
admin.site.register(Projection)
# Register your models here.

class PersonAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_admin', 'is_staff', 
            'is_superuser')  # da ispise one sve nazive svojstva
    search_fields = ('email', 'username') # za pretragu
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()




admin.site.register(Person, PersonAdmin)
