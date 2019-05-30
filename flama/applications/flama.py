import typing

from starlette.staticfiles import StaticFiles

from flama.applications.base import BaseApp
from flama.applications.resources import ResourcesMixin
from flama.applications.schema import SchemaMixin

__all__ = ["Flama"]


class Flama(BaseApp, SchemaMixin, ResourcesMixin):
    def __init__(
        self,
        title: typing.Optional[str] = "",
        version: typing.Optional[str] = "",
        description: typing.Optional[str] = "",
        schema: typing.Optional[str] = "/schema/",
        docs: typing.Optional[str] = "/docs/",
        redoc: typing.Optional[str] = None,
        admin: typing.Optional[str] = "/admin/",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Add schema and docs routes
        self.add_schema_routes(
            title=title, version=version, description=description, schema_path=schema, docs_path=docs, redoc_path=redoc
        )

        # Add admin site routes
        self.add_admin_routes(path=admin)

        # Static
        self.mount(path="/_flama_static/", app=StaticFiles(packages=["flama"]), name="flama-static")
