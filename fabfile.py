from contextlib import contextmanager
from fabric.api import *


@hosts('root@roboclub.org')
@with_settings(no_keys=True)
def deploy():
    code_dir = '/var/www/crm'
    with cd(code_dir), \
         prefix('export WORKON_HOME=/var/www/env/'), \
         prefix('export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.4'), \
         prefix('source /usr/local/bin/virtualenvwrapper.sh'), \
         prefix('workon crm'):

        run('git status')
        run('git pull')
        run('pip install -r requirements.txt')
        run('./manage.py migrate')
        run('touch crm/wsgi.py')
