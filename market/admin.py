from django.contrib import admin
from .models import (CustomUser,OrderRoom,OrderFood,
                     Motel,Restaurant,Bar,OrderDrinks,DrinksStockOrder)

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Motel)
admin.site.register(OrderRoom)
admin.site.register(Restaurant)
admin.site.register(OrderFood)
admin.site.register(Bar)
admin.site.register(OrderDrinks)
admin.site.register(DrinksStockOrder)
#admin.site.register(AllOrders)