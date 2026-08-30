from django.core.management import BaseCommand
from shopapp.models import Order,Product
from django.contrib.auth.models import Group,User

from typing import Sequence
from django.db import transaction


class Command(BaseCommand):
    """
    Create new command
    """
    # transaction.atomic если будет ошибка
    #  то команда не выполниться даже частично
    #@transaction.atomic
    def handle(self, *args, **options): 
        with transaction.atomic():
            self.stdout.write('Create order with product')
            user = User.objects.get(username='admin')
                                                # or defer
            products:Sequence[Product]=Product.objects.only('id').all()
            order,created = Order.objects.get_or_create(
                delivery_address='Brynsk',
                promocode="asdsd3",
                user=user,
            )
            for product in products:
                order.products.add(product)
            order.save()    
            self.stdout.write(f'Create new order {order}')
        self.stdout.write(self.style.SUCCESS('success create order'))