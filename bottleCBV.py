import re
import sys
import inspect


_py2 = sys.version_info[0] == 2
_py3 = sys.version_info[0] == 3


class route(object):
    def __init__(self, rule, **options):
        """
        Class Initializer - This will only execute if using BottleCBV's original route() style.
        """

        # Not sure if this is needed, need to test what happens when you specify a rule but not options in BottleCBV.
        if not options:
            options = dict(method='ANY')
        self.rule = rule
        self.options = options

    def __call__(self, func):
        f = func
        rule = self.rule
        options = self.options

        def decorator(*args, **kwargs):
            if not hasattr(f, '_rule_cache') or f._rule_cache is None:
                f._rule_cache = {f.__name__: [(rule, options)]}
            elif not f.__name__ in f._rule_cache:
                f._rule_cache[f.__name__] = [(rule, options)]
            else:
                f._rule_cache[f.__name__].append((rule, options))
            return f

        return decorator()

    @staticmethod
    def decorate(f, rule, **options):
        if not hasattr(f, '_rule_cache') or f._rule_cache is None:
            f._rule_cache = {f.__name__: [(rule, options)]}
        elif not f.__name__ in f._rule_cache:
            f._rule_cache[f.__name__] = [(rule, options)]
        else:
            f._rule_cache[f.__name__].append((rule, options))
        return f

    @staticmethod
    def get(rule):
        """
        GET Method
        CRUD Use Case: Read
        Example:
          Request a user profile
        """
        options = dict(method='GET')

        def decorator(f):
            return route.decorate(f, rule, **options)

        return decorator

    @staticmethod
    def post(rule):
        """
        POST Method
        CRUD Use Case: Create
        Example:
          Create a new user
        """
        options = dict(method='POST')

        def decorator(f):
            return route.decorate(f, rule, **options)

        return decorator

    @staticmethod
    def put(rule):
        """
        PUT Method
        CRUD Use Case: Update / Replace
        Example:
          Set item# 4022 to Red Seedless Grapes, instead of tomatoes
        """
        options = dict(method='PUT')

        def decorator(f):
            return route.decorate(f, rule, **options)

        return decorator

    @staticmethod
    def patch(rule):
        """
        PATCH Method
        CRUD Use Case: Update / Modify
        Example:
          Rename then user's name from Jon to John
        """  
        options = dict(method='PATCH')

        def decorator(f):
            return route.decorate(f, rule, **options)

        return decorator

    @staticmethod
    def delete(rule):
        """
        DELETE Method
        CRUD Use Case: Delete
        Example:
          Delete user# 12403 (John)
        """
        options = dict(method='DELETE')

        def decorator(f):
            return route.decorate(f, rule, **options)

        return decorator

    @staticmethod
    def head(rule):
        """
        HEAD Method
        CRUD Use Case: Read (in-part)
        Note: This is the same as GET, but without the response body.
        
        This is useful for items such as checking if a user exists, such as this example:
          Request: GET /user/12403
          Response: (status code) 404 - Not Found
        
        If you are closely following the REST standard, you can also verify if the requested PATCH (update) was successfully applied, in this example:
          Request: PUT /user/12404 { "name": "John"}
          Response: (status code) 304 - Not Modified
        """
        options = dict(method='HEAD')

        def decorator(f):
            return route.decorate(f, rule, **options)

        return decorator

    @staticmethod
    def any(rule):
        """
        From the Bottle Documentation: 
          
        The non-standard ANY method works as a low priority fallback: Routes that listen to ANY will match requests regardless of their HTTP method but only if no other more specific route is defined. This is helpful for proxy-routes that redirect requests to more specific sub-applications.
        """
        options = dict(method='ANY')
        
        def decorator(f):
            return route.decorate(f, rule, **options)

        return decorator

