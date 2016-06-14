import os
import unittest

from click.testing import CliRunner
from dockersible.main import cli


class CliTestCase(unittest.TestCase):
    def test_backup_without_container_raise_error(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['backup'])
        self.assertEqual(result.exit_code, 2)

    def test_backup_one_container(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['backup', 'd6c0fe130dba'])
        self.assertEqual(result.exit_code, 0)

    def test_backup_two_containers(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['backup', 'd6c0fe130dba', 'e130dbad6c0f'])
        self.assertEqual(result.exit_code, 0)

    def test_backup_with_output_folder_raise_error_if_not_dir(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['backup', 'romantic_heisenberg', '--output', 'not_a_folder'])
        self.assertEqual(result.exit_code, 2)

    def test_backup_order_doesnt_matter(self):
        runner = CliRunner()
        cwd = os.path.dirname(os.path.realpath(__file__))
        result = runner.invoke(cli, ['backup', 'romantic_heisenberg', '--output', cwd])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ['backup', '--output', cwd, 'romantic_heisenberg'])
        self.assertEqual(result.exit_code, 0)

    def test_restore_without_container_raise_error(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['restore'])
        self.assertEqual(result.exit_code, 2)

    def test_restore_without_backup_file_raise_error(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['restore', 'container_name'])
        self.assertEqual(result.exit_code, 2)

    def test_restore_without_existing_backup_file_raise_error(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['restore', 'container_name', '--backup', 'not_a_backup_file.tar.gz'])
        self.assertEqual(result.exit_code, 2)

    def test_restore_without_tar_gz_raise_error(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['restore', 'container_name', '--backup', 'archive/1.txt'])
        self.assertEqual(result.exit_code, 2)

    def test_restore_ok(self):
        runner = CliRunner()
        archive_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive.tar.gz')
        result = runner.invoke(cli, ['restore', 'container_name', '--backup', archive_path])
        self.assertEqual(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main()
