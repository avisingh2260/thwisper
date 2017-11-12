#!/usr/bin/env python
import os
import sys
PORT = int(os.getenv('VCAP_APP_PORT', '8000'))
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wypeak.settings")

    from django.core.management import execute_from_command_line
  #  sys.argv.append('0.0.0.0:' + str(PORT))
    execute_from_command_line(sys.argv + ['0.0.0.0:' + str(PORT)])
    