# -*- coding: utf-8 -*-
"""进程间同步工具类.

"""
from typing import Dict, List, Tuple, NoReturn
from multiprocessing import Lock, Manager, get_start_method

_lock: Lock = Lock()
"""控制共享内存映射字典的锁"""

_name_index_mapper: Dict[str, int] = {}
"""共享内存名字和锁的映射字典"""

_lock_list: List[Lock] = []
"""锁的列表"""


def get_shm_lock(shm_name) -> Lock:
    """获取共享内存对应的跨进程锁"""

    # 如果没有初始化进程间锁，则会使用默认的锁。
    if not _lock_list:
        return _lock

    # 同步：先查找映射字典中是否有该共享内存
    with _lock:
        # case: 不存在共享内存，则需要创建。
        if shm_name not in _name_index_mapper:
            # 找到最大的序号
            index_values = list(_name_index_mapper.values())
            index_values.sort()

            if not index_values:
                current_index = 0
            else:
                current_index = index_values[-1] + 1

            _name_index_mapper[shm_name] = current_index

    # case: 存在则直接返回对应序号，再根据序号返回得到锁
    return _lock_list[_name_index_mapper[shm_name]]


def initial_sync_in_fork(lock_number: int = 64) -> Tuple[Lock, Dict[str, int], List[Lock]]:
    """Fork方式的启动：只需要调用此方法，子进程自动继承同步对象

    Args:
        lock_number (int, optional): 子进程对应的锁的数量. Defaults to 64.

    Returns:
        Tuple[Lock, Dict[str, int], List[Lock]]: 同步对象
    """
    global _lock, _name_index_mapper, _lock_list
    manager = Manager()

    _lock = manager.Lock()
    _name_index_mapper = manager.dict()
    _lock_list = manager.list([manager.Lock() for _ in range(lock_number)])

    return _lock, _name_index_mapper, _lock_list


def initial_sync_in_spawn(lock_number: int = 64) -> Tuple[Lock, Dict[str, int], List[Lock]]:
    """Spawn方式的启动：需要在主进程先调用此方法，再将同步对象手动放入子进程中。

    Args:
        lock_number (int, optional): 子进程的对应的锁数量. Defaults to 64.

    Returns:
        Tuple[Lock, Dict[str, int], List[Lock]]: 同步对象
    """
    manager = Manager()

    lock = manager.Lock()
    name_index_mapper = manager.dict()
    lock_list = manager.list([manager.Lock() for _ in range(lock_number)])

    return lock, name_index_mapper, lock_list


def synchronization_setter(lock: Lock, name_index_mapper: Dict[str, int], lock_list: List[Lock]) -> NoReturn:
    """用于Spawn启动时，手动传入子进程的同步对象。

    Args:
        lock (Lock): 控制映射表的锁
        name_index_mapper (Dict[str, int]): 子进程的锁的序号映射
        lock_list (List[Lock]): 子进程锁的列表

    """
    global _lock, _name_index_mapper, _lock_list

    _lock = lock
    _name_index_mapper = name_index_mapper
    _lock_list = lock_list


# 自动启动

if get_start_method() == 'fork':
    initial_sync_in_fork(64)
