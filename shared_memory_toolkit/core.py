# -*- coding: utf-8 -*-
"""The core of shared memory toolkit.

基础的初始化以及最为核心的加载共享内存函数。

全局变量:

    1. FIX_LENGTH::

        共享内存的固定大小，一般美容嗯为图片的大小: 1920 * 1080 * 3 == 6220800

    2. _share_memory_cache_mapper::

        共享内存对象字典，通过此字典来缓存共享内存对象而不需要每次实例化SharedMemory

    3. _share_memory_lock_mapper 和 _manager::

        用于控制共享内存的同步读取/写入


"""
from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Lock
from typing import Dict, Tuple

from .sync import get_shm_lock

FIX_LENGTH: int = 6220800
"""固定数据块（图片）的大小，用于从不定大小的共享内存中获取定长数据，默认为1920*1080*3大小的图片。"""

_share_memory_cache_mapper: Dict[str, SharedMemory] = {}
"""Dict[str, SharedMemory]: 存储共享内存名字和共享内存实体对象的共享内存对象字典"""


def _get_share_memory(shared_memory_name: str) -> Tuple[SharedMemory, Lock]:
    """从共享内存映射表中加载一个共享内存，返回共享内存对象和对应的锁。

    如果不存在（第一次加载）共享内存，则会创建一个FIX_LENGTH大小的共享内存，和相应的锁。

    Note:
        如果不在同一个进程下也可以相互访问共享内存。

    Note:
        如果执行了initial_shared_memory_lock，则会通过一个跨进程字典来使不同进程之间保持同一个锁。

    Args:
        shared_memory_name (str): 共享内存名字。

    Returns:
        Tuple[SharedMemory, Lock]: 共享内存和锁的元组。
    """
    # 获取此操作的锁
    lock = get_shm_lock(shared_memory_name)

    # 从当前进程的共享内存对象字典中获取共享内存对象
    shared = _share_memory_cache_mapper.get(shared_memory_name)

    # case: 当前进程中暂存的共享内存对象字典中不存在该共享内存
    if shared is None:

        with lock:
            # 同步：尝试创建
            # case: 系统中不存在此共享内存，则创建一个新的共享内存区
            try:
                shared = SharedMemory(name=shared_memory_name, create=True, size=FIX_LENGTH)
                assert len(shared.buf) == FIX_LENGTH
            # case: 系统中存在此共享内存，则创建共享内存对象并放入当前进程的共享内存对象字典
            except FileExistsError:
                shared = SharedMemory(name=shared_memory_name, create=False)

            _share_memory_cache_mapper[shared_memory_name] = shared

    # FIXME: 无法删除
    # case: 当前找到的共享内存大小小于FIX_LENGTH，则关闭改共享内存然后重新创建
    # if len(shared.buf) <= FIX_LENGTH:
    #     shared.close()
    #     shared.unlink()
    #     shared = SharedMemory(name=shared_memory_name, create=True, size=FIX_LENGTH)
    #
    #     _share_memory_cache_mapper[shared_memory_name] = shared

    return _share_memory_cache_mapper[shared_memory_name], lock
