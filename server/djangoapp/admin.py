from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['carMake', 'dealerId', 'name','type', 'year']

# CarMakeAdmin class with CarModelInline
class CarMakeInline(admin.StackedInline):
    model = CarMake

class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name','description']

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)