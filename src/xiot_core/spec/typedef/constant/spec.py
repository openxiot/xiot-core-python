from typing import Final


class Spec:
    """
    模拟 Java 接口的常量容器类
    所有常量为类级别的 Final 常量，不可修改
    """
    CATEGORY: Final[str] = "category"
    NAME: Final[str] = "name"
    NAMESPACE: Final[str] = "namespace"
    IID: Final[str] = "iid"
    TYPE: Final[str] = "type"
    DESCRIPTION: Final[str] = "description"
    SERVICES: Final[str] = "services"
    PROPERTIES: Final[str] = "properties"
    ACTIONS: Final[str] = "actions"
    EVENTS: Final[str] = "events"
    ACCESS: Final[str] = "access"
    FORMAT: Final[str] = "format"
    VALUE_LIST: Final[str] = "value-list"
    VALUE_RANGE: Final[str] = "value-range"
    VALUE_LENGTH: Final[str] = "value-length"
    IN: Final[str] = "in"
    OUT: Final[str] = "out"
    ARGUMENTS: Final[str] = "arguments"
    VALUE: Final[str] = "value"
    UNIT: Final[str] = "unit"
    PIID: Final[str] = "piid"
    PROPERTY: Final[str] = "property"
    REPEAT: Final[str] = "repeat"
    VALUES: Final[str] = "values"
    MEMBERS: Final[str] = "members"
    ELEMENT: Final[str] = "element"
    SIZE: Final[str] = "size"

    DEFAULT_VALUE: Final[str] = "default-value"

    REQUIRED_SERVICES: Final[str] = "required-services"
    OPTIONAL_SERVICES: Final[str] = "optional-services"

    REQUIRED_ACTIONS: Final[str] = "required-actions"
    OPTIONAL_ACTIONS: Final[str] = "optional-actions"

    REQUIRED_EVENTS: Final[str] = "required-events"
    OPTIONAL_EVENTS: Final[str] = "optional-events"

    REQUIRED_PROPERTIES: Final[str] = "required-properties"
    OPTIONAL_PROPERTIES: Final[str] = "optional-properties"

    DESCRIPTION_ZH_CN: Final[str] = "zh-CN"
    DESCRIPTION_ZH_TW: Final[str] = "zh-TW"
    DESCRIPTION_EN_US: Final[str] = "en-US"

    X_REQUIRED: Final[str] = "x-required"
    X_PROPERTY_ADDABLE: Final[str] = "x-property-addable"
    X_ACTION_ADDABLE: Final[str] = "x-action-addable"
    X_EVENT_ADDABLE: Final[str] = "x-event-addable"

    PROPERTY_FIRMWARE_REVISION: Final[str] = "firmware-revision"