import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        exe = os.path.join(settings.PROJECT_DIR, "..", "env", "bin", "python3")  # TODO find env executable
        manage = os.path.join(settings.PROJECT_DIR, "manage.py")
        if os.name == 'nt':
            command = "at 00:01 /every:monday,tuesday,wednesday,thursday,friday,saturday,sunday {} {} cron".format(exe, manage)
            os.system(command)
        else:
            with open("crontabfile", "w") as file:
                content = "1 0 * * * {} {} cron\n".format(exe, manage)
                file.write(content)
            os.system("crontab crontabfile")
            os.remove("crontabfile")
