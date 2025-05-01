from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Type

__NAMESPACE__ = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"


class AggregationType(Enum):
    FORECAST_MODEL_RUN_COLLECTION = "forecastModelRunCollection"
    FORECAST_MODEL_RUN_SINGLE_COLLECTION = "forecastModelRunSingleCollection"
    JOIN_EXISTING = "joinExisting"
    JOIN_NEW = "joinNew"
    TILED = "tiled"
    UNION = "union"


class DataType(Enum):
    BYTE = "byte"
    CHAR = "char"
    SHORT = "short"
    INT = "int"
    LONG = "long"
    FLOAT = "float"
    DOUBLE = "double"
    STRING = "String"
    STRING_1 = "string"
    STRUCTURE = "Structure"
    SEQUENCE = "Sequence"
    OPAQUE = "opaque"
    ENUM1 = "enum1"
    ENUM2 = "enum2"
    ENUM4 = "enum4"
    UBYTE = "ubyte"
    USHORT = "ushort"
    UINT = "uint"
    ULONG = "ulong"


class ObjectType(Enum):
    ATTRIBUTE = "attribute"
    DIMENSION = "dimension"
    VARIABLE = "variable"
    GROUP = "group"


@dataclass
class CacheVariable:
    class Meta:
        name = "cacheVariable"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Dimension:
    class Meta:
        name = "dimension"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    length: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    is_unlimited: bool = field(
        default=False,
        metadata={
            "name": "isUnlimited",
            "type": "Attribute",
        },
    )
    is_variable_length: bool = field(
        default=False,
        metadata={
            "name": "isVariableLength",
            "type": "Attribute",
        },
    )
    is_shared: bool = field(
        default=True,
        metadata={
            "name": "isShared",
            "type": "Attribute",
        },
    )
    org_name: str | None = field(
        default=None,
        metadata={
            "name": "orgName",
            "type": "Attribute",
        },
    )


@dataclass
class LogicalReduce:
    class Meta:
        name = "logicalReduce"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    dim_names: str | None = field(
        default=None,
        metadata={
            "name": "dimNames",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LogicalSection:
    class Meta:
        name = "logicalSection"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    section: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LogicalSlice:
    class Meta:
        name = "logicalSlice"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    dim_name: str | None = field(
        default=None,
        metadata={
            "name": "dimName",
            "type": "Attribute",
            "required": True,
        },
    )
    index: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PromoteGlobalAttribute:
    class Meta:
        name = "promoteGlobalAttribute"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    org_name: str | None = field(
        default=None,
        metadata={
            "name": "orgName",
            "type": "Attribute",
        },
    )


@dataclass
class Values:
    class Meta:
        name = "values"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    start: float | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    increment: float | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    npts: int | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    separator: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    from_attribute: str | None = field(
        default=None,
        metadata={
            "name": "fromAttribute",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class Attribute:
    class Meta:
        name = "attribute"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    type: DataType = field(
        default=DataType.STRING,
        metadata={
            "type": "Attribute",
        },
    )
    value: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    separator: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    org_name: str | None = field(
        default=None,
        metadata={
            "name": "orgName",
            "type": "Attribute",
        },
    )
    is_unsigned: bool | None = field(
        default=None,
        metadata={
            "name": "isUnsigned",
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class EnumTypedef:
    class Meta:
        name = "enumTypedef"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    type: DataType = field(
        default=DataType.ENUM1,
        metadata={
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "enum",
                    "type": Type["EnumTypedef.EnumType"],
                },
            ),
        },
    )

    @dataclass
    class EnumType:
        key: int | None = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
        content: list[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
                "mixed": True,
            },
        )


@dataclass
class Remove:
    class Meta:
        name = "remove"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    type: ObjectType | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Variable:
    class Meta:
        name = "variable"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    attribute: list[Attribute] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    values: Values | None = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    variable: list[Variable] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    logical_section: LogicalSection | None = field(
        default=None,
        metadata={
            "name": "logicalSection",
            "type": "Element",
        },
    )
    logical_slice: LogicalSlice | None = field(
        default=None,
        metadata={
            "name": "logicalSlice",
            "type": "Element",
        },
    )
    logical_reduce: LogicalReduce | None = field(
        default=None,
        metadata={
            "name": "logicalReduce",
            "type": "Element",
        },
    )
    remove: list[Remove] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    type: DataType | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    typedef: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shape: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    org_name: str | None = field(
        default=None,
        metadata={
            "name": "orgName",
            "type": "Attribute",
        },
    )


@dataclass
class Group:
    class Meta:
        name = "group"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    choice: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "enumTypedef",
                    "type": EnumTypedef,
                },
                {
                    "name": "dimension",
                    "type": Dimension,
                },
                {
                    "name": "variable",
                    "type": Variable,
                },
                {
                    "name": "attribute",
                    "type": Attribute,
                },
                {
                    "name": "group",
                    "type": Type["Group"],
                },
                {
                    "name": "remove",
                    "type": Remove,
                },
            ),
        },
    )
    name: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    org_name: str | None = field(
        default=None,
        metadata={
            "name": "orgName",
            "type": "Attribute",
        },
    )


