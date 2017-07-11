# coding=gbk
"""
�����㷨 ����������������
�������� ð������
ϣ������
�鲢���� �������� ������
��������
"""
import math
# ��һ��
"""
�������� InsertionSort ��������Ĺ���ԭ���ǣ�����ÿ��δ�������ݣ��������������дӺ���ǰɨ�裬�ҵ���Ӧλ�ò����롣
���裺
1.�ӵ�һ��Ԫ�ؿ�ʼ����Ԫ�ؿ�����Ϊ�Ѿ�������
2.ȡ����һ��Ԫ�أ����Ѿ������Ԫ�������дӺ���ǰɨ��
3.�����ɨ���Ԫ�أ������򣩴�����Ԫ�أ�����Ԫ�غ���һλ
4.�ظ�����3��ֱ���ҵ��������Ԫ��С�ڻ��ߵ�����Ԫ�ص�λ��
5.����Ԫ�ز��뵽��λ�ú�
6.�ظ�����2~5
"""
def insert_sort(array):
    n = len(array)
    for i in range(1,n):
        if array[i] < array[i-1]:
            temp = array[i]
            index = i           #��������±�
            for j in range(i-1,-1,-1):  #��i-1 ѭ���� 0 (����0)
                if array[j] > temp :
                    array[j+1] = array[j]
                    index = j   #��¼�������±�
                else :
                    break
            array[index] = temp
    return array

"""
ð������ BubbleSort ð�������ԭ��ǳ��򵥣����ظ����߷ù�Ҫ��������У�һ�αȽ�����Ԫ�أ�������ǵ�˳�����Ͱ����ǽ���������
���裺
�Ƚ����ڵ�Ԫ�ء������һ���ȵڶ����󣬾ͽ�������������
�Ե�0������n-1��������ͬ���Ĺ�������ʱ���������͡�����������������λ���ϡ�
������е�Ԫ���ظ����ϵĲ��裬�������һ����
����ÿ�ζ�Խ��Խ�ٵ�Ԫ���ظ�����Ĳ��裬ֱ��û���κ�һ��������Ҫ�Ƚϡ�
"""
def bubble_sort(arry):
    n = len(arry)                   #�������ĳ���
    for i in range(n):
        for j in range(1,n-i):
            if  arry[j-1] > arry[j] :       #���ǰ�߱Ⱥ��ߴ�
                arry[j-1],arry[j] = arry[j],arry[j-1]      #�򽻻�����
    return arry

"""
ѡ������ SelectionSort ѡ���������������ֱ�۵��������Ĺ���ԭ�����¡�
���裺
��δ�����������ҵ���С����Ԫ�أ���ŵ��������е���ʼλ�á�
�ٴ�ʣ��δ����Ԫ���м���Ѱ����С����Ԫ�أ�Ȼ��ŵ����������е�ĩβ��
�Դ����ƣ�ֱ������Ԫ�ؾ�������ϡ�
"""
def select_sort(array):
    n = len(array)
    for i in range(0,n):
        min = i                             #��СԪ���±���
        for j in range(i+1,n):
            if array[j] < array[min] :
                min = j                     #�ҵ���Сֵ���±�
        array[min],array[i] = array[i],array[min]   #��������
    return array

"""
ϣ������ ShellSort
ϣ������Ҳ�Ƶݼ����������㷨��ʵ���Ƿ������������ Donald Shell ��1959�������ϣ�������Ƿ��ȶ������㷨��

ϣ������Ļ���˼���ǣ�����������һ�����в����зֱ���в��������ظ�����̣�����ÿ���ø������У����������ˣ����������ˣ������С�
����������ֻ��һ���ˡ�������ת��������Ϊ�˸��õ�������㷨���㷨������ʹ�������������

���磬����������һ����[ 13 14 94 33 82 25 59 94 65 23 45 27 73 25 39 10 ]����������Բ���Ϊ5��ʼ��������
���ǿ���ͨ�������б������5�еı��������õ������㷨���������Ǿ�Ӧ�ÿ�������������

13 14 94 33 82
25 59 94 65 23
45 27 73 25 39
10
Ȼ�����Ƕ�ÿ�н�������

10 14 73 25 23
13 27 94 33 39
25 59 94 65 82
45
�������������֣��������һ��ʱ���ǵõ���[ 10 14 73 25 23 13 27 94 33 39 25 59 94 65 82 45 ]��
��ʱ10�Ѿ�������ȷλ���ˣ�Ȼ������3Ϊ������������

10 14 73
25 23 13
27 94 33
39 25 59
94 65 82
45
����֮���Ϊ��

10 14 13
25 23 33
27 25 59
39 65 73
45 94 82
94
�����1�����������򣨴�ʱ���Ǽ򵥵Ĳ��������ˣ���
"""
def shell_sort(array):
    n = len(array)
    gap = round(n/2)       #��ʼ���� , ��round��������ȡ��
    while gap > 0 :
        for i in range(gap,n):        #ÿһ�н��в������� , ��gap �� n-1
            temp = array[i]
            j = i
            while ( j >= gap and array[j-gap] > temp ):    #��������
                array[j] = array[j-gap]
                j = j - gap
            array[j] = temp
        gap = round(gap/2)                     #�������ò���
    return array

