import time
import unittest

import random
from multiprocessing import Process, shared_memory
from concurrent.futures import ProcessPoolExecutor

from shared_memory_toolkit.core import _get_share_memory


def dump_bytes(shm_name: str, random_bytes: bytes):
    shm, lock = _get_share_memory(shm_name)

    shm.buf[:len(random_bytes)] = random_bytes


def load_bytes(shm_name: str) -> bytes:
    shm, lock = _get_share_memory(shm_name)

    return bytes(shm.buf)


def dump_bytes_in_process(shm_name: str, random_bytes: bytes):
    # cannot pickle local function as subprocess
    p = Process(target=dump_bytes, args=(shm_name, random_bytes))
    p.daemon = True
    p.start()
    p.join()


def get_lock_id(shm_name):
    shm, lock = _get_share_memory(shm_name)
    print(id(lock))

    return id(lock)


class CoreTestCase(unittest.TestCase):

    def test_default_property(self):
        """默认的各项属性"""
        from shared_memory_toolkit import core

        with self.subTest('Default FIX_LENGTH: 6220800'):
            assert core.FIX_LENGTH == 6220800

        with self.subTest('Default _share_memory_cache_mapper: empty'):
            assert core._share_memory_cache_mapper == {}

    def test_get_share_memory_same_name(self):
        """_get_share_memory: 相同名字加载相同的共享内存"""
        same_name = 'same_name'

        shm_0, lock_0 = _get_share_memory(same_name)
        shm_1, lock_1 = _get_share_memory(same_name)

        assert lock_0._id == lock_1._id
        assert shm_0.name == shm_1.name

    def test_get_shm_in_different_process(self):
        """主进程创建后，子进程写入，共享内存产生相同变化"""
        random_bytes_content = random.randbytes(1920 * 1080 * 3)

        # 必须由主进程先创建共享内存 否则子进程后退出时会自动销毁
        shm_in_main, lock_main = _get_share_memory('same_name')

        # 子进程写入
        dump_bytes_in_process(shm_name='same_name', random_bytes=random_bytes_content)

        assert bytes(shm_in_main.buf) == random_bytes_content


if __name__ == '__main__':
    unittest.main()
