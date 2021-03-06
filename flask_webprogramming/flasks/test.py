# # # sql
# # # ['Alias', 'ClauseElement', 'ClauseVisitor', 'ColumnCollection', 'ColumnElement', 'CompoundSelect', 'Delete', 'False_', 'FromClause', 'Insert', 'Join', 'Select', 'Selectable', 'TableClause', 'TableSample', 'True_', 'Update', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__go', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'alias', 'all_', 'and_', 'annotation', 'any_', 'asc', 'base', 'between', 'bindparam', 'case', 'cast', 'collate', 'column', 'compiler', 'crud', 'ddl', 'default_comparator', 'delete', 'desc', 'distinct', 'dml', 'elements', 'except_', 'except_all', 'exists', 'expression', 'extract', 'false', 'func', 'funcfilter', 'functions', 'insert', 'intersect', 'intersect_all', 'join', 'label', 'lateral', 'literal', 'literal_column', 'modifier', 'naming', 'not_', 'null', 'nullsfirst', 'nullslast', 'operators', 'or_', 'outerjoin', 'outparam', 'over', 'quoted_name', 'schema', 'select', 'selectable', 'sqltypes', 'subquery', 'table', 'tablesample', 'text', 'true', 'tuple_', 'type_api', 'type_coerce', 'union', 'union_all', 'update', 'util', 'visitors', 'within_group']

# # # sql.expression
# # # ['Alias', 'BinaryExpression', 'BindParameter', 'BooleanClauseList', 'CTE', 'Case', 'Cast', 'ClauseElement', 'ClauseList', 'CollectionAggregate', 'ColumnClause', 'ColumnCollection', 'ColumnElement', 'CompoundSelect', 'Delete', 'Executable', 'Exists', 'Extract', 'False_', 'FromClause', 'FromGrouping', 'Function', 'FunctionElement', 'FunctionFilter', 'Generative', 'GenerativeSelect', 'Grouping', 'HasCTE', 'HasPrefixes', 'HasSuffixes', 'Insert', 'Join', 'Label', 'Lateral', 'Null', 'Over', 'PARSE_AUTOCOMMIT', 'ReleaseSavepointClause', 'RollbackToSavepointClause', 'SavepointClause', 'ScalarSelect', 'Select', 'SelectBase', 'Selectable', 'TableClause', 'TableSample', 'TextAsFrom', 'TextClause', 'True_', 'Tuple', 'TypeClause', 'TypeCoerce', 'UnaryExpression', 'Update', 'UpdateBase', 'ValuesBase', 'Visitable', 'WithinGroup', '_BinaryExpression', '_BindParamClause', '_Case', '_Cast', '_Executable', '_Exists', '_Extract', '_False', '_FromGrouping', '_Generative', '_Grouping', '_Label', '_Null', '_Over', '_ScalarSelect', '_SelectBase', '_TextClause', '_True', '_Tuple', '_TypeClause', '_UnaryExpression', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '_clause_element_as_expr', '_clone', '_cloned_difference', '_cloned_intersection', '_column_as_key', '_corresponding_column_or_error', '_expression_literal_as_text', '_from_objects', '_interpret_as_from', '_is_column', '_labeled', '_literal_as_binds', '_literal_as_label_reference', '_literal_as_text', '_only_column_elements', '_select_iterables', '_string_or_unprintable', '_truncated_label', 'alias', 'all_', 'and_', 'any_', 'asc', 'between', 'bindparam', 'case', 'cast', 'collate', 'column', 'delete', 'desc', 'distinct', 'except_', 'except_all', 'exists', 'extract', 'false', 'func', 'funcfilter', 'insert', 'intersect', 'intersect_all', 'join', 'label', 'lateral', 'literal', 'literal_column', 'modifier', 'not_', 'null', 'nullsfirst', 'nullslast', 'or_', 'outerjoin', 'outparam', 'over', 'public_factory', 'quoted_name', 'select', 'subquery', 'table', 'tablesample', 'text', 'true', 'tuple_', 'type_coerce', 'union', 'union_all', 'update', 'within_group']

