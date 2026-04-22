from xiot_core.spec.typedef.definition.property.access import Access


class AccessCodec:
    @staticmethod
    def decode(array: list[str]) -> Access:
        access_list = [x for x in array if isinstance(x, str)]
        return Access.value_of_list(access_list)
