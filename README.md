# shared_memory_toolkit

A Python shared memory toolkit for process picture between different processes.

#### 2022.6.17 Upgrade: 添加头信息，支持自动转换图片

#### Upgrade: 支持读写不同形状的图片，读写不同大小的共享内存

--- 

### 简单使用

> get_share_memory

包装了SharedMemory功能并且添加了全局锁控制的核心函数。可以创建指定大小的共享内存或者找到一个存在的共享内存，以及对应的锁。

读

```python
from shared_memory_toolkit import get_share_memory

# 读取已存在共享内存
exist_name = 'exist_name'
exist_shm, exist_lock = get_share_memory(exist_name)

with exist_lock:
    bytes_data = bytes(exist_shm.buf)
```

写

```python
from shared_memory_toolkit import get_share_memory

# 创建并且写入共享内存
shm_name = 'shm_name'
size = 10241024

new_shm, new_lock = get_share_memory(shm_name, size)

with new_lock:
    new_shm.buf[:] = bytearray(10241024)
```

#### 初始化锁

根据系统自动创建相应的锁控制逻辑，默认是64个共享内存。

```python
from shared_memory_toolkit import initial_sync_in_fork

# 如果需要更多的共享内存锁
lock_number = 1024

# 如果是fork形式(Linux)
initial_sync_in_fork(lock_number)
```

### 读取图片 - 动态读取

```python
import numpy
from shared_memory_toolkit import dump_image_into_shared_memory, load_image_from_shared_memory

image_hd = numpy.ndarray((1280, 720, 3), dtype=numpy.uint8)
image_1080 = numpy.ndarray((1080, 1920, 3), dtype=numpy.uint8)
        
# 存1080大图片
dump_image_into_shared_memory('image_name', image_1080)

new_image = load_image_from_shared_memory('image_name')

assert new_image.tobytes() == image_1080.tobytes()

# 改存为小图片
dump_image_into_shared_memory('image_name', image_hd)

other_image = load_image_from_shared_memory('image_name')

assert other_image.tobytes() == image_hd.tobytes()

```

#### TODO:

1. base64_image module.
