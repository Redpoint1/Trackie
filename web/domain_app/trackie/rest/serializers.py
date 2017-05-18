from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_bulk.serializers import BulkListSerializer
from rest_framework.exceptions import ValidationError


class OwnHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    def get_default_field_names(self, declared_fields, model_info):
        return (
            [model_info.pk.name] +
            [self.url_field_name] +
            list(declared_fields.keys()) +
            list(model_info.fields.keys()) +
            list(model_info.forward_relations.keys())
        )


class FixBulkListSerializer(BulkListSerializer):
    def to_internal_value(self, data):
        try:
            return super(BulkListSerializer, self).to_internal_value(data)
        except AttributeError:
            pass

        instance_map = {
            getattr(i, self.update_lookup_field): i for i in self.instance
        }

        ret = []
        errors = []
        for item in data:
            field = item[self.update_lookup_field]
            self.child.instance = instance_map.get(field)
            try:
                validated = self.child.run_validation(item)
            except ValidationError as exc:
                errors.append(exc.detail)
            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise ValidationError(errors)

        return ret
