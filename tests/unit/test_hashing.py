import unittest

from app.utils.hashing import Hash


class TestHash(unittest.TestCase):
    def test_bcrypt_str(self):
        self.assertIsNotNone(Hash.bcrypt('password'))

    def test_bcrypt_not_str(self):
        with self.assertRaises(TypeError):
            Hash.bcrypt(None)

        with self.assertRaises(TypeError):
            Hash.bcrypt(1)

    def test_verifies_true(self):
        assert Hash.verify('password', Hash.bcrypt('password')) is True

    def test_verifies_false(self):
        assert Hash.verify('password2', Hash.bcrypt('password')) is False
