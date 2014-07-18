from bottleCBV.bottleCBV import BottleView, route
from functools import wraps

VALUE1 = "value1"

def get_value():
    return VALUE1

class BasicView(BottleView):

    def index(self):
        """A docstring for testing that docstrings are set"""
        return "Index"

    def get(self, obj_id):
        return "Get " + obj_id

    def put(self, id):
        return "Put " + id

    def patch(self, id):
        return "Patch " + id

    def post(self):
        return "Post"

    def delete(self, id):
        return "Delete " + id

    def custom_method(self):
        return "Custom Method"

    def custom_method_with_params(self, p_one, p_two):
        return "Custom Method %s %s" % (p_one, p_two,)

    @route("/routed/")
    def routed_method(self):
        return "Routed Method"

    @route("/route1/")
    @route("/route2/")
    def multi_routed_method(self):
        return "Multi Routed Method"

    @route("/noslash")
    def no_slash_method(self):
        return "No Slash Method"

    @route("/endpoint/", name="basic_endpoint")
    def custom_endpoint(self):
        return "Custom Endpoint"

    @route("/route3/", methods=['POST'])
    def custom_http_method(self):
        return "Custom HTTP Method"


class IndexView(BottleView):
    route_base = "/"
    route_prefix = "/"
    def index(self):
        return "Index"


class RouteBaseView(BottleView):
    route_base = "/base-routed/"

    def index(self):
        return "Index"


class RoutePrefixView(BottleView):
    route_prefix = "/my_prefix/"

    def index(self):
        return "Index"


class VariedMethodsView(BottleView):

    def index(self):
        return "Index"

    @route("/routed/")
    def routed_method(self):
        return "Routed Method"

    @classmethod
    def class_method(cls):
        return "Class Method"

class SubVariedMethodsView(VariedMethodsView):
    pass

def func_decorator(f):
    def decorated_view(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_view

def wraps_decorator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
      return f(*args, **kwargs)
    return decorated_view


def params_decorator(p_1, p_2):
    def decorator(f):
       @wraps(f)
       def decorated_function(*args, **kwargs):
           return f(*args, **kwargs)
       return decorated_function
    return decorator


def recursive_decorator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        decorated_view.foo()
        return f(*args, **kwargs)

    def foo():
        return 'bar'
    decorated_view.foo = foo

    return decorated_view

def more_recursive(stop_type):
    def _inner(func):
        def _recursive(*args, **kw):
            return func(*args, **kw)
        return _recursive
    return _inner


class DecoratedView(BottleView):
    @func_decorator
    def index(self):
        return "Index"

    @func_decorator
    def get(self, id):
        return "Get " + id

    @recursive_decorator
    def post(self):
        return "Post"

    @params_decorator("oneval", "anotherval")
    def params_decorator_method(self):
        return "Params Decorator"

    @params_decorator(get_value(), "value")
    def delete(self, obj_id):
        return "Params Decorator Delete " + obj_id


    @more_recursive(None)
    def get_some(self):
        return "Get Some"

    @more_recursive(None)
    @recursive_decorator
    def get_this(self):
        return "Get This"

    @route('/mixitup')
    @more_recursive(None)
    @recursive_decorator
    def mixitup(self):
        return "Mix It Up"

    @more_recursive(None)
    def someval(self, val):
        return "Someval " + val

    @route('/anotherval/<val>')
    def anotherval(self, val):
        return "Anotherval " + val



class InheritanceView(BasicView):

    # Tests method override
    def get(self, obj_id):
        return "Inheritance Get " + obj_id

    @route('/<obj_id>/delete', methods=['DELETE'])
    def delete(self, obj_id):
        return "Inheritance Delete " + obj_id

    @route('/with_route')
    def with_route(self):
        return "Inheritance with route"


class DecoratedInheritanceView(DecoratedView):

    @recursive_decorator
    def get(self, obj_id):
        return "Decorated Inheritance Get " + obj_id
