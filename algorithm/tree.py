# coding=gbk
"""
节点类
"""
class Node(object):

    def __init__(self, elem=-1, lchild=None, rchild=None):
        self.elem = elem
        self.lchild = lchild
        self.rchild = rchild

"""
树类
"""
class Tree(object):

    def __init__(self):
        self.root = Node()

    """
    为树添加节点
    """
    def add(self, elem):
        node = Node(elem)
        if self.root.elem == -1:            #如果树是空的，则对根节点赋值
            self.root = node
        else:
            myQueue = []
            treeNode = self.root
            myQueue.append(treeNode)
            while myQueue:                      #对已有的节点进行层次遍历
                treeNode = myQueue.pop(0)
                if treeNode.lchild == None:
                    treeNode.lchild = node
                    return
                elif treeNode.rchild == None:
                    treeNode.rchild = node
                    return
                else:
                    myQueue.append(treeNode.lchild)
                    myQueue.append(treeNode.rchild)

    """
    利用递归实现树的先序遍历
    """
    def front_digui(self, root):

        if root == None:
            return
        print(root.elem)
        self.front_digui(root.lchild)
        self.front_digui(root.rchild)

    """
    利用递归实现树的中序遍历
    """
    def middle_digui(self, root):
        if root == None:
            return
        self.middle_digui(root.lchild)
        print(root.elem)
        self.middle_digui(root.rchild)

    """
    利用递归实现树的后序遍历
    """
    def later_digui(self, root):
        if root == None:
            return
        self.later_digui(root.lchild)
        self.later_digui(root.rchild)
        print(root.elem)

    """
    利用堆栈实现树的先序遍历
    """
    def front_stack(self, root):
        if root == None:
            return
        myStack = []
        node = root
        while node or myStack:
            while node:                     #从根节点开始，一直找它的左子树
                print(node.elem)
                myStack.append(node)
                node = node.lchild
            node = myStack.pop()            #while结束表示当前节点node为空，即前一个节点没有左子树了
            node = node.rchild                  #开始查看它的右子树

    """
    利用堆栈实现树的中序遍历
    """
    def middle_stack(self, root):
        if root == None:
            return
        myStack = []
        node = root
        while node or myStack:
            while node:                     #从根节点开始，一直找它的左子树
                myStack.append(node)
                node = node.lchild
            node = myStack.pop()            #while结束表示当前节点node为空，即前一个节点没有左子树了
            print(node.elem)
            node = node.rchild                  #开始查看它的右子树

    """
    利用堆栈实现树的后序遍历
    """
    def later_stack(self, root):
        if root == None:
            return
        myStack1 = []
        myStack2 = []
        node = root
        myStack1.append(node)
        while myStack1:                   #这个while循环的功能是找出后序遍历的逆序，存在myStack2里面
            node = myStack1.pop()
            if node.lchild:
                myStack1.append(node.lchild)
            if node.rchild:
                myStack1.append(node.rchild)
            myStack2.append(node)
        while myStack2:                         #将myStack2中的元素出栈，即为后序遍历次序
            print(myStack2.pop().elem)

    """
    利用队列实现树的层次遍历
    """
    def level_queue(self, root):
        if root == None:
            return
        myQueue = []
        node = root
        myQueue.append(node)
        while myQueue:
            node = myQueue.pop(0)
            print(node.elem)
            if node.lchild != None:
                myQueue.append(node.lchild)
            if node.rchild != None:
                myQueue.append(node.rchild)

"""
二分查找树
"""
class TreeNode(object):
    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

    def hasLeftChild(self):
        return self.left

    def hasRightChild(self):
        return self.right

    def isLeftChild(self):
        return self.parent and self.parent.left == self

    def isRightChild(self):
        return self.parent and self.parent.right == self


class BSTree(object):
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def insert(self, x):
        node = TreeNode(x)
        if not self.root:
            self.root = node
            self.size += 1
        else:
            currentNode = self.root
            while True:
                if x < currentNode.key:
                    if currentNode.left:
                        currentNode = currentNode.left
                    else:
                        currentNode.left = node
                        node.parent = currentNode
                        self.size += 1
                        break
                elif x > currentNode.key:
                    if currentNode.right:
                        currentNode = currentNode.right
                    else:
                        currentNode.right = node
                        node.parent = currentNode
                        self.size += 1
                        break
                else:
                    break

    def find(self, key):
        if self.root:
            res = self._find(key, self.root)
            if res:
                return res
            else:
                return None
        else:
            return None

    def _find(self, key, node):
        if not node:
            return None
        elif node.key == key:
            return node
        elif key < node.key:
            return self._find(key, node.left)
        else:
            return self._find(key, node.right)

    def findMin(self):
        if self.root:
            current = self.root
            while current.left:
                current = current.left
            return current
        else:
            return None

    def _findMin(self, node):
        if node:
            current = node
            while current.left:
                current = current.left
            return current

    def findMax(self):
        if self.root:
            current = self.root
            while current.right:
                current = current.right
            return current
        else:
            return None

    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self.find(key)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size -= 1
            else:
                print("Error, key not in tree", KeyError)
                raise
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('Error, key not in tree')

    def remove(self, node):
        if not node.left and not node.right:  # node为树叶
            if node == node.parent.left:
                node.parent.left = None
            else:
                node.parent.right = None

        elif node.left and node.right:  # 有两个儿子
            minNode = self._findMin(node.right)
            node.key = minNode.key
            self.remove(minNode)

        else:  # 有一个儿子
            if node.hasLeftChild():
                if node.isLeftChild():
                    node.left.parent = node.parent
                    node.parent.left = node.left
                elif node.isRightChild():
                    node.left.parent = node.parent
                    node.parent.right = node.left
                else:  # node为根
                    self.root = node.left
                    node.left.parent = None
                    node.left = None
            else:
                if node.isLeftChild():
                    node.right.parent = node.parent
                    node.parent.left = node.right
                elif node.isRightChild():
                    node.right.parent = node.parent
                    node.parent.right = node.right
                else:  # node为根
                    self.root = node.right
                    node.right.parent = None
                    node.right = None


