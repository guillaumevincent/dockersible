import os

import sys

import click
import docker
import docker.errors

from dockersible import archive

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

docker_client = docker.Client(base_url='unix://var/run/docker.sock')


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Simple docker management scripts"""

    euid = os.geteuid()
    if euid != 0:
        click.echo(click.style('dockersible not started as root. You should run as root.', fg='yellow'))
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *args)


@cli.command('backup', short_help='backup one or more container')
@click.argument('container_names', nargs=-1, required=True)
@click.option('-o', '--output', help='output folder to save the backups', metavar='<directory>')
def backup(container_names, output):
    """Backup one or more container.

    a python script to backup docker volumes.


Example:


    \b
    # backup container with short id d6c0fe130dba in current working directory
    dockersible backup d6c0fe130dba

    \b
    # backup romantic_heisenberg named container inside /tmp folder
    dockersible backup romantic_heisenberg --output /tmp

    \b
    # backup container_id1 and container_id2 inside /tmp folder
    dockersible backup <container_id1> <container_id2> --output /tmp
    """
    if not output:
        output = os.getcwd()

    if not os.path.isdir(output):
        raise click.UsageError('--output option should be an existing folder. Leave empty to use current working dir.')

    for container_name in container_names:
        try:
            container_inspect = docker_client.inspect_container(container_name)
            archive.archive_volumes(container_inspect, output)
        except docker.errors.NotFound:
            click.echo(click.style('error container %s not found. ignore this one ...' % container_name, fg='red'))
        except Exception as e:
            print(e)
            click.echo(click.style('unknown error while archiving container %s' % container_name, fg='red'))


@cli.command('restore', short_help='restore one container')
@click.argument('container_name', required=True)
@click.option('-b', '--backup', help='backup file to restore', required=True)
def restore(container_name, backup):
    """Restore one container.

stop container and restore dockersible backup. Backup name is important.
The expected format is important <datetime>.<volume_id|volume_name>.tar.gz



Example:


    \b
    # restore backup 20151126T120343.romantic_heisenberg.tar.gz for romantic_heisenberg named container
    dockersible restore --backup 20151126T120343.romantic_heisenberg.tar.gz romantic_heisenberg
    """
    if not os.path.isfile(backup) or not backup.endswith('tar.gz'):
        raise click.UsageError('--backup option should be a tar.gz archive')

    try:
        container_inspect = docker_client.inspect_container(container_name)
        click.echo(click.style('stopping %s' % container_name, fg='yellow'))
        docker_client.stop(container_name)
        archive.restore_volume(container_inspect, backup)
        click.echo('restarting %s' %container_name)
        docker_client.restart(container_name)
        click.echo(click.style('container %s restarted, and restore done !' % container_name, fg='green'))
    except docker.errors.NotFound:
        click.echo(click.style('error container %s not found. ignore this one ...' % container_name, fg='red'))
    except Exception as e:
        print(e)
        click.echo(click.style('unknown error while restoring container %s' % container_name, fg='red'))
