import time
import unittest
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_start_method, Process

from shared_memory_toolkit.sync import initial_sync_in_spawn, get_shm_lock, synchronization_setter


def process_state(*args):
    synchronization_setter(*args)

    from shared_memory_toolkit.sync import _lock, _lock_list, _name_index_mapper

    return _lock._id, _name_index_mapper._id, _lock_list._id


def process_id(n: str = 'name'):
    lock = get_shm_lock(n)
    return lock._id


@unittest.skipUnless(condition=get_start_method() == 'spawn', reason='spawn')
class SyncSpawnTestCase(unittest.TestCase):
    def test_initial_sync_in_spawn(self):
        syncs = initial_sync_in_spawn()

        with ProcessPoolExecutor(4) as pool:
            sub_results = [pool.submit(process_state, *syncs).result() for _ in range(10)]

        with self.subTest('same lock id'):
            for sub_result in sub_results:
                self.assertEquals(sub_result[0], syncs[0]._id)

        with self.subTest('same mapper id'):
            for sub_result in sub_results:
                self.assertEquals(sub_result[1], syncs[1]._id)

        with self.subTest('same lock_list id'):
            for sub_result in sub_results:
                self.assertEquals(sub_result[2], syncs[2]._id)

    def test_get_shm_lock_same_lock(self):
        """一致的名称返回一致的锁"""
        sync = initial_sync_in_spawn()
        synchronization_setter(*sync)

        lock_0 = get_shm_lock('uuid')
        lock_1 = get_shm_lock('uuid')

        assert lock_0._id == lock_1._id

    def test_get_shm_lock_between_process(self):
        _, d, l = initial_sync_in_spawn()

        from shared_memory_toolkit.sync import synchronization_setter
        with ProcessPoolExecutor(4, initializer=synchronization_setter, initargs=(_, d, l)) as pool:
            futures = [pool.submit(process_id) for _ in range(10)]
            ids = [_.result() for _ in futures]

        [self.assertEquals(_, ids[0]) for _ in ids]


if __name__ == '__main__':
    unittest.main()