class RBTree:
    def __init__(self):
        self.nil = RBTreeNode(0)
        self.root = self.nil

class RBTreeNode:
    def __init__(self, x):
        self.key = x
        self.left = None
        self.right = None
        self.parent = None
        self.color = 'black'

class Solution:
    def InorderTreeWalk(self, x):
        if x != None:
            self.InorderTreeWalk(x.left)
            if x.key != 0:
                print('key:', x.key, 'parent:', x.parent.key, 'color:', x.color)
            self.InorderTreeWalk(x.right)

    def level_queue(self, root):
        if root == None:
            return
        myQueue = []
        node = root
        myQueue.append(node)
        while myQueue:
            node = myQueue.pop(0)
            if node.key != 0:
                print('key:', node.key, 'parent:', node.parent.key, 'color:', node.color)
            if node.left != None:
                myQueue.append(node.left)
            if node.right != None:
                myQueue.append(node.right)

    def LeftRotate(self, T, x):
        y = x.right
        x.right = y.left
        if y.left != T.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == T.nil:
            T.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def RightRotate(self, T, x):
        y = x.left
        x.left = y.right
        if y.right != T.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == T.nil:
            T.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def RBInsert(self, T, z):
        # init z
        z.left = T.nil
        z.right = T.nil
        z.parent = T.nil

        y = T.nil
        x = T.root
        while x != T.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == T.nil:
            T.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = T.nil
        z.right = T.nil
        z.color = 'red'
        self.RBInsertFixup(T,z)

    def RBInsertFixup(self, T, z):
        while z.parent.color == 'red':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.LeftRotate(T, z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.RightRotate(T,z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.RightRotate(T, z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.LeftRotate(T, z.parent.parent)
        T.root.color = 'black'

    def RBTransplant(self, T, u, v):
        if u.parent == T.nil:
            T.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def RBDelete(self, T, z):
        y = z
        y_original_color = y.color
        if z.left == T.nil:
            x = z.right
            self.RBTransplant(T, z, z.right)
        elif z.right == T.nil:
            x = z.left
            self.RBTransplant(T, z, z.left)
        else:
            y = self.TreeMinimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.RBTransplant(T, y, y.right)
                y.right = z.right
                y.right.parent = y
            self.RBTransplant(T, z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'black':
            self.RBDeleteFixup(T, x)

    def RBDeleteFixup(self, T, x):
        while x != T.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.LeftRotate(T, x.parent)
                    w = x.parent.right
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.RightRotate(T, w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self.LeftRotate(T, x.parent)
                    x = T.root
            else:
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.RightRotate(T, x.parent)
                    w = x.parent.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.LeftRotate(T, w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self.RightRotate(T, x.parent)
                    x = T.root
        x.color = 'black'

    def TreeMinimum(self, x):
        while x.left != T.nil:
            x = x.left
        return x


if __name__ == '__main__':
    # elems = range(10)           #生成十个数据作为树节点
    # tree = Tree()          #新建一个树对象
    # for elem in elems:
    #     print(elem)
    #     tree.add(elem)           #逐个添加树的节点

    # print('队列实现层次遍历:')
    # tree.level_queue(tree.root)

    # print('递归实现先序遍历:')
    # tree.front_digui(tree.root)
    # print('递归实现中序遍历:')
    # tree.middle_digui(tree.root)
    # print('递归实现后序遍历:')
    # tree.later_digui(tree.root)
    #
    # print('堆栈实现先序遍历:')
    # tree.front_stack(tree.root)
    # print('堆栈实现中序遍历:')
    # tree.middle_stack(tree.root)
    # print('堆栈实现后序遍历:')
    # tree.later_stack(tree.root)

    nodes = [16,10,24,18,27,2,26,29,17,1]
    T = RBTree()
    s = Solution()
    for node in nodes:
        s.RBInsert(T, RBTreeNode(node))

    s.InorderTreeWalk(T.root)
    print("层次遍历")
    s.level_queue(T.root)

    # s.RBDelete(T, T.root)
    # print('after delete')
    # s.InorderTreeWalk(T.root)