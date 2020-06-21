import collections
import collections.abc

# class A:
#     class B:
#         def testb(self):
#             print("testb is running")
#
# class AAA(collections.MutableSequence):
#     a = 1
#
# aaa = AAA()
# print(aaa.a)

def gen_123():
    yield 1
    yield 2
    yield 3

g = gen_123()
next(g)
next(g)
next(g)
next(g)