from django.core.management import BaseCommand
from shopapp.models import Product
class Command(BaseCommand):
    """
    Create products
    """
    def handle(self, *args, **options):
        self.stdout.write("Create products")

        products_names = [
            "Laptop",
            "Smartphone",
            "Samsung"
        ]
        for product_name in products_names:
            product,created = Product.objects.get_or_create(name=product_name)
            self.stdout.write(f'create {product_name}')
        self.stdout.write(self.style.SUCCESS('success'))
   