# coding=gbk
"""
排序算法 按名称来进行排序
插入排序 冒泡排序
希尔排序
归并排序 快速排序 堆排序
基数排序
"""
import math
# 第一类
"""
插入排序 InsertionSort 插入排序的工作原理是，对于每个未排序数据，在已排序序列中从后向前扫描，找到相应位置并插入。
步骤：
1.从第一个元素开始，该元素可以认为已经被排序
2.取出下一个元素，在已经排序的元素序列中从后向前扫描
3.如果被扫描的元素（已排序）大于新元素，将该元素后移一位
4.重复步骤3，直到找到已排序的元素小于或者等于新元素的位置
5.将新元素插入到该位置后
6.重复步骤2~5
"""
def insert_sort(array):
    n = len(array)
    for i in range(1,n):
        if array[i] < array[i-1]:
            temp = array[i]
            index = i           #待插入的下标
            for j in range(i-1,-1,-1):  #从i-1 循环到 0 (包括0)
                if array[j] > temp :
                    array[j+1] = array[j]
                    index = j   #记录待插入下标
                else :
                    break
            array[index] = temp
    return array

"""
冒泡排序 BubbleSort 冒泡排序的原理非常简单，它重复地走访过要排序的数列，一次比较两个元素，如果他们的顺序错误就把他们交换过来。
步骤：
比较相邻的元素。如果第一个比第二个大，就交换他们两个。
对第0个到第n-1个数据做同样的工作。这时，最大的数就“浮”到了数组最后的位置上。
针对所有的元素重复以上的步骤，除了最后一个。
持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。
"""
def bubble_sort(arry):
    n = len(arry)                   #获得数组的长度
    for i in range(n):
        for j in range(1,n-i):
            if  arry[j-1] > arry[j] :       #如果前者比后者大
                arry[j-1],arry[j] = arry[j],arry[j-1]      #则交换两者
    return arry

"""
选择排序 SelectionSort 选择排序无疑是最简单直观的排序。它的工作原理如下。
步骤：
在未排序序列中找到最小（大）元素，存放到排序序列的起始位置。
再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。
以此类推，直到所有元素均排序完毕。
"""
def select_sort(array):
    n = len(array)
    for i in range(0,n):
        min = i                             #最小元素下标标记
        for j in range(i+1,n):
            if array[j] < array[min] :
                min = j                     #找到最小值的下标
        array[min],array[i] = array[i],array[min]   #交换两者
    return array

"""
希尔排序 ShellSort
希尔排序，也称递减增量排序算法，实质是分组插入排序。由 Donald Shell 于1959年提出。希尔排序是非稳定排序算法。

希尔排序的基本思想是：将数组列在一个表中并对列分别进行插入排序，重复这过程，不过每次用更长的列（步长更长了，列数更少了）来进行。
最后整个表就只有一列了。将数组转换至表是为了更好地理解这算法，算法本身还是使用数组进行排序。

例如，假设有这样一组数[ 13 14 94 33 82 25 59 94 65 23 45 27 73 25 39 10 ]，如果我们以步长为5开始进行排序，
我们可以通过将这列表放在有5列的表中来更好地描述算法，这样他们就应该看起来是这样：

13 14 94 33 82
25 59 94 65 23
45 27 73 25 39
10
然后我们对每列进行排序：

10 14 73 25 23
13 27 94 33 39
25 59 94 65 82
45
将上述四行数字，依序接在一起时我们得到：[ 10 14 73 25 23 13 27 94 33 39 25 59 94 65 82 45 ]。
这时10已经移至正确位置了，然后再以3为步长进行排序：

10 14 73
25 23 13
27 94 33
39 25 59
94 65 82
45
排序之后变为：

10 14 13
25 23 33
27 25 59
39 65 73
45 94 82
94
最后以1步长进行排序（此时就是简单的插入排序了）。
"""
def shell_sort(array):
    n = len(array)
    gap = round(n/2)       #初始步长 , 用round四舍五入取整
    while gap > 0 :
        for i in range(gap,n):        #每一列进行插入排序 , 从gap 到 n-1
            temp = array[i]
            j = i
            while ( j >= gap and array[j-gap] > temp ):    #插入排序
                array[j] = array[j-gap]
                j = j - gap
            array[j] = temp
        gap = round(gap/2)                     #重新设置步长
    return array

