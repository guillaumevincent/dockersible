def list_volumes(docker_inspect):
    volumes = []
    for mount in docker_inspect['Mounts']:
        volumes.append({
            'container_id': docker_inspect['Id'],
            'name': mount['Name'],
            'mountpoint': mount['Source']
        })
    return volumes
