# shared_memory_toolkit

A Python shared memory toolkit for process picture between different processes.

### How to use

main process - 主进程

```python
# optional
import cv2
from shared_memory_toolkit import dump_image_into_shared_memory

image = cv2.imread('test.pic')
dump_image_into_shared_memory('uuid_content', image)
```

sub process - 子进程

```python
from shared_memory_toolkit import load_image_from_shared_memory

# ... some other codes

image = load_image_from_shared_memory('uuid_content')
```

主进程和子进程中的image将会完全保持一致：由同样的bytes转换而来。

#### TODO:

1. unittest for raw_image.
2. base64_image module.
3. README and docs.
