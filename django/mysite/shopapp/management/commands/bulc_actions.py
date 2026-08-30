from django.core.management import BaseCommand
from shopapp.models import Product,Order
from django.contrib.auth.models import User
from typing import Sequence
from django.db import transaction


class Command(BaseCommand):
    """
    Create new command
    """
    # transaction.atomic если будет ошибка
    #  то команда не выполниться даже частично

    def handle(self, *args, **options):
        self.stdout.write('Start demo bulk actions')

        # update product
        result = Product.objects.filter(
            name__contains='Smartphone',
        ).update(discount=10)
        print(result)





         # create new prod
        #info = [
        #    ("Smartphone1",199),
        #     ("Smartphone2",1199),
        #      ("Smartphone3",499)
        #]
        #products = [
        #    Product(name=name,price=price)
        #    for name,price in info
        #]
        #res = Product.objects.bulk_create(products)
        #for obj in res:
        #    print(obj)
        self.stdout.write(f'Done')