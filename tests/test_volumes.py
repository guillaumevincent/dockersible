import unittest
from dockersible.volumes import list_volumes


class VolumesTestCase(unittest.TestCase):
    def test_list_volumes_from_container(self):
        docker_inspect = {
            'Id': 'd2194465e223685bf1f6bba2e032c30ab28b845635040339403ab0ec42019c1b',
            'Config': {
                'Volumes': {
                    '/var/lib/postgresql/data': {}
                },
            },
            'Mounts': [{
                'Source': '/var/lib/docker/volumes/test_postgresql/_data',
                'Mode': 'rw',
                'Propagation': 'rprivate',
                'RW': True,
                'Destination': '/var/lib/postgresql/data',
                'Driver': 'local',
                'Name': 'test_postgresql'
            }]
        }
        volumes = list_volumes(docker_inspect)
        expected_volumes = [{
            'container_id': 'd2194465e223685bf1f6bba2e032c30ab28b845635040339403ab0ec42019c1b',
            'mountpoint': '/var/lib/docker/volumes/test_postgresql/_data',
            'name': 'test_postgresql'
        }]
        self.assertCountEqual(volumes, expected_volumes)


if __name__ == '__main__':
    unittest.main()