"""
归并排序 MergeSort

归并排序是采用分治法的一个非常典型的应用。归并排序的思想就是先递归分解数组，再合并数组。
先考虑合并两个有序数组，基本思路是比较两个数组的最前面的数，谁小就先取谁，取了后相应的指针就往后移一位。
然后再比较，直至一个数组为空，最后把另一个数组的剩余部分复制过来即可。

再考虑递归分解，基本思路是将数组分解成left和right，如果这两个数组内部数据是有序的，那么就可以用上面合并数组的方法将这两个数组合并排序。
如何让这两个数组内部是有序的？可以再二分，直至分解出的小组只含有一个元素时为止，此时认为该小组内部已有序。然后合并排序相邻二个小组即可。
"""
def merge_sort(ary):
    if len(ary) <= 1 :
        return ary
    num = int(len(ary)/2)       #二分分解
    left = merge_sort(ary[:num])
    right = merge_sort(ary[num:])
    return merge(left,right)    #合并数组

def merge(left,right):
    '''合并操作，
    将两个有序数组left[]和right[]合并成一个大的有序数组
    '''
    l,r = 0,0           #left与right数组的下标指针
    result = []
    while l<len(left) and r<len(right) :
        if left[l] < right[r]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result

"""
快速排序 QuickSort
介绍：
快速排序通常明显比同为Ο(n log n)的其他算法更快，因此常被采用，而且快排采用了分治法的思想，所以在很多笔试面试中能经常看到快排的影子。可见掌握快排的重要性。

步骤：

从数列中挑出一个元素作为基准数。
分区过程，将比基准数大的放到右边，小于或等于它的数都放到左边。
再对左右区间递归执行第二步，直至各区间只有一个数。

"""
def quick_sort(array):
    return qsort(array,0,len(array)-1)

def qsort(array,left,right):
    #快排函数，array为待排序数组，left为待排序的左边界，right为右边界
    if left >= right :
        return array
    key = array[left]     #取最左边的为基准数
    lp = left           #左指针
    rp = right          #右指针
    while lp < rp :
        while array[rp] >= key and lp < rp :
            rp -= 1
        while array[lp] <= key and lp < rp :
            lp += 1
        array[lp],array[rp] = array[rp],array[lp]

    array[left],array[lp] = array[lp],array[left]
    qsort(array,left,lp-1)
    qsort(array,rp+1,right)
    return array

"""
堆排序 HeapSort
介绍：

堆排序在 top K 问题中使用比较频繁。堆排序是采用二叉堆的数据结构来实现的，虽然实质上还是一维数组。二叉堆是一个近似完全二叉树 。

二叉堆具有以下性质：

父节点的键值总是大于或等于（小于或等于）任何一个子节点的键值。
每个节点的左右子树都是一个二叉堆（都是最大堆或最小堆）。
步骤：

构造最大堆（Build_Max_Heap）：若数组下标范围为0~n，考虑到单独一个元素是大根堆，则从下标n/2开始的元素均为大根堆。于是只要从n/2-1开始，向前依次构造大根堆，这样就能保证，构造到某个节点时，它的左右子树都已经是大根堆。

堆排序（HeapSort）：由于堆是用数组模拟的。得到一个大根堆后，数组内部并不是有序的。因此需要将堆化数组有序化。思想是移除根节点，并做最大堆调整的递归运算。第一次将heap[0]与heap[n-1]交换，再对heap[0...n-2]做最大堆调整。第二次将heap[0]与heap[n-2]交换，再对heap[0...n-3]做最大堆调整。重复该操作直至heap[0]和heap[1]交换。由于每次都是将最大的数并入到后面的有序区间，故操作完后整个数组就是有序的了。

最大堆调整（Max_Heapify）：该方法是提供给上述两个过程调用的。目的是将堆的末端子节点作调整，使得子节点永远小于父节点 。
"""
def heap_sort(ary) :
    n = len(ary)
    first = int(n/2-1)       #最后一个非叶子节点
    for start in range(first,-1,-1) :     #构造大根堆
        max_heapify(ary,start,n-1)
    for end in range(n-1,0,-1):           #堆排，将大根堆转换成有序数组
        ary[end],ary[0] = ary[0],ary[end]
        max_heapify(ary,0,end-1)
    return ary


