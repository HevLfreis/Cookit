import getpass

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Add a user.'

    def handle(self, *args, **options):
        while True:
            username = raw_input('Username: ')
            password = getpass.getpass('Password: ')
            password2 = getpass.getpass('Enter password again: ')

            if password != password2:
                self.stdout.write('Password incorrect')
                break

            elif len(password) < 6:
                self.stdout.write('Password too short, longer than 6 is prefered')
                break

            else:
                try:
                    user = User.objects.create_user(username=username, password=password)
                    self.stdout.write('New user -%s- update successfully' % username)
                except:
                    self.stdout.write('New user -%s- update failed' % username)
                finally:
                    if raw_input('Continue ? [Y/N]: ') == 'N':
                        break





