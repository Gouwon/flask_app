import json, re
from sqlalchemy import sql



# class QuertyConstructor():
#     pc = {"Post" : ['id', 'head', 'content', 'author', 'registdt', 'updatedt']}

#     def __init__(self, table='Post', **kwargs):
#         self.table = table
#         self.data = kwargs
#         self.sql_query = "first"

#     @property
#     def query(self):
#         print("inside the getter")
#         self.sql_query="second"
#         return self.sql_query
    
#     def __query__(self):
#         pass
        


# data = {'order': 'desc', 'criteria': 'head', 'search': '', 'limit' : '10', 'pageno' : '0'}
# q = QuertyConstructor(table='Post', **data)
# print(q.table, q.sql_query, q.query)
# d = {"t" : "s"}
# print(q.query)
# q = QuertyConstructor(data)

class B(ModelHelper):
    def plus(self, v):
        return v + 2
column = B()
print(dir(column))
filt = getattr(column, "plus")(3)
print(filt)


# print(dir(object))
# p = getattr(object, '__')