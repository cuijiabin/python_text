# coding=gbk
"""
排序算法默写
"""

# 1.归并排序
def merge_sort(array):
    if len(array) <=1:
        return array
    num = int(len(array)/2)
    left = merge_sort(array[:num])
    right = merge_sort(array[num:])
    return merge(left,right)

def merge(left,right):
    result = []
    i,j = 0,0
    while i<len(left) and j<len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result +=left[i:] # result.append(left[i:]) 注意点
    result +=right[j:]
    return result

def quick(array,left,right):
    if left >= right:
        return array
    key, lp, rp = array[left],left,right
    while lp < rp:
        while array[rp] >= key and lp <rp:
            rp -= 1
        while array[lp] <= key and lp <rp:
            lp += 1
        array[lp],array[rp] = array[rp],array[lp]

    array[left],array[lp] = array[lp],array[left]

    quick(array,left,lp-1)
    quick(array,rp+1,right)

    return array

# 需要额外的空间
def quick_sort(array):
    if len(array) <= 1:
        return array
    key = array[0]
    less = []
    more = []
    mid =[key]
    for i in range(1,len(array)):
        if key > array[i]:
            less.append(array[i])
        elif key < array[i]:
            more.append(array[i])
        else:
            mid.append(array[i])
    less = quick_sort(less)
    more = quick_sort(more)

    return less + mid + more

if __name__ =="__main__":
    # l = [1,3,7]
    # r = [1,2,4]
    # m = merge(l,r)
    l = [5,4,2,5,4,1,2,6,9]
    # s = merge_sort(l)
    s = quick(l,0,len(l)-1)
    # print(quick([5,4,2,5,4,1,2,6,9],0,8))
    print(s)
    n = quick_sort(l)
    print(s)