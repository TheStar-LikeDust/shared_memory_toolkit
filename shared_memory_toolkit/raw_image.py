# -*- coding: utf-8 -*-
"""numpy格式图片的读取和写入。

全局变量:

    1. IMAGE_SHAPE: 默认图片的形状

函数:

    1. dump_image_into_shared_memory: Dump image
    2. load_image_from_shared_memory: Load image

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
        memory_size: int = FIX_LENGTH,
) -> SharedMemory:
    """将当前的图片dump成共享内存放入当前的共享内存映射中，此操作加锁

    Args:
        shared_memory_name (str): 共享内存名
        image (numpy.ndarray): numpy格式图片
        memory_size (int): 图片格式大小，默认为默认图像形状的大小. Default is 6220800

    Returns:
        SharedMemory: 共享内存对象
    """

    # 获取图片大小 如果指定的大小过小, 则会自动扩大
    image_size: int = get_image_size(image.shape)
    shm_size: int = max(image_size + 14, memory_size)

    # 找到共享内存
    shared_memory, lock = get_share_memory(shared_memory_name, shm_size)

    # 构建头部信息
    bytes_content = bytes().join(
        [
            # 图片数据大小
            image_size.to_bytes(8, 'big'),
            # 图片形状 三维
            int(image.shape[0]).to_bytes(2, 'big'),
            int(image.shape[1]).to_bytes(2, 'big'),
            int(image.shape[2]).to_bytes(2, 'big'),
            # 图片数据
            image.tobytes(),
            # 剩余长度需要填充空字节
            bytearray(abs(shm_size - 14 - image_size))
        ]
    )

    with lock:
        shared_memory.buf[:shm_size] = bytes_content
    return shared_memory


def load_image_from_shared_memory(
        shared_memory_name: str
) -> numpy.ndarray:
    """从当前的共享内存映射中读取相应的共享内存并转换为图像，此操作加锁

    Args:
        shared_memory_name (str): 共享内存名

    Returns:
        numpy.ndarray: numpy格式图片
    """
    shared_memory, lock = get_share_memory(shared_memory_name)

    with lock:
        # 重建头部信息
        # 图片大小
        image_size = int.from_bytes(shared_memory.buf[:8], 'big')

        # 图片形状
        image_shape_0 = int.from_bytes(shared_memory.buf[8:10], 'big')
        image_shape_1 = int.from_bytes(shared_memory.buf[10:12], 'big')
        image_shape_2 = int.from_bytes(shared_memory.buf[12:14], 'big')
        image_shape = (image_shape_0, image_shape_1, image_shape_2)

        # 图片字节数据 整体偏移14个字节
        # image_bytes_content = shared_memory.buf[14:image_size + 14]
        image = numpy.frombuffer(shared_memory.buf[14:image_size + 14], dtype=numpy.uint8).reshape(
            image_shape)
    return image
