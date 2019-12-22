# # ii = [1,2,3,4,5]
# # print(type(ii))
# # # # r = []
# # # # r = [i for i in ii if i % 2 == 0]
# # # # r = map(2 % i == 0 , ii)
# # # r = filter(lambda a: a % 2 == 0, ii)

# # # print(type(r))
# # # for rr in r:
# # #     print(rr)


# # d = ['{"head": "글10 의 제목입니다.", "content": "글10 의 내용입니다.", "author": "10"}', '{"head": "글11 의 제목입니다.", "content": "글11 의 내용입니다.", "author": "11"}', '{"head": "글12 의 제목입니다.", "content": "글12 의 내용입니다.", "author": "12"}', '{"head": "글13 의 제목입니다.", "content": "글13 의 내용입니다.", "author": "13"}', '{"head": "글14 의 제목입니다.", "content": "글14 의 내용입니다.", "author": "14"}', '{"head": "글15 의 제목입니다.", "content": "글15 의 내용입니다.", "author": "15"}', '{"head": "글16 의 제목입니다.", "content": "글16 의 내용입니다.", "author": "16"}', '{"head": "글17 의 제목입니다.", "content": "글17 의 내용입니다.", "author": "17"}', '{"head": "글18 의 제목입니다.", "content": "글18 의 내용입니다.", "author": "18"}', '{"head": "글19 의 제목입니다.", "content": "글19 의 내용입니다.", "author": "19"}']

# # import re

# # pattern = re.compile("(^{)")
# # s = pattern.findall(d[0])
# # print(s)

# # # print(type(d.items()), d.items())
# # # for k, v in d.items():
# # #     print(k, v)
# # # else:
# # #     print("/////")

# d = { "dddd" : '{ "dd" : "ssss"}',
#         "ddd" : [ {"aaaa" : "A"} , {"aaa" : "x"}] }

# print(d[list(d.keys())[0]])


# s = [ 1, 2, 3,4 ]

# for i in s:
#     print(i)

# a=["<class 'list'>", "<class 'str'>"]
# _haslist = True if "<class 'list'>" in a else False
    
# print("====================\n ", _haslist)

# # print(list(d.keys())[0])

v = [{'head': '글10 의 제목입니다.', 'content': '글10 의 내용입니다.', 'author': '10'}, {'head': '글11 의 제목입니다.', 'content': '글11 의 내용입니다.', 'author': '11'}, {'head': '글12 의 제목입니다.', 'content': '글12 의 내용입니다.', 'author': '12'}, {'head': '글13 의 제목입니다.', 'content': '글13 의 내용입니다.', 'author': '13'}, {'head': '글14 의 제목입니다.', 'content': '글14 의 내용입니다.', 'author': '14'}, {'head': '글15 의 제목입니다.', 'content': '글15 의 내용입니다.', 'author': '15'}, {'head': '글16 의 제목입니다.', 'content': '글16 의 내용입니다.', 'author': '16'}, {'head': '글17 의 제목입니다.', 'content': '글17 의 내용입니다.', 'author': '17'}, {'head': '글18 의 제목입니다.', 'content': '글18 의 내용입니다.', 'author': '18'}, {'head': '글19 의 제목입니다.', 'content': '글19 의 내용입니다.', 'author': '19'}]

import re

class svc(object):
    # print("<<<")
    p = "123"

    def fun(sss="default"):
        print(",,,,,, ", sss)
    
    def get_call(self):
        return self.call
    def set_call(self, v=1):
        self.call = v

    v = fun()

    def __init__(self):
        self.call = 100
        self.g = self.get_call()
        self.s = self.set_call()

    def __call__(self):
        print("this is call")


s = svc()
# s()
print(">>>>>", s.__getattribute__('v'))
print(">>>>>", s.__getattribute__('s'))
print(">>>>>", s.__getattribute__('g'))

print(dir(s))

def l(n=2):
    return n + 1

w = { "ss" : l() }

print(w["ss"])


# a = l()
# print(a)

# def bind(instance, method):
#     def binding_scope_fn(*args, **kwargs): 
#         return method(instance, *args, **kwargs)
#     return binding_scope_fn


def like(*args, **kwargs):
    def nested_function(*args, **kwargs):
        return " %s 입니다. " % args
    return nested_function

# a = like("s")
# b = like()
a = like()
print("<<<<", type(a), a, dir(a))
# print(">>>", a)
# print(object.__dir__)
# print(dir(object))


