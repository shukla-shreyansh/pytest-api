from jsonschema import validate


class SchemaValidator:
    @classmethod
    def validate_schema(cls, data, schema):
        validate(instance=data, schema=schema)

