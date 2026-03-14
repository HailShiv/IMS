from django.contrib import admin
from .models import User
from stores.models import Warehouse

admin.site.register(User)
admin.site.register(Warehouse)
