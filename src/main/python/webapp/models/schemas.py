from sqlalchemy import func
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema, ModelConverter, field_for
from geoalchemy2 import Geography
from models import *

class GeoConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        Geography: fields.Str
    })

class GeographySerializationField(fields.String):
    def _serialize(self, value, attr, obj):
        if value is None:
            return value
        else:
            if attr == 'geo':
                return {'latitude': db.session.scalar(func.ST_X(value)), 'longitude': db.session.scalar(func.ST_Y(value))}
            else:
                return None

    def _deserialize(self, value, attr, data):
        """Deserialize value. Concrete :class:`Field` classes should implement this method.

        :param value: The value to be deserialized.
        :param str attr: The attribute/key in `data` to be deserialized.
        :param dict data: The raw input data passed to the `Schema.load`.
        :raise ValidationError: In case of formatting or validation failure.
        :return: The deserialized value.

        .. versionchanged:: 2.0.0
            Added ``attr`` and ``data`` parameters.
        """
        if value is None:
            return value
        else:
            if attr == 'loc':
                return WKTGeographyElement('POINT({0} {1})'.format(str(value.get('longitude')), str(value.get('latitude'))))
            else:
                return None

class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ('search_vector',)

class PinSchema(ModelSchema):
    geo = GeographySerializationField(attribute='geo')
    class Meta:
        model = Pin
        sqla_session = db.session
        model_converter = GeoConverter
        exclude = ('search_vector',)

class VoteSchema(ModelSchema):
    class Meta:
        model = Vote

class CommentSchema(ModelSchema):
    class Meta:
        model = Comment
        exclude = ('search_vector',)

class TagSchema(ModelSchema):
    class Meta:
        model = Tag
        exclude = ('search_vector',)

class PinTagSchema(ModelSchema):
    class Meta:
        model = PinTag

