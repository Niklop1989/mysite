from django.core.management import BaseCommand
from shopapp.models import Order,Product
from django.contrib.auth.models import Group,User



class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write('no order')
            return

        products = Product.objects.all()
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(self.style.SUCCESS('Successfully added order '
                                             f'{order.products.all()} to order {order}'))
