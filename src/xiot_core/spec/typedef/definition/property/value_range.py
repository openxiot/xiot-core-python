from typing import List, Optional, Generic, TypeVar

from xiot_core.spec.typedef.definition.property.constraint_value import ConstraintValue
from xiot_core.spec.typedef.definition.property.data.data_format import DataFormat
from xiot_core.spec.typedef.definition.property.data.data_value import DataValue

T = TypeVar('T')

class ValueRange(ConstraintValue[T], Generic[T]):
    def __init__(self, format_: DataFormat, list_: List[object] = None,
                 min_: object = None, max_: object = None, step_: object = None):
        self.format = format_
        self.min_value: Optional[DataValue[T]] = None
        self.max_value: Optional[DataValue[T]] = None
        self.step_value: Optional[DataValue[T]] = None
        self.has_step = False

        if list_ is not None:
            if len(list_) == 2:
                self._init(format_, list_[0], list_[1], None)
            elif len(list_) == 3:
                self._init(format_, list_[0], list_[1], list_[2])
            else:
                raise ValueError("value list is invalid (size must be 2 or 3)")
        elif min_ is not None and max_ is not None:
            self._init(format_, min_, max_, step_)
        else:
            raise ValueError("invalid parameters")

    def _init(self, fmt: DataFormat, min_: object, max_: object, step: object) -> None:
        self.min_value = fmt.create_value(min_)
        self.max_value = fmt.create_value(max_)
        min_value = self.min_value
        max_value = self.max_value

        if min_value is None:
            raise ValueError(f"minValue invalid: {type(min_).__name__} => {min_}")
        if max_value is None:
            raise ValueError(f"maxValue invalid: {type(max_).__name__} => {max_}")

        if step is not None:
            self.step_value = fmt.create_value(step)
            self.has_step = True
            if self.step_value is None:
                raise ValueError(f"stepValue invalid: {type(step).__name__} => {step}")
        else:
            self.step_value = None
            self.has_step = False

        if not fmt.check_min_max(min_value, max_value, self.step_value):
            raise ValueError(f"check(min, max, step) failed, min: {min_} max: {max_} step:{step}")

    def validate(self, value: DataValue[T]) -> bool:
        min_value = self.min_value
        max_value = self.max_value

        if min_value is None:
            raise ValueError("minValue is None")

        if max_value is None:
            raise ValueError("maxValue is None")

        return self.format.validate(
            value, min_value, max_value,
            self.step_value if self.has_step else None
        )

    @property
    def min_value(self) -> Optional[DataValue[T]]:
        return self._min_value

    @min_value.setter
    def min_value(self, val: DataValue[T]) -> None:
        self._min_value = val

    @property
    def max_value(self) -> Optional[DataValue[T]]:
        return self._max_value

    @max_value.setter
    def max_value(self, val: DataValue[T]) -> None:
        self._max_value = val

    @property
    def step_value(self) -> Optional[DataValue[T]]:
        return self._step_value

    @step_value.setter
    def step_value(self, val: DataValue[T]) -> None:
        self._step_value = val

    def to_list(self) -> List[object]:
        min_ = self.min_value
        max_ = self.max_value
        step_ = self.step_value
        if min_ is None or max_ is None:
            raise ValueError("min or max is None")
        list_ = [min_.raw_value(), max_.raw_value()]
        if self.has_step:
            if step_ is None:
                raise ValueError("step is None")
            else:
                list_.append(step_.raw_value())
        return list_