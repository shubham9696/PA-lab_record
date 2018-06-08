import sys
import os
import time
from threading import Thread

#The threading module uses threads, the multiprocessing module uses processes.
# The difference is that threads run in the same memory space, while processes have separate memory.
#  This makes it a bit harder to share objects between processes with multiprocessing.
# Since threads use the same memory, precautions have to be taken or two threads will write to the same memory at the same time.
#  This is what the global interpreter lock is for.
# Spawning processes is a bit slower than spawning threads. Once they are running, there is not much difference.

def quick_sort(arr, left, right):
    i = left
    j = right
    pivot = arr[(left + right) // 2]
    while i <= j:
        while arr[i] < pivot:
            i = i + 1
        while arr[j] > pivot:
            j = j - 1
        if i <= j:
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp
            i = i + 1
            j = j - 1

    lthread = None
    rthread = None

    if left < j:
        lthread = Thread(target=lambda: quick_sort(arr, left, j))
        lthread.start()

    if right > i:
        rthread = Thread(target=lambda: quick_sort(arr, i, right))
        rthread.start()

    if lthread is not None:
        lthread.join()
    if rthread is not None:
        rthread.join()

    return arr


def main():
    print("Enter the elements of the array:")
    arr = list(map(int, input().split()))
    quick_sort(arr, 0, len(arr) - 1)
    print("Sorted array:",arr)


if __name__ == '__main__':
    main()
