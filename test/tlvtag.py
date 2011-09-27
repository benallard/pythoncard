"""
Those are helper classes to build arrays containing TLVs


"""

def sanitycheck(array):
    mask = (1 << 8) - 1
    for i in range(len(array)):
        if array[i] > ((1 << (8)-1) - 1):
            array[i] =  -(~(array[i]-1) & mask)

class Tag(list):
    def __init__(self, cls=0, constr=False, number=0):
        if number >= 31:
            self.append((cls << 6) + (int(constr) << 5) + 0x1f)
            tagNumber = number
            chunks = []
            while tagNumber > 0:
                chunks.append(tagNumber & 0x7f)
                tagNumber = tagNumber >> 7
            bLen = 1
            for i in reversed(chunks):
                self.append(0x80)
                self[-1] += i
            #clear the high bit on the last part
            self[-1] &= 0x7f
        else:
            self.append((cls << 6) + (int(constr) << 5) + number)
        sanitycheck(self)

class TLV(list):
    def __init__(self, tag=Tag(), value=[]):
        self.extend(tag)
        if (len(value) > 127):
            length = len(value)
            chunks = []
            while length > 0:
                chunks.append(length % 0xff)
                length = length // 0xff
            self.append(0x80 | len(chunks))
            self.extend(chunks)
        else:
            self.append(len(value))
        self.extend(value)
        sanitycheck(self)