#最大堆调整：将堆的末端子节点作调整，使得子节点永远小于父节点
#start为当前需要调整最大堆的位置，end为调整边界
def max_heapify(ary,start,end):
    root = start
    while True :
        child = root*2 +1               #调整节点的子节点
        if child > end : break
        if child+1 <= end and ary[child] < ary[child+1] :
            child = child+1             #取较大的子节点
        if ary[root] < ary[child] :     #较大的子节点成为父节点
            ary[root],ary[child] = ary[child],ary[root]     #交换
            root = child
        else :
            break

"""
基数排序

"""
def radix_sort(lists, radix=10):
    k = int(math.ceil(math.log(max(lists), radix)))
    bucket = [[] for i in range(radix)]
    for i in range(1, k+1):
        for j in lists:
            bucket[j/(radix**(i-1)) % (radix**i)].append(j)
        del lists[:]
        for z in bucket:
            lists += z
            del z[:]
    return lists


# 堆排序的思想 -- 以大根堆为例:
# 1) 构建堆
# 2) 把堆根取下来放到有序区去 -- 堆跟是当前堆上最大的数字
# 3) 此时堆没有根了，重新调整堆，然后重复1) - 3)直到堆成为一个空堆
#
# 堆排序是选择排序的一种： 也是每次从未排序的区域选择一个值放入已排序的区域
# 它对直接选择排序的改进是： 对于以前已经比较过的结果可以保留下来：不用再重复比较：这也是堆的特性

def heap_sort(arr):
    build_heap(arr)
    print(arr)
    arrlen = len(arr)
    for i in reversed(range(1, arrlen)):
        # 把堆跟(最大的值)放到最后面去
        swap(arr, 0, i)
        # 重新调整堆
        heapify(arr, 0, i - 1)


def swap(arr, index1, index2):
    tmp = arr[index1]
    arr[index1] = arr[index2]
    arr[index2] = tmp


def build_heap(arr):
    """
    以arr[0]到arr[(arrlen / 2)]为根的这些子树是需要调整的子树
    其他的都是叶子节点
    """
    arrlen = len(arr)
    harf = int(math.floor(arrlen / 2))
    for i in reversed(range(0, harf)):
        heapify(arr, i, arrlen - 1)


def heapify(arr, low, high):
    left = low * 2 + 1
    right = left + 1
    current = low

    # 暂存这个“假根”的值
    tmp = arr[low]

    # 如果当前节点还有子树
    while left <= high:
        if right <= high:
            if arr[left] < arr[right]:
                next = right
            else:
                next = left
        else:
            next = left

        # 确实有个孩子的值比他大
        if tmp < arr[next]:
            # 把这个大的值上移到父亲节点
            arr[current] = arr[next]
            # 更新current
            current = next
            left = current * 2 + 1
            right = left + 1
        else:
            # 这个堆已经完成
            break

    # 把假根把到这个正确的位置
    arr[current] = tmp

if __name__ =="__main__":
    arr = [1,2,5,6,7,4,9,8]
    # arr = insert_sort(arr)
    # arr = bubble_sort(arr)
    # arr = select_sort(arr)
    # arr = shell_sort(arr)
    # arr = merge_sort(arr)
    # arr = heap_sort(arr)
    heap_sort(arr)
    print(arr)