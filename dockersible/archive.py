import datetime
import os
import tarfile

import re

import shutil

import click
from dockersible.volumes import list_volumes


def tar(source_dir, output_file):
    with tarfile.open(output_file, "w:gz") as tar_file:
        tar_file.add(source_dir, arcname=os.path.basename(source_dir))


def untar(archive_file, output_dir):
    with tarfile.open(archive_file) as tar_file:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar_file, os.path.abspath(output_dir))


def archive_volumes(docker_inspect, output_folder):
    volumes = list_volumes(docker_inspect)
    datetime_now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')
    for volume in volumes:
        backup_name = '{datetime_now}.{volume_name}.tar.gz'.format(datetime_now=datetime_now,
                                                                   volume_name=volume['name'])
        backup_file_path = os.path.join(output_folder, backup_name)
        click.echo('backuping %s' % volume['name'])
        tar(volume['mountpoint'], backup_file_path)
        click.echo(click.style('backup ok : %s' % backup_file_path, fg='green'))


def get_volume_name(path):
    basename = os.path.basename(path)
    name = re.sub('\.tar\.gz$', '', basename)
    try:
        return name.split('.')[1]
    except Exception as e:
        click.echo(click.style('%s is not a dockersible backup, dockersible restore --help' % basename, fg='red'))
    return basename


def empty_dir(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def restore_volume(docker_inspect, backup_file):
    volumes = list_volumes(docker_inspect)

    for volume in volumes:
        volume_name = get_volume_name(backup_file)
        if volume['name'] == volume_name:
            empty_dir(volume['mountpoint'])
            untar(backup_file, volume['mountpoint'])
