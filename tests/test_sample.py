import unittest

import random

import numpy

from shared_memory_toolkit import get_share_memory, initial_sync_in_fork, dump_image_into_shared_memory, \
    load_image_from_shared_memory


class Normal_TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.image = numpy.ndarray((1080, 1920, 3), dtype=numpy.uint8)

    def test_get_share_memory(self):
        size = random.randint(10000, 10000000)
        bytes_content = random.randbytes(size)

        shm_name = 'shm_name'
        shm_0, _ = get_share_memory(shm_name, size)

        shm_0.buf[:] = bytes_content

        shm_1, _ = get_share_memory(shm_name)

        assert bytes(shm_0.buf) == bytes(shm_1.buf) == bytes_content

    def test_raw_image(self):
        dump_image_into_shared_memory('t', self.image)

        image = load_image_from_shared_memory('t')

        assert image.tobytes() == self.image.tobytes()


if __name__ == '__main__':
    unittest.main()
