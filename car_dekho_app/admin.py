from django.contrib import admin
from .models import CarList, ShowroomList, Review
# Register your models here.

admin.site.register(CarList)
admin.site.register(ShowroomList)
admin.site.register(Review)