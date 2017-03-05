from drf_extra_fields.fields import Base64ImageField
from versatileimagefield.utils import (
    build_versatileimagefield_url_set,
    get_rendition_key_set,
    validate_versatileimagefield_sizekey_list
)


class ImageLimitField(Base64ImageField):
    read_only = True

    ALLOWED_TYPES = (
        "jpeg",
        "jpg",
        "png",
    )

    def __init__(self, sizes, *args, **kwargs):
        if isinstance(sizes, str):
            sizes = get_rendition_key_set(sizes)
        self.sizes = validate_versatileimagefield_sizekey_list(sizes)
        super(ImageLimitField, self).__init__(*args, **kwargs)

    def to_representation(self, file):
        context_request = None
        if self.context:
            context_request = self.context.get('request', None)
        return build_versatileimagefield_url_set(
            file,
            self.sizes,
            request=context_request
        )
