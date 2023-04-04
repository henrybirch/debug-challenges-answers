# You need to create a function that parses a .txt file that is csv-formatted
# into a dataframe-like python object

# Your function should return columns with correct types. If the type of the column
# can not be inferred as the same throughout, e.g. int, the column should default to str.

# Lists should only be typed if the types they contain are homogenous.
# e.g. 30|fifty should default to List[str], 30|20 can be List[int]

# Check every piece of data in a column to make sure the types are homogenous
from types import NoneType
from typing import (
    NewType,
    Any,
    List,
    Optional,
    Dict,
    TypeVar,
    Union,
    Literal,
    Type,
)

Column = Union[
    List[Optional[str]],
    List[Optional[int]],
    List[Optional[float]],
    List[Optional[List[Optional[str]]]],
    List[Optional[List[Optional[int]]]],
    List[Optional[List[Optional[float]]]],
]

DataFrame = Dict[str, Column]


class InvalidNumberOfColumnsError(Exception):
    pass


def parse_csv(text: List[str]) -> DataFrame:
    def represent_type(t: Type[float | int], s: str) -> bool:
        try:
            t(s)
        except ValueError:
            return False
        return True

    def get_value_type_for_column(column: List[str]):
        def get_value_type_single(
            value: str,
        ) -> Type[NoneType | str | int | float]:
            if value in ("None", ""):
                return NoneType

            for type in [int, float]:
                if represent_type(type, value):
                    return type

            return str

        class TypeRepresentation:
            def __init__(
                self, type: Type[NoneType | str | int | float], is_list: bool
            ):
                self.type = type
                self.is_list = is_list

            def __eq__(self, other):
                return (
                    self.type is other.type and self.is_list is other.is_list
                )

        def get_value_type(value: str) -> TypeRepresentation:
            first_type_pass = get_value_type_single(value)

            if first_type_pass is not str:
                return TypeRepresentation(first_type_pass, False)

            if "|" not in value:
                return TypeRepresentation(str, False)

            value_types = [
                get_value_type_single(value) for value in value.split("|")
            ]

            for meta_type in [NoneType, str, float, int]:
                if all(
                    value_type is meta_type or value_type is NoneType
                    for value_type in value_types
                ):
                    return TypeRepresentation(meta_type, True)

        def reduce_types(
            types: List[TypeRepresentation],
        ) -> TypeRepresentation:
            first_non_none_type: TypeRepresentation | None = None
            for value_type in types:
                if value_type.type is NoneType:
                    continue
                if (
                    first_non_none_type is not None
                    and first_non_none_type != value_type
                ):
                    return TypeRepresentation(str, False)
            return first_non_none_type
