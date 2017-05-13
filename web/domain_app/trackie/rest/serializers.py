from rest_framework.serializers import HyperlinkedModelSerializer


class OwnHyperlinkedModelSerializer(HyperlinkedModelSerializer):

    def get_default_field_names(self, declared_fields, model_info):
        return (
            [model_info.pk.name] +
            [self.url_field_name] +
            list(declared_fields.keys()) +
            list(model_info.fields.keys()) +
            list(model_info.forward_relations.keys())
        )