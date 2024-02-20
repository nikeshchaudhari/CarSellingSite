from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Register)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Owner_Detail)
admin.site.register(Image)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id','car','status')
    list_editable = ('status',)

@admin.register(Favourate)
class FavourateAdmin(admin.ModelAdmin):
    list_display = ('id','user','car_detail','favourate')
    list_editable = ('favourate',)

