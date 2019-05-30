import os
import typing

from marshmallow import Schema, fields

from flama.applications.base import BaseApp
from flama.responses import HTMLResponse
from flama.types import asgi
from flama.types.data_structures import ResourceRegistryItem

if typing.TYPE_CHECKING:
    from flama.resources import BaseResource

__all__ = ["ResourcesMixin"]


class ResourceMetadata(Schema):
    path = fields.String(title="path", description="Resource full path")
    name = fields.String(title="name", description="Resource unique name")
    verbose_name = fields.String(title="verbose_name", description="Verbose name")
    list_columns = fields.List(
        fields.String(), title="list_columns", description="List of columns to display on List view"
    )
    order_columns = fields.List(
        fields.String(), title="order_columns", description="List of columns used to sort on List view"
    )


class Metadata(Schema):
    resources = fields.Dict(
        title="resources", description="Resource list", keys=fields.String(), values=fields.Nested(ResourceMetadata)
    )
    admin = fields.String(title="admin", description="Admin URL")
    schema = fields.String(title="schema", description="OpenAPI schema URL")


def admin() -> HTMLResponse:
    with open(os.path.join(BaseApp.TEMPLATES_DIR, "admin.html")) as f:
        content = f.read()

    return HTMLResponse(content)


def metadata(app: asgi.App) -> Metadata:
    return {
        "resources": {
            resource._meta.name: {
                "path": registry_item.path + resource._meta.name + "/",
                "name": resource._meta.name,
                "verbose_name": resource._meta.verbose_name,
                "list_columns": resource._meta.admin.list_columns,
                "order_columns": resource._meta.admin.order_columns,
            }
            for resource, registry_item in app.resources.items()
            if registry_item.admin
        },
        "admin": app._admin_path,
        "schema": app._schema_path,
    }


class ResourcesMixin:
    resources = {}

    def add_admin_routes(self, path: typing.Optional[str] = "/admin/"):
        assert hasattr(self, "_schema_path"), "Schema generation is needed for Admin site"

        self._admin_path = path.rstrip("/") + "/"

        # Admin site
        self.add_route(path=self._admin_path, route=admin, include_in_schema=False, name="admin")

        # Metadata
        self.add_route(
            path=self._admin_path + "_metadata/", route=metadata, include_in_schema=False, name="admin-metadata"
        )

    def add_resource(self, path: str, resource: "BaseResource", admin: bool = True):
        self.resources[resource] = ResourceRegistryItem(path, admin)
        self.router.add_resource(path, resource=resource)

    def resource(self, path: str, admin: bool = True) -> typing.Callable:
        def decorator(resource: "BaseResource") -> "BaseResource":
            self.resources[resource] = ResourceRegistryItem(path, admin)
            self.router.add_resource(path, resource=resource)
            return resource

        return decorator