class BottleView(object):
    """ Class based view implementation for bottle (following flask-classy architech)
    """
    decorators = []
    DEFAULT_ROUTES = ["get", "put", "post", "delete", "index", "options"]
    base_route = None
    route_prefix = None
    view_identifier = "view"

    @classmethod
    def register(cls, app, base_route=None, route_prefix=None):
        """ Register all the possible routes of the subclass
        :param app: bottle app instance
        :param base_route: prepend to the route rule (/base_route/<class_name OR route_prefix>)
        :param route_prefix: used when want to register custom rule, which is not class name
        """
        if cls is BottleView:
            raise TypeError("cls must be a subclass of BottleView, not BottleView itself")

        cls._app = app
        cls.route_prefix = route_prefix or cls.route_prefix
        cls.base_route = base_route or cls.base_route
        # import ipdb; ipdb.set_trace()
        # get all the valid members of  the class to register Endpoints
        routes = cls._get_interesting_members(BottleView)

        # initialize the class
        klass = cls()

        # Iterate through class members to register Endpoints
        for func_name, func in routes:
            # print "*"*50

            method_args = inspect.getargspec(func)[0]
            # Get
            rule = cls._build_route_rule(func_name, *method_args)
            method = "GET"

            if func_name in cls.DEFAULT_ROUTES:
                if func_name == "index":
                    method = "GET"
                else:
                    method = func_name.upper()

            # create name for endpoint
            endpoint = "%s:%s" % (cls.__name__, func_name)
            callable_method = getattr(klass, func_name)
            for decorator in cls.decorators:
                callable_method = decorator(callable_method)

            try:
                custom_rule = func._rule_cache
            except AttributeError:
                method_args = inspect.getargspec(func)[0]
                rule = cls._build_route_rule(func_name, *method_args)
                method = "GET"

                if func_name in cls.DEFAULT_ROUTES:
                    if func_name == "index":
                        method = "GET"
                    else:
                        method = func_name.upper()

                cls._app.route(callback=callable_method, method=method,
                               path=rule, name=endpoint)
            else:
                custom_rule_list = custom_rule.values()
                if _py3:
                    custom_rule_list = list(custom_rule_list)

                for cached_rule in custom_rule_list[0]:
                    rule, options = cached_rule
                    try:
                        method = options.pop("method")
                    except KeyError:
                        method = "GET"

                    try:
                        endpoint = options.pop("name")
                    except KeyError:
                        pass

                    cls._app.route(callback=callable_method, path=rule,
                                   method=method, name=endpoint, **options)

            print ("%s : %s, Endpoint: %s" % (method, rule, endpoint))

    @classmethod
    def _build_route_rule(cls, func_name, *method_args):

        klass_name = cls.__name__.lower()
        klass_name = (klass_name[:-len(cls.view_identifier)]
                      if klass_name.endswith(cls.view_identifier)
                      else klass_name)

        if not (cls.base_route or cls.route_prefix):
            rule = klass_name
        elif not cls.base_route and cls.route_prefix:
            rule = cls.route_prefix
        elif cls.base_route and not cls.route_prefix:
            rule = "%s/%s" % (cls.base_route, klass_name)
        elif cls.base_route and cls.route_prefix:
            rule = "%s/%s" % (cls.base_route, cls.route_prefix)

        rule_parts = [rule]

        if func_name not in cls.DEFAULT_ROUTES:
            rule_parts.append(func_name.replace("_", "-").lower())

        ignored_rule_args = ['self']
        if hasattr(cls, 'base_args'):
            ignored_rule_args += cls.base_args

        for arg in method_args:
            if arg not in ignored_rule_args:
                rule_parts.append("<%s>" % arg)

        result = "/%s/" % join_paths(*rule_parts)
        result = re.sub(r'(/)\1+', r'\1', result)
        result = re.sub("/{2,}", "/", result)

        return result

    @classmethod
    def _get_interesting_members(cls, base_class):
        """Returns a list of methods that can be routed to"""
        base_members = dir(base_class)
        predicate = inspect.ismethod if _py2 else inspect.isfunction
        all_members = inspect.getmembers(cls, predicate=predicate)
        return [member for member in all_members
                if not member[0] in base_members
                and ((hasattr(member[1], "__self__")
                      and not member[1].__self__ in cls.__class__.__mro__) if _py2 else True)
                and not member[0].startswith("_")]


def join_paths(*path_pieces):
    """Join parts of a url path"""
    # Remove blank strings, and make sure everything is a string
    cleaned_parts = map(str, filter(None, path_pieces))
    if _py3:
        cleaned_parts = list(cleaned_parts)

    return "/".join(cleaned_parts)
