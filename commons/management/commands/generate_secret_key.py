from django.core.management import utils
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generates new Secret Key"

    def handle(self, *args, **kwargs):
        key = utils.get_random_secret_key()
        self.stdout.write(self.style.SUCCESS(key))
