import unittest

import numpy

from shared_memory_toolkit import load_image_from_shared_memory, dump_image_into_shared_memory


class MyTestCase(unittest.TestCase):

    def test_dynamic_image(self):
        image_hd = numpy.ndarray((1280, 720, 3), dtype=numpy.uint8)
        image_1080 = numpy.ndarray((1080, 1920, 3), dtype=numpy.uint8)
        image_4k = numpy.ndarray((3840, 2160, 3), dtype=numpy.uint8)

        image_name = 'common'

        dump_image_into_shared_memory(image_name, image_1080)

        assert load_image_from_shared_memory(image_name).tobytes() == image_1080.tobytes()

        dump_image_into_shared_memory(image_name, image_hd)

        assert load_image_from_shared_memory(image_name).tobytes() == image_hd.tobytes()

        with self.subTest('oversize'):
            with self.assertRaises(ValueError) as ve:
                dump_image_into_shared_memory(image_name, image_4k)
                assert load_image_from_shared_memory(image_name).tobytes() == image_4k.tobytes()

        # 设置巨大的内存空间
        big_image = 'big_image'
        dump_image_into_shared_memory(big_image, image_hd, 200000000)
        dump_image_into_shared_memory(big_image, image_1080, 200000000)
        dump_image_into_shared_memory(big_image, image_4k, 200000000)


if __name__ == '__main__':
    unittest.main()