# # # sql.operators.ColumnOperators
# # # ['__add__', '__and__', '__class__', '__contains__', '__delattr__', '__dir__', '__div__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__invert__', '__le__', '__lshift__', '__lt__', '__mod__', '__module__', '__mul__', '__ne__', '__neg__', '__new__', '__or__', '__radd__', '__rdiv__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__rshift__', '__rsub__', '__rtruediv__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__sub__', '__subclasshook__', '__truediv__', 'all_', 'any_', 'asc', 'between', 'bool_op', 'collate', 'concat', 'contains', 'desc', 'distinct', 'endswith', 'ilike', 'in_', 'is_', 'is_distinct_from', 'isnot', 'isnot_distinct_from', 'like', 'match', 'notilike', 'notin_', 'notlike', 'nullsfirst', 'nullslast', 'op', 'operate', 'reverse_operate', 'startswith', 'timetuple']

# # # sql.SELECT
# # # ['__and__', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__invert__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__or__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__visit_name__', '__weakref__', '_annotate', '_annotations', '_bind', '_clone', '_cloned_set', '_cols_populated', '_columns_plus_names', '_compiler', '_compiler_dispatch', '_constructor', '_copy_internals', '_correlate', '_correlate_except', '_deannotate', '_distinct', '_execute_on_connection', '_execution_options', '_for_update_arg', '_from_cloned', '_from_objects', '_froms', '_generate', '_get_display_froms', '_group_by_clause', '_hide_froms', '_hints', '_init_collections', '_is_clone_of', '_is_from_container', '_is_join', '_is_lateral', '_is_lexical_equivalent', '_is_select', '_label_resolve_dict', '_limit', '_limit_clause', '_memoized_property', '_needs_parens_for_grouping', '_negate', '_offset', '_offset_clause', '_order_by_clause', '_order_by_label_element', '_params', '_populate_column_collection', '_prefixes', '_refresh_for_new_column', '_reset_exported', '_scalar_type', '_select_iterable', '_set_bind', '_setup_prefixes', '_setup_suffixes', '_simple_int_limit', '_simple_int_offset', '_statement_hints', '_suffixes', '_textual', '_translate_schema', '_with_annotations', 'alias', 'append_column', 'append_correlation', 'append_from', 'append_group_by', 'append_having', 'append_order_by', 'append_prefix', 'append_whereclause', 'apply_labels', 'as_scalar', 'autocommit', 'bind', 'c', 'column', 'columns', 'compare', 'compile', 'correlate', 'correlate_except', 'correspond_on_equivalents', 'corresponding_column', 'count', 'cte', 'description', 'distinct', 'except_', 'except_all', 'execute', 'execution_options', 'for_update', 'foreign_keys', 'froms', 'get_children', 'group_by', 'having', 'inner_columns', 'intersect', 'intersect_all', 'is_clause_element', 'is_derived_from', 'is_selectable', 'join', 'label', 'lateral', 'limit', 'locate_all_froms', 'named_with_column', 'offset', 'order_by', 'outerjoin', 'params', 'prefix_with', 'primary_key', 'reduce_columns', 'replace_selectable', 'scalar', 'schema', 'select', 'select_from', 'selectable', 'self_group', 'suffix_with', 'supports_execution', 'tablesample', 'type', 'union', 'union_all', 'unique_params', 'where', 'with_for_update', 'with_hint', 'with_only_columns', 'with_statement_hint']

# # vs = "나는"
# # l = ['%s', '%s_', '__%s__']

# # for i in l:
# #     print(i % vs)
# # s = (0 - 1) * 2
# # print(s)


# # # import re
# # # s = "?order=desc&criteria=head&limit=20&order_by=head&offset=&search=%25%25"

# # # pattern = re.compile('offset=(.*[0-9])&')
# # # v = pattern.search(s)
# # # v = re.findall(pattern, s)[0]
# # # print(v)

# # import pymysql
# # import random


# # def get_conn(db='dooodb'):
# #     return pymysql.connect(
# #         host='localhost',
# #         user='dooo',
# #         password='',
# #         port=3306,
# #         db=db,
# #         charset='utf8')

# # sql_insert = "insert into Posts(head, content, author) values(%s,%s,%s)"
# # lst = []
# # heads = ['%s의 글의 제목입니다.', '%s의 글입니다.']
# # contents = ['강감찬은 강감하다.', '글의 내용은 없습니다.', '떨어저라! ^.^', '내이으아']
# # authors = [i for i in range(10)]

# # for i in range(1, 1000):
# #     v = random.randint(1, 10) % 2
# #     w = random.randint(1, 10) % 3
# #     x = random.randint(1, 10) % 10
# #     lst.append(
# #         tuple(
# #             (heads[v], contents[w], authors[x])
# #         )
# #     )

