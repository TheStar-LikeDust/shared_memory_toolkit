# shared_memory_toolkit

A Python shared memory toolkit for process picture between different processes.

# Upgrade: 支持读写不同形状的图片，读写不同大小的共享内存

### How to use

main process - 主进程

```python
from shared_memory_toolkit import load_image_from_shared_memory, dump_image_into_shared_memory

# load image
import cv2

raw_image = cv2.imread('image')

image_shm_name = 'camera_1817'
dump_image_into_shared_memory(image_shm_name, raw_image)

# in other process

image = load_image_from_shared_memory('camera_1817')

# raw_image == image
```

#### TODO:

1. base64_image module.
