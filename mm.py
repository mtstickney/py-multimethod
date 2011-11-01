"""Implementation of multimethods, similar in spirit to
http://www.artima.com/weblogs/viewpost.jsp?thread=101605"""

multimethod_lst = {}

class MultiMethod:
    def __init__(self, fname, summary_func):
        self.dispatch_tbl = {}
        self.name = fname
        self.summarize = summary_func

    def __call__(self, *args, **kwargs):
        k = self.summarize(*args, **kwargs)
        if k not in self.dispatch_tbl:
            s = "Multimethod '{}': No method for summary value '{}'".format(self.name, k)
            raise Exception(s)
        return self.dispatch_tbl[k](*args, **kwargs)

    def register(self, f, summary):
        self.dispatch_tbl[summary] = f

class StrictMultiMethod(MultiMethod):
    def register(self, f, summary):
        if summary in self.dispatch_tbl:
            s = "MultiMethod '{}': Redefining method for summary value '{}'".format(self.name, summary)
            raise Exception(s)
        self.dispatch_tbl[summary] = f

def multimethod(name, sfunc, strict=False):
    if strict:
        mm = StrictMultiMethod(name, sfunc)
    else:
        mm = MultiMethod(name, sfunc)
    multimethod_lst[name] = mm

def defmulti(summary):
    def register(func):
        mm = multimethod_lst[func.__name__]
        mm.register(func, summary)
        return mm
    return register
