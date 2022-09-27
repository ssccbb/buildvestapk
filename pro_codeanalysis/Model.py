class Code:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.codes = []


class Base:

    def __init__(self, name, code_start, code_end):
        self.name = ''
        self.code_area = []
        self.permission = ''
        self.modifier = []
        if name is not None:
            self.name = name
        if code_start is None or code_end is None or code_start == code_end:
            self.code_area = [code_end if code_start is None else code_start]
        elif code_start <= code_end:
            self.code_area = [code_start, code_end]
            print('Base.__init__()')
        pass


class Class(Base):

    def __init__(self):
        Base.__init__(self, '', 0, 0)
        self.type = ''
        self.package = ''
        self.parent = ''
        self.implement = []
        self.methods = []
        self.vars = []
        self.import_lib = []
        self.inner_class = []
        pass


class Method(Base):

    def __init__(self, method_type, name, code_start, code_end):
        Base.__init__(self, name, code_start, code_end)
        self.return_type = ''
        self.input_param = []
        # 构造方法 or 普通方法
        self.method_type = method_type
        pass


class Var(Base):
    def __init__(self):
        Base.__init__(self)
        self.type = ''
        pass


class Notes(Base):
    def __init__(self, code_start, code_end):
        Base.__init__(self, "", code_start, code_end)
        pass
