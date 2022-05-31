import time
import unittest

import random
from multiprocessing import Process, shared_memory

from shared_memory_toolkit.core import initial_shared_memory_lock, _get_share_memory


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


class MyTestCase(unittest.TestCase):
    def test_get_share_memory_same_name(self):
        """_get_share_memory: same name with same shared memory."""

        same_name = 'same_name'

        shm_0, lock_0 = _get_share_memory(same_name)
        shm_1, lock_1 = _get_share_memory(same_name)

        assert lock_0 == lock_1

        assert shm_0.name == shm_1.name

    def test_get_shm_in_different_process(self):
        """主进程创建后，子进程写入，共享内存产生相同变化"""
        random_bytes_content = random.randbytes(1920 * 1080 * 3)

        # 主进程创建共享内存 否则子进程后退出时会自动销毁
        shm_in_main, lock_main = _get_share_memory('same_name')

        dump_bytes_in_process(shm_name='same_name', random_bytes=random_bytes_content)

        assert bytes(shm_in_main.buf) == random_bytes_content


if __name__ == '__main__':
    unittest.main()
