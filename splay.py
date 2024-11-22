from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

class SplayForest():
    def  __init__(self,
                  roots : None):
        self.roots = roots

    def newtree(self,treename):
        self.roots[treename] = None

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!!!
    def dump(self):
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.roots == None:
            dict_repr = {}
        else:
            dict_repr = {}
            for t in self.roots:
                if self.roots[t] is not None:
                    dict_repr[t] = _to_dict(self.roots[t])
        print(json.dumps(dict_repr,indent = 2))

    # returns the IOP, IOS, or the node with the key
    def bstSearch(self,root:Node,key:int):
        if root.key == key:
            return root
        elif root.key < key:
            if not root.rightchild:
                return root
            return self.bstSearch(root.rightchild,key)
        else:
            if not root.leftchild:
                return root
            return self.bstSearch(root.leftchild,key)

    # splay
    def splay(self,treename:str,root:Node,key:int):
        aboveRoot = root.parent
        y = self.bstSearch(root,key)   # y is node to bring to root
        while(y.parent != aboveRoot):       # while y is not the root
            if y.parent == root:    # if y is child of root, zig
                self.zig(treename,y)
            # if it requires zig zag
            elif ((y.parent.parent.leftchild == y.parent and y.parent.rightchild == y)
                or (y.parent.parent.rightchild == y.parent and y.parent.leftchild == y)):
                self.zigzag(treename,y)
            # otherwise it requires zigzig
            else:
                self.zigzig(treename,y)
        return

    # assume zig is only called if the node has a valid parent
    def zig(self,treename:str,node:Node):
        # parent is old parent; reassign node.parent to be gparent
        parent = node.parent
        node.parent = parent.parent
        # if node is left child of parent
        if node == parent.leftchild:
            tempRight = node.rightchild
            node.rightchild = parent
            if (parent.parent):
                # if parent is the left child of gparent
                if (parent.parent.leftchild == parent):
                    parent.parent.leftchild = node
                else:
                    parent.parent.rightchild = node
            parent.parent = node
            parent.leftchild = tempRight
            if (tempRight):
                tempRight.parent = parent
        # else node is right child of parent
        else:
            tempLeft = node.leftchild
            node.leftchild = parent
            if (parent.parent):
                # if parent is the left child of gparent
                if (parent.parent.leftchild == parent):
                    parent.parent.leftchild = node
                else:
                    parent.parent.rightchild = node
            parent.parent = node
            parent.rightchild = tempLeft
            if (tempLeft):
                tempLeft.parent = parent
        # is node new root?
        if node.parent == None:         
            self.roots[treename] = node
    

    def zigzag(self,treename:str,node:Node):
        self.zig(treename,node)
        self.zig(treename,node)


    def zigzig(self,treename:str,node:Node):
        self.zig(treename,node.parent)
        self.zig(treename,node)

    
    # Search:
    # Search for the key or the last node before we fall out of the tree.
    # Splay that node.
    def search(self,treename: str,key:int):
        self.splay(treename,self.roots[treename],key)


    # Insert Type 1:
    # The key is guaranteed to not be in the tree.
    # Call splay(x) and respond according to whether we get the IOP or IOS.
    def insert(self,treename:str,key:int):
        newNode = Node(key, None, None, None)

        # if this is an empty tree
        if (self.roots[treename] == None):
            self.roots[treename] = newNode
            return

        # otherwise this is an existing tree
        self.splay(treename,self.roots[treename],key)

        # splayNode is the splayed node aka current root
        splayNode = self.roots[treename]

        # if splayNode is the IOS
        if (newNode.key < splayNode.key):
            if (splayNode.leftchild):
                newNode.leftchild = splayNode.leftchild
                newNode.leftchild.parent = newNode
            newNode.rightchild = splayNode
            splayNode.leftchild = None
        # else splayNode is the IOP
        else:
            if (splayNode.rightchild):   
                newNode.rightchild = splayNode.rightchild
                newNode.rightchild.parent = newNode
            newNode.leftchild = splayNode
            splayNode.rightchild = None
        splayNode.parent = newNode
        self.roots[treename] = newNode


    # Delete Type 1:
    # The key is guarenteed to be in the tree.
    # Call splay(key) and then respond accordingly.
    # If key (now at the root) has two subtrees call splay(key) on the right one.
    def delete(self,treename:str,key:int):
        self.splay(treename,self.roots[treename],key)
        delNode = self.roots[treename]
        # if root only has left subtree
        if (delNode.leftchild and not delNode.rightchild):
            self.roots[treename] = delNode.leftchild
            delNode.leftchild.parent = None
        elif (delNode.rightchild and not delNode.leftchild):
            self.roots[treename] = delNode.rightchild
            delNode.rightchild.parent = None
        else:
            self.splay(treename,delNode.rightchild,key)
            delNode.rightchild.leftchild = delNode.leftchild
            delNode.leftchild.parent = delNode.rightchild
            self.roots[treename] = delNode.rightchild
            delNode.rightchild.parent = None
            