@dataclass
class Aggregation:
    class Meta:
        name = "aggregation"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    choice: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "group",
                    "type": Group,
                },
                {
                    "name": "dimension",
                    "type": Dimension,
                },
                {
                    "name": "variable",
                    "type": Variable,
                },
                {
                    "name": "attribute",
                    "type": Attribute,
                },
                {
                    "name": "remove",
                    "type": Remove,
                },
            ),
        },
    )
    variable_agg: list[Aggregation.VariableAgg] = field(
        default_factory=list,
        metadata={
            "name": "variableAgg",
            "type": "Element",
        },
    )
    promote_global_attribute: list[PromoteGlobalAttribute] = field(
        default_factory=list,
        metadata={
            "name": "promoteGlobalAttribute",
            "type": "Element",
        },
    )
    cache_variable: list[CacheVariable] = field(
        default_factory=list,
        metadata={
            "name": "cacheVariable",
            "type": "Element",
        },
    )
    netcdf: list[Netcdf] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    scan: list[Aggregation.Scan] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        },
    )
    scan_fmrc: list[Aggregation.ScanFmrc] = field(
        default_factory=list,
        metadata={
            "name": "scanFmrc",
            "type": "Element",
        },
    )
    type: AggregationType | None = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dim_name: str | None = field(
        default=None,
        metadata={
            "name": "dimName",
            "type": "Attribute",
        },
    )
    recheck_every: str | None = field(
        default=None,
        metadata={
            "name": "recheckEvery",
            "type": "Attribute",
        },
    )
    time_units_change: bool | None = field(
        default=None,
        metadata={
            "name": "timeUnitsChange",
            "type": "Attribute",
        },
    )
    fmrc_definition: str | None = field(
        default=None,
        metadata={
            "name": "fmrcDefinition",
            "type": "Attribute",
        },
    )

    @dataclass
    class VariableAgg:
        name: str | None = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass
    class Scan:
        location: str | None = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
        reg_exp: str | None = field(
            default=None,
            metadata={
                "name": "regExp",
                "type": "Attribute",
            },
        )
        suffix: str | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )
        subdirs: bool = field(
            default=True,
            metadata={
                "type": "Attribute",
            },
        )
        older_than: str | None = field(
            default=None,
            metadata={
                "name": "olderThan",
                "type": "Attribute",
            },
        )
        date_format_mark: str | None = field(
            default=None,
            metadata={
                "name": "dateFormatMark",
                "type": "Attribute",
            },
        )
        enhance: bool | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass
    class ScanFmrc:
        location: str | None = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
        reg_exp: str | None = field(
            default=None,
            metadata={
                "name": "regExp",
                "type": "Attribute",
            },
        )
        suffix: str | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )
        subdirs: bool = field(
            default=True,
            metadata={
                "type": "Attribute",
            },
        )
        older_than: str | None = field(
            default=None,
            metadata={
                "name": "olderThan",
                "type": "Attribute",
            },
        )
        run_date_matcher: str | None = field(
            default=None,
            metadata={
                "name": "runDateMatcher",
                "type": "Attribute",
            },
        )
        forecast_date_matcher: str | None = field(
            default=None,
            metadata={
                "name": "forecastDateMatcher",
                "type": "Attribute",
            },
        )
        forecast_offset_matcher: str | None = field(
            default=None,
            metadata={
                "name": "forecastOffsetMatcher",
                "type": "Attribute",
            },
        )


@dataclass
class Netcdf:
    class Meta:
        name = "netcdf"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    read_metadata: object | None = field(
        default=None,
        metadata={
            "name": "readMetadata",
            "type": "Element",
        },
    )
    explicit: object | None = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    iosp_param: object | None = field(
        default=None,
        metadata={
            "name": "iospParam",
            "type": "Element",
        },
    )
    choice: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "enumTypedef",
                    "type": EnumTypedef,
                },
                {
                    "name": "group",
                    "type": Group,
                },
                {
                    "name": "dimension",
                    "type": Dimension,
                },
                {
                    "name": "variable",
                    "type": Variable,
                },
                {
                    "name": "attribute",
                    "type": Attribute,
                },
                {
                    "name": "remove",
                    "type": Remove,
                },
                {
                    "name": "aggregation",
                    "type": Aggregation,
                },
            ),
        },
    )
    location: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    title: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    enhance: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    add_records: bool | None = field(
        default=None,
        metadata={
            "name": "addRecords",
            "type": "Attribute",
        },
    )
    iosp: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    iosp_param_attribute: str | None = field(
        default=None,
        metadata={
            "name": "iospParam",
            "type": "Attribute",
        },
    )
    buffer_size: int | None = field(
        default=None,
        metadata={
            "name": "bufferSize",
            "type": "Attribute",
        },
    )
    ncoords: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    coord_value: str | None = field(
        default=None,
        metadata={
            "name": "coordValue",
            "type": "Attribute",
        },
    )
    section: str | None = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
