#/bin/bash
export GPU_LIBRARY_PATH=/usr/local/cuda-11.7/targets/x86_64-linux/lib  
export GPU_INCLUDE_PATH=/usr/local/cuda-11.7/targets/x86_64-linux/include/



make DEVICE=GPU API=CUDA CARD=NVIDIA NUMWI=64