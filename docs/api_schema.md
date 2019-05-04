# API Schemas

Starlette API includes optional support for generating 
[OpenAPI schemas][openapi], using `apispec` and `pyyaml` libraries.
 
The Schema generator gathers all the API information needed directly from your 
code and infers the schema for your application based on OpenAPI standard. The 
schema will be also served under `/schema/` route by default.

Let's take a look at that with an example including all the pieces involved in 
the generation of the API schema:

## Data Schemas

```python
from marshmallow import Schema, fields, validate


class Puppy(Schema):
    id = fields.Integer()
    name = fields.String()
    age = fields.Integer(validate=validate.Range(min=0))
```

## Routes

```python
from . import schemas


def list_puppies(name: str = None) -> schemas.Puppy(many=True):
    """
    tags:
        - puppy
    summary:
        List puppies.
    description:
        List the puppies collection. There is an optional query parameter that 
        specifies a name for filtering the collection based on it.
    responses:
        200:
            description: List puppies.
    """
    ...
    

def create_puppy(puppy: schemas.Puppy) -> schemas.Puppy:
    """
    tags:
        - puppy
    summary:
        Create a new puppy.
    description:
        Create a new puppy using data validated from request body and add it 
        to the collection.
    responses:
        200:
            description: Puppy created successfully.
    """
    ...
```


## Application

```python
from flama.applications import Flama

from . import views


app = Flama(
    title="Puppy Register",               # API title
    version="0.1",                        # API version
    description="A register of puppies",  # API description
    schema="/schema/",                    # Path to expose OpenAPI schema
)


app.add_route("/", views.list_puppies, methods=["GET"])
app.add_route("/", views.create_puppy, methods=["POST"])
```

## Schema

```yaml
components:
  parameters: {}
  schemas:
    APIError:
      properties:
        status_code:
          description: HTTP status code
          format: int32
          title: status_code
          type: integer
        detail:
          description: Error detail
          title: detail
          type: string
        error:
          description: Exception or error type
          title: type
          type: string
      required:
      - detail
      - status_code
      type: object
    Puppy:
      properties:
        name:
          type: string
        age:
          format: int32
          minimum: 0
          type: integer
        id:
          format: int32
          type: integer
      type: object
info:
  description: A register of puppies
  title: Puppy Register
  version: '0.1'
openapi: 3.0.0
paths:
  /:
    get:
      description: List the puppies collection. There is an optional query parameter
        that specifies a name for filtering the collection based on it.
      parameters:
      - in: query
        name: name
        required: false
        schema:
          default: null
          nullable: true
          type: string
      responses:
        200:
          content:
            application/json:
              schema:
                items:
                  $ref: '#/components/schemas/Puppy'
                type: array
          description: List puppies.
        default:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/APIError'
          description: Unexpected error.
      summary: List puppies.
      tags:
      - puppy
    post:
      description: Create a new puppy using data validated from request body and add
        it to the collection.
      requestBody:
        content:
          application/json:
            schema:
              properties:
                age:
                  format: int32
                  minimum: 0
                  type: integer
                id:
                  format: int32
                  type: integer
                name:
                  type: string
              type: object
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Puppy'
          description: Puppy created successfully.
        default:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/APIError'
          description: Unexpected error.
      summary: Create a new puppy.
      tags:
      - puppy
tags: []
```

You can disable the schema generation by using `None` value for the `schema` argument.

```python
from flama.applications import Flama

app = Flama(
    title="Puppy Register",               # API title
    version="0.1",                        # API version
    description="A register of puppies",  # API description
    schema=None,                          # Disable api schema generation
)
```

[openapi]: https://github.com/OAI/OpenAPI-Specification
