from bottleCBV import BottleView, route


VALUE1 = "value1"


def get_value():
    return VALUE1


def mydecorator(original_function):
    def new_function(*args, **kwargs):
        resp = original_function(*args, **kwargs)
        return "decorator:%s" % resp
    return new_function


class BasicView(BottleView):

    def index(self):
        """A docstring for testing that docstrings are set"""
        return "Index"

    def get(self, obj_id):
        return "Get:" + obj_id

    def put(self, id):
        return "Put " + id

    def post(self):
        return "Post"

    def delete(self, id):
        return "Delete " + id

    def mymethod(self):
        return "My Method"

    def mymethod_args(self, p_one, p_two):
        return "My Method %s %s" % (p_one, p_two,)

    @route("/endpoint/")
    def mymethod_route(self):
        return "Custom Route"

    @route("/endpoint/", method=["POST", "PUT"])
    def mymethod_route_post(self):
        from bottle import request
        return "Custom Route %s" % request.method.upper()

    @route("/route1/")
    @route("/route2/")
    def multi_routed_method(self):
        return "Multi Routed Method"


class RouteBaseView(BottleView):
    base_route = "my"
    def index(self):
        return "index-route-base"


class RoutePrefixView(BottleView):
    route_prefix = "/"
    def index(self):
        return "index-route-prefix"

    def post(self):
        return "post-route-prefix"

    def get(self):
        return "get-route-prefix"


class DecoratorView(BottleView):
    decorators = [mydecorator]
    def index(self):
        return "index"

    def post(self):
        return "post"

    def get(self, val):
        return "get:%s" % val

    def myfunc(self, arg1):
        return "get:myfunc:%s" % arg1

    @route("/my-custom-route/")
    def my_custom_route(self):
        return "get:my-custom-route"

class SingleDecoratorView(BottleView):

    def index(self):
        return "index"

    @mydecorator
    def post(self):
        return "post"

    def get(self, val):
        return "get:%s" % val