# # def save(lst):
# #     try:
# #         conn = get_conn('dooodb')
# #         conn.autocommit = False
# #         cur = conn.cursor()

# #         cur.executemany(sql_insert, lst)
# #         conn.commit()
# #         print("Affected RowCount is", cur.rowcount, "/", len(lst))

# #     except Exception as err:
# #         conn.rollback()
# #         print("Error!!", err)

# #     finally:
# #         try:
# #             cur.close()
# #         except:
# #             print("Error on close cursor")

# #         try:
# #             conn.close()
# #         except Exception as err2:
# #             print("Fail to connect!!", err2)


# # save(lst)

# # data = {"criteria": "head", "order": "desc", "order_by": "head", "limit": "20", "offset": "20"}

# # key_set = set(data.keys())
# # print(key_set, type(key_set), type(data.keys()))
# # print("limit" in key_set)
# # s = set(["limit", "criteria"])
# # v = key_set - s
# # print(v, type(v))
# # for w in v:
# #     print(w)
# #     print(data[w])

# #     {'criteria': 'head',
# #  'limit': '20',
# #  'offset': '0',
# #  'order': 'desc',
# #  'order_by': 'registdt',
# #  'search': ''}

# # class F():
# #     def __init__(self):
# #         self.data = [None]

# # f = F()
# # l = f.data and len(f.data) or 0
# # print(l)

# # s = zip([1, 2, 3], [4, 5, 6])
# # for ss in s:
# #     print(ss)

# # hol = jjak = 0
# # print(hol, jjak)
# # hol = 1
# # print(hol, jjak)

# # import datetime
# # print(datetime.datetime.now())
# # print(datetime.datetime.today())

# # kw = {'question_id': 1}

# # def f(**kwargs):
# #     print(kwargs, type(kwargs))
# #     print('이름: ', name)
# #     print('나이: ', age)
# #     print('주소: ', address)

# # def ff(name, **kwargs):
# #     print('이름: ', name)
# #     s = kwargs
# #     print(kwargs, '\n\n====111')
# #     print(s, '\n\n====111')
# #     def ffff(**kwargs):
# #         if(kwargs):
# #             print(kwargs, '\n\n====2222')
# #         print(s, '\n\n====222')
# #     return ffff(**kwargs)
#     # print(first, '\n\n====')

# # def fff(name, *args):
# #     print('이름: ', name)
# #     print(args, '\n\n====')

    
# # dd = {'name': 'kim', 'first':1}
# # ff(name='kim')
# # ff(**dd)
# # ddd = {'name': 'kim'}
# # fff(*[1,2,3],**ddd)
# ## fff(**ddd, *[1,2,3])
# # fff('kim', *[1,2,3])


# # def personal_info(name, age, address):
# #     print('이름: ', name)
# #     print('나이: ', age)
# #     print('주소: ', address)

# # x = {'name': '홍길동', 'age': 30, 'address': '서울시 용산구 이촌동'}
# # xx = [1,2,3]
# # personal_info(**x)
# # f(**x)


# from functools import wraps





# # def decorator_function(original_function): #1, #4 
# #     s = 3
# #     def wrapper_function(): #5 #8 
# #         print(s)
# #         return original_function() #9 
# #     return wrapper_function #6 
 
# # # def display(): #2, #10 
# # #     print("display 함수가 실행됐습니다") #11 

# # def index():
# #     print('>>>>>>> v ', locals(), vars(decorator_function))

# # # decorated_display = decorator_function(display)  #3 display 함수를 젇날 
# # # decorated_display = decorator_function(index)
# # # decorated_display() #7 

# # # print(vars(decorator_function))

# # print(dir(index), type(index))
# # for attr in dir(index):
# #     print("%s of index() : %s" % (attr, getattr(index, attr)))

# # index()


# def f1(): #outer function
#     f1.a = 1
#     def f2(): #outer function
#         print (f1.a) #prints 2
#     f2()
#     print (f1.a) #prints 2

# # f1()

# def f():
#     print("ssss", locals(), f1.s)
    
# def f1(a):
#     f1.s = 1000
#     print(f1.s, locals())

#     def f2(b):
#         print(f1.s, locals())
#         f()
#         return a+b
#     return f2
# a = f1(1)
# # print(type(f1))
# # b = f1(100)

# print (a(2))
# print(type((1,2)))
# # print (b(2))

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(">>>>", BASE_DIR)