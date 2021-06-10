from rest_framework.renderers import CoreJSONRenderer, coreapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.coreapi import LinkNode, insert_into
from rest_framework_swagger import renderers


class CustomSchemaGenerator(SchemaGenerator):
    """
    自定义SchemaGenerator
    """
    def get_links(self, request=None):
        links = LinkNode()

        paths = []
        view_endpoints = []
        for path, method, callback in self.endpoints:
            view = self.create_view(callback, method, request)
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue
            link = view.schema.get_link(path, method, base_url=self.url)
            link._fields += self.get_core_fields(view)

            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, view)

            insert_into(links, keys, link)

        return links

    # Take our custom parameters from the class and pass them to swagger to generate the interface documentation.
    @staticmethod
    def get_core_fields(view):
        return getattr(view, 'core_api_fields', ())


class SwaggerSchemaView(APIView):
    """
    SwaggerSchemaView
    """
    _ignore_model_permissions = False
    exclude_from_schema = False
    # 认证类，不需要登录的接口，配置为[]
    authentication_classes = []
    # 权限判断类，不需要权限的接口，配置为[]，或[AllowAny, ]
    permission_classes = [AllowAny, ]
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        # print(request.path)
        generator = CustomSchemaGenerator(title="格格足迹服务端", description="格格足迹的服务端相关接口测试和文档说明")
        schema = generator.get_schema(request=request)
        return Response(schema)


def DocParam(name="default", location="query", required=True, description=None,
             type="string", schema=None, example=None, *args, **kwargs):
    """
    构造参数
    :param name: Field name
    :param location: The location of the parameter. Possible values are "query", "header", "path", "formData" or "body".
    :param required: Enter Field True or False
    :param description: Parameter Description
    :param type: The value MUST be one of "string", "number", "integer", "boolean", "array" or "file"
    :param schema:
    :param example:
    :param args:
    :param kwargs:
    :return:
    """

    return coreapi.Field(name=name, location=location,
                         required=required, description=description,
                         type=type)
