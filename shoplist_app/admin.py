from django.contrib import admin
from .models import StorageLoc, ShopDept, Item, Meal

admin.site.register(StorageLoc)
admin.site.register(ShopDept)
admin.site.register(Item)
admin.site.register(Meal)
