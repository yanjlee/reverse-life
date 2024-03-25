# -*- coding: utf-8 -*-
import time

# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        re = ListNode(0)
        r = re
        carry = 0
        while l1 or l2:
            x = l1.val if l1 else 0
            y = l2.val if l2 else 0
            s = carry + x + y
            carry = s // 10
            r.next = ListNode(s % 10)
            r = r.next
            if l1 != None:
                l1 = l1.next
            if l2 != None:
                l2 = l2.next
        if carry > 0:
            r.next = ListNode(1)
        return re.next


if __name__ == "__main__":
    time_start = time.time()
    nums = [2, 11, 7, 15]
    target = 9
    Solution = Solution()
    res_list = Solution.addTwoNumbers(nums, target)
    print(res_list)
    time_end = time.time()
    time_spent = time_end - time_start
    print("_________________________time_spent:%s" % time_spent)
