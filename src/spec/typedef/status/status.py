from typing import Final

class Status:
    UNDEFINED: Final[int] = -1
    COMPLETED: Final[int] = 0
    TO_BE_EXECUTE: Final[int] = 1
    INTERNAL_ERROR: Final[int] = -500
    ACCESS_KEY_INVALID: Final[int] = -501
    DEVICE_ID_NOT_EXIST: Final[int] = -502
    QUERY_NOT_SUPPORTED: Final[int] = -503
    TIMEOUT: Final[int] = -504

    # FOR XCP DEVICE ENDPOINT VERIFY
    DEVICE_ID_INVALID: Final[int] = -100
    DEVICE_TYPE_INVALID: Final[int] = -101
    PUBLIC_KEY_NOT_FOUND: Final[int] = -102
    SIGNATURE_NOT_FOUND: Final[int] = -103
    VERSION_NOT_FOUND: Final[int] = -104
    AUTHENTICATION_NOT_FOUND: Final[int] = -105
    AUTHENTICATION_NOT_SUPPORTED: Final[int] = -106
    STATUS_INVALID: Final[int] = -107
    SIGNATURE_INVALID: Final[int] = -108
    CODEC_NOT_FOUND: Final[int] = -109
    CODEC_NOT_IMPLEMENTED: Final[int] = -110
    DEVICE_ALREADY_ONLINE: Final[int] = -111

    # FOR OPERATION
    DEVICE_OFFLINE: Final[int] = -400
    AUTHENTICATION_FAILED: Final[int] = -401
    SERVICE_NOT_FOUND: Final[int] = -410
    PID_INVALID: Final[int] = -420
    PROPERTY_NOT_FOUND: Final[int] = -421
    PROPERTY_CANNOT_READ: Final[int] = -422
    PROPERTY_CANNOT_WRITE: Final[int] = -423
    PROPERTY_CANNOT_NOTIFY: Final[int] = -424
    PROPERTY_VALUE_INVALID: Final[int] = -425
    PROPERTY_VALUE_ERROR: Final[int] = -426
    DUPLICATE_PID: Final[int] = 427
    AID_INVALID: Final[int] = -430
    ACTION_NOT_FOUND: Final[int] = -431
    ACTION_IN_ERROR: Final[int] = -432
    ACTION_IN_VALUE_INVALID: Final[int] = -433
    ACTION_OUT_ERROR: Final[int] = -434
    ACTION_OUT_VALUE_INVALID: Final[int] = -435
    DUPLICATE_AID: Final[int] = 436
    EID_INVALID: Final[int] = -440
    EVENT_NOT_FOUND: Final[int] = -441
    EVENT_ARGUMENTS_ERROR: Final[int] = -442
    EVENT_ARGUMENTS_VALUE_ERROR: Final[int] = -443

    # FOR C2C
    CLOUD_ERROR: Final[int] = -600
    CLOUD_NOT_AUTHORIZED: Final[int] = -601
    CLOUD_AUTHORIZATION_EXPIRED: Final[int] = -602

    # FOR CONTROLLER
    OWNERSHIP_NOT_FOUND: Final[int] = -700
    NO_PERMISSION: Final[int] = -701

    # FOR RULE
    RULE_ID_NOT_FOUND: Final[int] = -750

    # FOR SPACE USER
    USER_ID_NOT_FOUND: Final[int] = -801