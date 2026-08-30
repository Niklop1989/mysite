from django.core.management import BaseCommand
from blogapp.models import Article
class Command(BaseCommand):
    """
    Create autors
    """
    def handle(self, *args, **options):
        self.stdout.write("Create products")

        article_names = [
            "Puskin",
            "Nogin",
            "Lopan"
        ]
        for art_name in article_names:
            articl,created = Article.objects.get_or_create(title=art_name)
            self.stdout.write(f'create {article_names}')
        self.stdout.write(self.style.SUCCESS('success'))
   