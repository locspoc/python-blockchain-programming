def myFunc(int_in):
    return int_in/5

print('Hello!')

# print(myFunc(14))

class myClass:
    oneval = 17
    def div(self, int_in):
        try:
            return int_in/self.oneval
        except TypeError:
            print("Must pass integer to div")
            return 0
        except:
            print("Unknown error in div")
            return 0
    def __init__(self, inval):
        self.oneval = inval

class newClass (myClass):
    name = 'Levi'
    def __repr__(self):
        name = "Jeff"
        return (self.name + ": oneval is equal to " + 
                str(self.oneval))

C = myClass(4)
B = myClass(10)
# print(C.oneval)
# print(C.div(34))
# print(B.div(34))

N = newClass(12)
# print(N.name)
# print(N.div(36))
# print(N)
print(N.div('rutebega'))

if __name__ == '__main__':
    print(myFunc(21))
else:
    print('Primer imported, not invoked')
