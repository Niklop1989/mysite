from django.core.management import BaseCommand
from shopapp.models import Product

from django.contrib.auth.models import User

from typing import Sequence


class Command(BaseCommand):
    
    def handle(self, *args, **options): 
       
        self.stdout.write('Start demo selection fields')

        users_info = User.objects.values_list('username',flat=True)
        for u_list in users_info:
            print(u_list)

        #products_values = Product.objects.values('pk','name')
        #for p_values in products_values:
        #    print(p_values)

        self.stdout.write('success create order')