"""
�鲢���� MergeSort

�鲢�����ǲ��÷��η���һ���ǳ����͵�Ӧ�á��鲢�����˼������ȵݹ�ֽ����飬�ٺϲ����顣
�ȿ��Ǻϲ������������飬����˼·�ǱȽ������������ǰ�������˭С����ȡ˭��ȡ�˺���Ӧ��ָ���������һλ��
Ȼ���ٱȽϣ�ֱ��һ������Ϊ�գ�������һ�������ʣ�ಿ�ָ��ƹ������ɡ�

�ٿ��ǵݹ�ֽ⣬����˼·�ǽ�����ֽ��left��right����������������ڲ�����������ģ���ô�Ϳ���������ϲ�����ķ���������������ϲ�����
����������������ڲ�������ģ������ٶ��֣�ֱ���ֽ����С��ֻ����һ��Ԫ��ʱΪֹ����ʱ��Ϊ��С���ڲ�������Ȼ��ϲ��������ڶ���С�鼴�ɡ�
"""
def merge_sort(ary):
    if len(ary) <= 1 :
        return ary
    num = int(len(ary)/2)       #���ַֽ�
    left = merge_sort(ary[:num])
    right = merge_sort(ary[num:])
    return merge(left,right)    #�ϲ�����

def merge(left,right):
    '''�ϲ�������
    ��������������left[]��right[]�ϲ���һ�������������
    '''
    l,r = 0,0           #left��right������±�ָ��
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
�������� QuickSort
���ܣ�
��������ͨ�����Ա�ͬΪ��(n log n)�������㷨���죬��˳������ã����ҿ��Ų����˷��η���˼�룬�����ںܶ�����������ܾ����������ŵ�Ӱ�ӡ��ɼ����տ��ŵ���Ҫ�ԡ�

���裺

������������һ��Ԫ����Ϊ��׼����
�������̣����Ȼ�׼����ķŵ��ұߣ�С�ڻ�������������ŵ���ߡ�
�ٶ���������ݹ�ִ�еڶ�����ֱ��������ֻ��һ������

