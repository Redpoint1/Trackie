import django.db.models.fields as db_fields
from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import HyperlinkedRelatedField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.exceptions import ValidationError, APIException
from ..racer.serializers import RaceRacerSerializer
from ......trackie.models import RaceData, Race


class RaceDataGeoJSONPostSerializer(GeoFeatureModelSerializer):
    race = HyperlinkedRelatedField("race-detail", queryset=Race.objects.all())

    class Meta:
        model = RaceData
        geo_field = "position"
        exclude = []

    def validate_data(self, value):
        fields = self.context["view"].queryset[0].type.fields.all()
        errors = dict()
        raise_500 = False
        checked_fields = set()

        for field in fields:
            checked_fields.add(field.name)
            errors[field.name] = list()
            json_value = value.get(field.name)

            try:
                django_class = getattr(db_fields, field.type)
                rest_field, rest_kwargs = self.build_standard_field(field.name, django_class())
            except (AttributeError, KeyError):
                errors[field.name].append(_("Unknown field type '{}'").format(field.name, field.type))
                raise_500 = True
                continue

            obj = rest_field(**rest_kwargs)

            try:
                obj.run_validation(data=json_value)
            except ValidationError as e:
                errors[field.name].extend(e.detail)

            if not errors[field.name]:
                errors.pop(field.name)

        unchecked_fields = set(value.keys()) - checked_fields

        for unchecked_field in unchecked_fields:
            errors[unchecked_field] = [_("Unexpected field")]

        if any(list(map(len, errors.values()))):
            if raise_500:
                raise APIException(detail=errors)
            raise ValidationError(detail=errors)

        return value


class RaceDataGeoJSONSerializer(RaceDataGeoJSONPostSerializer):
    race = HyperlinkedRelatedField("race-detail", read_only=True)
    racer = RaceRacerSerializer(source="racer.racer")
