class A:
    def func1(self):
        print("func1")

    @property
    def val1(self):
        return "1"
    a = 1


class B(A):
    b = 1


b = B()
b.c = 1
print(B.__dict__)
