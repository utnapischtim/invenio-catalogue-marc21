# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 UI record response serializers."""

from flask_resources import BaseListSchema, JSONSerializer, MarshmallowSerializer

from .schema import Marc21CatalogueDepositSchema


class Marc21CatalogueDepositSerializer(MarshmallowSerializer):
    """UI JSON serializer implementation."""

    def __init__(self) -> None:
        """Marc21 UI JSON Constructor.

        :param object_schema_cls: object schema serializing the Marc21 record. (default: `Marc21Schema`)
        :param object_key: str key dump ui specific information
        """
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=Marc21CatalogueDepositSchema,
            list_schema_cls=BaseListSchema,
        )
