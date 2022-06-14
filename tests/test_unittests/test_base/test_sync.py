import unittest

from shared_memory_toolkit.sync import get_shm_lock


class MyTestCase(unittest.TestCase):
    def test_get_shm_lock_without_initial(self):
        """不初始化"""

        lock_0 = get_shm_lock('test_memory_0')
        lock_1 = get_shm_lock('test_memory_1')

        assert lock_0 == lock_1


if __name__ == '__main__':
    unittest.main()
