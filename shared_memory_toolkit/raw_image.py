# -*- coding: utf-8 -*-
"""numpy格式图片的读取和写入。

全局变量:

    1. IMAGE_SHAPE: 默认图片的形状

函数:

    1. dump_image_into_shared_memory: Dump image
    2. load_image_from_shared_memory: Load image

TODO:

    1. 基于shm的numpy数组
"""
from typing import Tuple
from multiprocessing.shared_memory import SharedMemory

import numpy

from .core import get_share_memory, FIX_LENGTH

DEFAULT_IMAGE_SHAPE: Tuple[int, int, int] = (1080, 1920, 3)
"""图像的默认形状"""

get_image_size = lambda x: x[0] * x[1] * x[2]
"""获取图像大小"""


def dump_image_into_shared_memory(
        shared_memory_name: str,
        image: numpy.ndarray,
        memory_size: int = get_image_size(DEFAULT_IMAGE_SHAPE),
) -> SharedMemory:
    """将当前的图片dump成共享内存放入当前的共享内存映射中，此操作加锁

    Args:
        shared_memory_name (str): 共享内存名
        image (numpy.ndarray): numpy格式图片
        memory_size (int): 图片格式大小，默认为默认图像形状的大小. Default is 6220800

    Returns:
        SharedMemory: 共享内存对象
    """
    shared_memory, lock = get_share_memory(shared_memory_name, memory_size)

    with lock:
        shared_memory.buf[:FIX_LENGTH] = image.tobytes()
    return shared_memory


def load_image_from_shared_memory(
        shared_memory_name: str,
        image_shape: Tuple[int, int, int] = DEFAULT_IMAGE_SHAPE,
) -> numpy.ndarray:
    """从当前的共享内存映射中读取相应的共享内存并转换为图像，此操作加锁

    Args:
        shared_memory_name (str): 共享内存名
        image_shape (Tuple[int, int, int]): 默认图像形状. Default is (1080, 1920, 3)

    Returns:
        numpy.ndarray: numpy格式图片
    """
    shared_memory, lock = get_share_memory(shared_memory_name)

    with lock:
        image = numpy.frombuffer(shared_memory.buf, dtype=numpy.uint8)[:get_image_size(image_shape)].reshape(
            image_shape)
    return image
