# coding=utf8
import read
import write
import add

'''
None  "" False [] {} () 0 都是布尔类型假
'''


class DataAPI(object):

    def __init__(self, filename, _type, key=None):
        self.filename = filename
        self.type = _type
        self.key = key
        self.read = read.Read()
        self.write = write.Write()
        self.add = add.Add()

    def run(self):

        if self.type not in list('rwa'):
            return False

        elif self.type == 'r':
            return self.read.read(self.filename, self.key)
        elif self.type == 'w':
            return self.write.write(self.filename, self.key)
        else:
            return self.add.add(self.filename, self.key)






