
class CommonUtils:

    # Return a generator
    @classmethod
    def list_split_by_step(cls, li, step):
        i = 0
        if len(li) // step < 1:
            yield li
        else:
            for i in range(0, len(li) // step):
                yield li[step*i: step*(i+1)]
            yield li[step*(i+1): len(li)]

    @classmethod
    def dict_split_by_step(cls, dict, step):
        pass


if __name__ == "__main__":
    li = [[1, 1, 2, ], [12, 2, 1, 1], [1], ['a', 'b', 'D'],[1,2,3,'a']]
    a = CommonUtils.list_split_by_step(li,6)
    print(next(a))
    print(next(a))
    print(next(a))
    print(next(a))
