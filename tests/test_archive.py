import filecmp
import os
import unittest

import shutil

from dockersible import archive

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def same_folders(dcmp):
    if dcmp.diff_files:
        return False
    for sub_dcmp in dcmp.subdirs.values():
        return same_folders(sub_dcmp)
    return True


class ArchiveTestCase(unittest.TestCase):
    def test_archive_folder(self):
        source_dir = os.path.join(TEST_DIR, 'archive')
        output_file = 'test.tar.gz'
        archive.tar(source_dir, output_file)
        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file)

    def test_unarchive_folder(self):
        archive_file = os.path.join(TEST_DIR, 'archive.tar.gz')
        restore_folder = os.path.join(TEST_DIR, 'restore')
        archive.untar(archive_file, restore_folder)
        self.assertTrue(same_folders(filecmp.dircmp(
            os.path.join(TEST_DIR, 'archive'),
            os.path.join(TEST_DIR, 'restore', 'archive')))
        )
        shutil.rmtree(restore_folder)

    def test_get_id_in_path(self):
        path = './20151126T120343.d2194465e223685bf1f6bba2e032c30ab28b845635040339403ab0ec42019c1b.tar.gz'
        self.assertEqual(archive.get_volume_name(os.path.abspath(path)),
                         'd2194465e223685bf1f6bba2e032c30ab28b845635040339403ab0ec42019c1b')

    def test_get_name_in_path(self):
        path = './20151126T120343.romantic_heisenberg.tar.gz'
        self.assertEqual(archive.get_volume_name(os.path.abspath(path)), 'romantic_heisenberg')


if __name__ == '__main__':
    unittest.main()
