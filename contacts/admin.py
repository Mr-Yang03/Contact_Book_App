from django.contrib import admin
from .models import Contact, Group

# Register your models here.
class ContactTable(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')

admin.site.register(Contact, ContactTable)
admin.site.register(Group)