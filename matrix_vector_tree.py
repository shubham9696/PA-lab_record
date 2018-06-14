import threading
import sys
import numpy as np
import os
from queue import Queue
import math


class leafs(threading.Thread):

    def __init__(self,node,val,col,mat,args=(),kwargs=None):
        threading.Thread.__init__(self, args=args, kwargs=kwargs)
        self.node = node
        self.val = val
        self.col = col
        self.mat = mat

    def run(self):
        for i in range(len(self.mat)):
            self.node.put(self.val * self.mat[i][self.col])


class Inodes(threading.Thread):
    def __init__(self,node,lchild,rchild,m,args=(),kwargs=None):
        threading.Thread.__init__(self, args=args, kwargs=kwargs)
        self.node=node
        self.lchild=lchild
        self.rchild=rchild
        self.steps=m

    def run(self):
        while self.steps>0 :
            x1=self.lchild.get()
            x2=self.rchild.get()
            self.node.put(x1+x2)
            self.steps-=1

def main():

    print("Enter the matrix dimensions:-")
    m=int(input())
    n=int(input())

    mat = []

    print("Enter the matrix")

    for i in range(m):
        mat.append(list(map(int,input().split())))

    print("Enter the vector dimensions:")

    v=int(input())

    if v!=n:
        sys.exit("Cannot perform multiplication with given dimensions")

    print("Enter the vector:")
    vec = []
    for i in range(v):
        k=int(input())
        vec.append(k)


    height=math.floor(math.log2(n))+1
    nodes= 1<<height
    nodes-=1

    qnodes =[Queue() for i in range(nodes)]
    tree= []

    for i in range(height):
        nodes_at_level= 1<<i
        for j in range(nodes_at_level):
            k=(nodes_at_level//2)+j
            cur=qnodes[k]
            if i!=height-1:
                lchild=qnodes[2*k+1]
                rchild=qnodes[2*k+2]
                val=Inodes(cur,lchild,rchild,m)
            else:
                y=vec[j]
                val=leafs(cur,y,j,mat)
            val.start()
            tree.append(val)

    tree[0].join()
    print("\nResult:-\n")
    for i in range(m):
        k=tree[0].node.get()
        print(k)
        print(" ")


if __name__ == '__main__':
    main()








