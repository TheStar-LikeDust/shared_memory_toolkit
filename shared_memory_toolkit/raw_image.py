# -*- coding: utf-8 -*-
"""numpy格式图片的读取和写入。


全局变量:

    1. IMAGE_SHAPE

函数:

    1. dump_image_into_shared_memory::

        Dump image

    2. load_image_from_shared_memory::

        Load image

Note:

    可跨进程使用


"""
import numpy

from .core import _get_share_memory, FIX_LENGTH

IMAGE_SHAPE = (1080, 1920, 3)
"""图像的默认形状"""


def dump_image_into_shared_memory(shared_memory_name: str, image: numpy.ndarray) -> memoryview:
    """将当前的图片dump成共享内存放入当前的共享内存映射中，此操作加锁

    Args:
        shared_memory_name (str): 共享内存名
        image (numpy.ndarray): numpy格式图片

    Returns:
        memoryview: 内存对象（共享内存的.buf属性）
    """
    shared_memory, lock = _get_share_memory(shared_memory_name)

    with lock:
        shared_memory.buf[:FIX_LENGTH] = image.tobytes()
    return shared_memory.buf


def load_image_from_shared_memory(shared_memory_name: str) -> numpy.ndarray:
    """从当前的共享内存映射中读取相应的共享内存并转换为图像，此操作加锁

    Args:
        shared_memory_name (str): 共享内存名

    Returns:
        numpy.ndarray: numpy格式图片
    """
    shared_memory, lock = _get_share_memory(shared_memory_name)

    with lock:
        image = numpy.frombuffer(shared_memory.buf, dtype=numpy.uint8)[:FIX_LENGTH].reshape(IMAGE_SHAPE)
    return image
