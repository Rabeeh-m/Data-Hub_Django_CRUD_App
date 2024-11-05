from django.contrib import admin # type: ignore

# Register your models here.

from . models import Record

admin.site.register(Record)