"""
def quick_sort(array):
    return qsort(array,0,len(array)-1)

def qsort(array,left,right):
    #���ź�����arrayΪ���������飬leftΪ���������߽磬rightΪ�ұ߽�
    if left >= right :
        return array
    key = array[left]     #ȡ����ߵ�Ϊ��׼��
    lp = left           #��ָ��
    rp = right          #��ָ��
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
������ HeapSort
���ܣ�

�������� top K ������ʹ�ñȽ�Ƶ�����������ǲ��ö���ѵ����ݽṹ��ʵ�ֵģ���Ȼʵ���ϻ���һά���顣�������һ��������ȫ������ ��

����Ѿ����������ʣ�

���ڵ�ļ�ֵ���Ǵ��ڻ���ڣ�С�ڻ���ڣ��κ�һ���ӽڵ�ļ�ֵ��
ÿ���ڵ��������������һ������ѣ��������ѻ���С�ѣ���
���裺

�������ѣ�Build_Max_Heap�����������±귶ΧΪ0~n�����ǵ�����һ��Ԫ���Ǵ���ѣ�����±�n/2��ʼ��Ԫ�ؾ�Ϊ����ѡ�����ֻҪ��n/2-1��ʼ����ǰ���ι������ѣ��������ܱ�֤�����쵽ĳ���ڵ�ʱ�����������������Ѿ��Ǵ���ѡ�

������HeapSort�������ڶ���������ģ��ġ��õ�һ������Ѻ������ڲ�����������ġ������Ҫ���ѻ��������򻯡�˼�����Ƴ����ڵ㣬�������ѵ����ĵݹ����㡣��һ�ν�heap[0]��heap[n-1]�������ٶ�heap[0...n-2]�����ѵ������ڶ��ν�heap[0]��heap[n-2]�������ٶ�heap[0...n-3]�����ѵ������ظ��ò���ֱ��heap[0]��heap[1]����������ÿ�ζ��ǽ����������뵽������������䣬�ʲ�����������������������ˡ�

���ѵ�����Max_Heapify�����÷������ṩ�������������̵��õġ�Ŀ���ǽ��ѵ�ĩ���ӽڵ���������ʹ���ӽڵ���ԶС�ڸ��ڵ� ��
"""
def heap_sort(ary) :
    n = len(ary)
    first = int(n/2-1)       #���һ����Ҷ�ӽڵ�
    for start in range(first,-1,-1) :     #��������
        max_heapify(ary,start,n-1)
    for end in range(n-1,0,-1):           #���ţ��������ת������������
        ary[end],ary[0] = ary[0],ary[end]
        max_heapify(ary,0,end-1)
    return ary


#���ѵ��������ѵ�ĩ���ӽڵ���������ʹ���ӽڵ���ԶС�ڸ��ڵ�
#startΪ��ǰ��Ҫ�������ѵ�λ�ã�endΪ�����߽�
def max_heapify(ary,start,end):
    root = start
    while True :
        child = root*2 +1               #�����ڵ���ӽڵ�
        if child > end : break
        if child+1 <= end and ary[child] < ary[child+1] :
            child = child+1             #ȡ�ϴ���ӽڵ�
        if ary[root] < ary[child] :     #�ϴ���ӽڵ��Ϊ���ڵ�
            ary[root],ary[child] = ary[child],ary[root]     #����
            root = child
        else :
            break

"""
��������

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


# �������˼�� -- �Դ����Ϊ��:
# 1) ������
# 2) �ѶѸ�ȡ�����ŵ�������ȥ -- �Ѹ��ǵ�ǰ������������
# 3) ��ʱ��û�и��ˣ����µ����ѣ�Ȼ���ظ�1) - 3)ֱ���ѳ�Ϊһ���ն�
#
# ��������ѡ�������һ�֣� Ҳ��ÿ�δ�δ���������ѡ��һ��ֵ���������������
# ����ֱ��ѡ������ĸĽ��ǣ� ������ǰ�Ѿ��ȽϹ��Ľ�����Ա����������������ظ��Ƚϣ���Ҳ�Ƕѵ�����

def heap_sort(arr):
    build_heap(arr)
    print(arr)
    arrlen = len(arr)
    for i in reversed(range(1, arrlen)):
        # �ѶѸ�(����ֵ)�ŵ������ȥ
        swap(arr, 0, i)
        # ���µ�����
        heapify(arr, 0, i - 1)


def swap(arr, index1, index2):
    tmp = arr[index1]
    arr[index1] = arr[index2]
    arr[index2] = tmp


def build_heap(arr):
    """
    ��arr[0]��arr[(arrlen / 2)]Ϊ������Щ��������Ҫ����������
    �����Ķ���Ҷ�ӽڵ�
    """
    arrlen = len(arr)
    harf = int(math.floor(arrlen / 2))
    for i in reversed(range(0, harf)):
        heapify(arr, i, arrlen - 1)


def heapify(arr, low, high):
    left = low * 2 + 1
    right = left + 1
    current = low

    # �ݴ�������ٸ�����ֵ
    tmp = arr[low]

    # �����ǰ�ڵ㻹������
    while left <= high:
        if right <= high:
            if arr[left] < arr[right]:
                next = right
            else:
                next = left
        else:
            next = left

        # ȷʵ�и����ӵ�ֵ������
        if tmp < arr[next]:
            # ��������ֵ���Ƶ����׽ڵ�
            arr[current] = arr[next]
            # ����current
            current = next
            left = current * 2 + 1
            right = left + 1
        else:
            # ������Ѿ����
            break

    # �Ѽٸ��ѵ������ȷ��λ��
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