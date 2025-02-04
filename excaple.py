U = 1


def pr():
    u = 1
    print(u, U)

u = 2

class I(u):
    def __init__(self, u):
        self.u = u

    def prr(self):
        print(self.u)


I.prr(3)
print(u, U)