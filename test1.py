from collections import abc
import collections
import collections.abc
import asyncio
from queue import Queue


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

# def gen_123():
#     yield 1
#     yield 2
#     yield 3
#
# g = gen_123()
# next(g)
# next(g)
# next(g)
#
#
# from functools import wraps
#
# asyncio.sleep()


class FrozenJSON:
        """一个只读接口， 使用属性表示法访问JSON类对象
        """
        def __init__(self, mapping):
            self.__data = dict(mapping)

        def __getattr__(self, name):
            if hasattr(self.__data, name):
                return getattr(self.__data, name)
            else:
                return FrozenJSON.build(self.__data[name])

        @classmethod
        def build(cls, obj):
            if isinstance(obj, abc.Mapping):
                return cls(obj)
            elif isinstance(obj, abc.MutableSequence):
                return [cls.build(item) for item in obj]
            else:
                return obj


dict1 = {'a': 1, 'b': 2, 'C': 3}
fj = FrozenJSON(dict1)
fj.a



