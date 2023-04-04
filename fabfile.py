import os
from contextlib import contextmanager
from fabric.api import cd, env, prefix, run, sudo, task, put
from fabric.contrib import files

PROJECT_NAME = 'mrcake'
PROJECT_ROOT = '/var/www/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, 'venv')
REPO = 'git@github.com:sgmagar/cakeg.git'

env.hosts = []

@task
def staging():
    env.hosts = ['root@staging-server']
    env.environment = 'staging'


@task
def production():
    env.hosts = ['root@159.89.201.92']
    env.environment = 'production'


@contextmanager
def source_virtualenv():
    with prefix('source ' + os.path.join(VENV_DIR, 'bin/activate')):
        yield

def clean():
    """Cleans Python bytecode"""
    sudo('find . -name \'*.py?\' -exec rm -rf {} \;')


def chown():
    """Sets proper permissions"""
    sudo('chown -R www-data:www-data %s' % PROJECT_ROOT)

def restart():
    sudo("systemctl restart {}_gunicorn".format(PROJECT_NAME))
    sudo('systemctl restart nginx')

def reload_daemon():
    sudo("systemctl daemon-reload")


def update_env():
    put(".prod_env", "{}/.env".format(PROJECT_ROOT))

@task
def deploy():
    """
    Deploys the latest tag to the production server
    """
    sudo('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))
    update_env()
    with cd(PROJECT_ROOT):
        run("git checkout master")
        run('git pull origin master')
        with source_virtualenv():
            with prefix('export DJANGO_SETTINGS_MODULE={}.settings.{}'.format(PROJECT_NAME, env.environment)):
                run('source venv/bin/activate && pip install -r requirements/{}.txt'.format(env.environment))
                run('./manage.py migrate')
                run('./manage.py collectstatic --noinput')
    chown()
    restart()


@task
def bootstrap():
    """Bootstrap the latest code at the app servers"""
    sudo(
        'apt-get update && apt-get install git nginx libjpeg8-dev postgresql libpq-dev python-dev python-pip python-virtualenv libfreetype6-dev libncurses5-dev'
    )
    if not files.exists(PROJECT_ROOT):
        sudo('mkdir -p {}'.format(PROJECT_ROOT))
        sudo('chown -R {}:{} {}'.format(env.user, env.user, PROJECT_ROOT))
        run('git clone {} {}'.format(REPO, PROJECT_ROOT))
    update_env()
    with cd(PROJECT_ROOT):
        sudo("mkdir -p logs")
        run('git checkout master')
        run('git pull origin master')
        run('virtualenv venv')
        with source_virtualenv():
            with prefix('export DJANGO_SETTINGS_MODULE={}.settings.{}'.format(PROJECT_NAME, env.environment)):
                run('source venv/bin/activate && pip install -r requirements/{}.txt'.format(env.environment))
                run('./manage.py migrate')
                run('./manage.py collectstatic --noinput')
    chown()
    if not files.exists("/etc/nginx/sites-enabled/{}.conf".format(PROJECT_NAME)):
        sudo('ln -s {project_root}/deployment/{environment}/nginx.conf /etc/nginx/sites-enabled/{project_name}.conf'.format(
            project_root=PROJECT_ROOT, environment=env.environment, project_name=PROJECT_NAME))
    sudo('cp -r {project_root}/deployment/{environment}/gunicorn.service /etc/systemd/system/{project_name}_gunicorn.service'.format(
            project_root=PROJECT_ROOT, environment=env.environment,
            project_name=PROJECT_NAME))

    reload_daemon()
    restart()
