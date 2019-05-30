import datetime
import enum
import typing
import uuid

import marshmallow

try:
    from sqlalchemy import Table
except Exception:  # pragma: no cover
    Table = typing.Any

try:
    from databases import Database
except Exception:  # pragma: no cover
    Database = typing.Any

__all__ = [
    "FieldLocation",
    "Field",
    "EndpointInfo",
    "OptInt",
    "OptStr",
    "OptBool",
    "OptFloat",
    "OptUUID",
    "OptDate",
    "OptDateTime",
    "Model",
    "PrimaryKey",
    "ResourceMeta",
    "ResourceAdmin",
    "ResourceMethodMeta",
    "ResourceRegistryItem",
    "HTTPMethod",
    "APIError",
]


class FieldLocation(enum.Enum):
    query = enum.auto()
    path = enum.auto()
    body = enum.auto()


class Field(typing.NamedTuple):
    name: str
    location: FieldLocation
    schema: typing.Union[marshmallow.fields.Field, marshmallow.Schema]
    required: bool = False


class EndpointInfo(typing.NamedTuple):
    path: str
    method: str
    func: typing.Callable
    query_fields: typing.Dict[str, Field]
    path_fields: typing.Dict[str, Field]
    body_field: Field
    output_field: typing.Any


OptInt = typing.Optional[int]
OptStr = typing.Optional[str]
OptBool = typing.Optional[bool]
OptFloat = typing.Optional[float]
OptUUID = typing.Optional[uuid.UUID]
OptDate = typing.Optional[datetime.date]
OptDateTime = typing.Optional[datetime.datetime]


class PrimaryKey(typing.NamedTuple):
    name: str
    type: typing.Any


class Model(typing.NamedTuple):
    table: Table
    primary_key: PrimaryKey


class ResourceAdmin(typing.NamedTuple):
    list_columns: typing.Sequence[str]
    order_columns: typing.Sequence[str]


class ResourceMeta(typing.NamedTuple):
    model: Model
    input_schema: marshmallow.Schema
    output_schema: marshmallow.Schema
    database: Database
    name: str
    verbose_name: str
    admin: ResourceAdmin


class ResourceMethodMeta(typing.NamedTuple):
    path: str
    methods: typing.List[str] = ["GET"]
    name: str = None
    kwargs: typing.Dict[str, typing.Any] = {}


class ResourceRegistryItem(typing.NamedTuple):
    path: str
    admin: bool


HTTPMethod = enum.Enum("HTTPMethod", ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"])


class APIError(marshmallow.Schema):
    status_code = marshmallow.fields.Integer(title="status_code", description="HTTP status code", required=True)
    detail = marshmallow.fields.Raw(title="detail", description="Error detail", required=True)
    error = marshmallow.fields.String(title="type", description="Exception or error type")
