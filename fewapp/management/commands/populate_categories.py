from typing import Any
from fewapp.models import Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command inserts category data"

    def handle(self, *args: any, **options: any):
        #delete existing data
        Category.objects.all().delete()
     
        categories = ['Sports', 'Technology', 'Science', 'Arts', 'Food']


        for category_name in categories:
            Category.objects.create(name = category_name)           
        self.stdout.write(self.style.SUCCESS("Completed inserting data"))
