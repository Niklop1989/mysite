from django.core.management import BaseCommand
from shopapp.models import Order,Product
from django.contrib.auth.models import Group,User

from typing import Sequence
from django.db import transaction
from django.db.models import Avg,Max,Min,Count,Sum

class Command(BaseCommand):
    """
    Create new command
    """
  
    def handle(self, *args, **options): 
        #self.stdout.write('Avd')
        #result = Product.objects.filter(name__contains='Smartphone1').aggregate(
        #    Avg('price'),
        #    min_price=Min('price'),
        #    max_price=Max('price'),
        #    count=Count('price')
        # )
        # print(result)

        orders = Order.objects.annotate(
            total = Sum('products__price',default=0),
            products_count = Count('products')
        )
        for order in orders:
            print(
                f' order {order.id}'
                f' with {order.products_count}'
                f' sum {order.total}'
            )

        self.stdout.write('done')