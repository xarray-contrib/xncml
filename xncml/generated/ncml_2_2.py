from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Type


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

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Dimension:
    class Meta:
        name = "dimension"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    length: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    is_unlimited: bool = field(
        default=False,
        metadata={
            "name": "isUnlimited",
            "type": "Attribute",
        }
    )
    is_variable_length: bool = field(
        default=False,
        metadata={
            "name": "isVariableLength",
            "type": "Attribute",
        }
    )
    is_shared: bool = field(
        default=True,
        metadata={
            "name": "isShared",
            "type": "Attribute",
        }
    )
    org_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "orgName",
            "type": "Attribute",
        }
    )


@dataclass
class LogicalReduce:
    class Meta:
        name = "logicalReduce"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    dim_names: Optional[str] = field(
        default=None,
        metadata={
            "name": "dimNames",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class LogicalSection:
    class Meta:
        name = "logicalSection"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    section: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class LogicalSlice:
    class Meta:
        name = "logicalSlice"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    dim_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "dimName",
            "type": "Attribute",
            "required": True,
        }
    )
    index: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class PromoteGlobalAttribute:
    class Meta:
        name = "promoteGlobalAttribute"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    org_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "orgName",
            "type": "Attribute",
        }
    )


@dataclass
class Values:
    class Meta:
        name = "values"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    start: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    increment: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    npts: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    separator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    from_attribute: Optional[str] = field(
        default=None,
        metadata={
            "name": "fromAttribute",
            "type": "Attribute",
        }
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )


@dataclass
class Attribute:
    class Meta:
        name = "attribute"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    type: DataType = field(
        default=DataType.STRING,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    separator: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    org_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "orgName",
            "type": "Attribute",
        }
    )
    is_unsigned: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isUnsigned",
            "type": "Attribute",
        }
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )


@dataclass
class EnumTypedef:
    class Meta:
        name = "enumTypedef"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    enum: List["EnumTypedef.EnumType"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    type: DataType = field(
        default=DataType.ENUM1,
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass
    class EnumType:
        key: Optional[int] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        content: List[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
                "mixed": True,
            }
        )


@dataclass
class Remove:
    class Meta:
        name = "remove"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    type: Optional[ObjectType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Variable:
    class Meta:
        name = "variable"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    attribute: List[Attribute] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    values: Optional[Values] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    variable: List["Variable"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    logical_section: Optional[LogicalSection] = field(
        default=None,
        metadata={
            "name": "logicalSection",
            "type": "Element",
        }
    )
    logical_slice: Optional[LogicalSlice] = field(
        default=None,
        metadata={
            "name": "logicalSlice",
            "type": "Element",
        }
    )
    logical_reduce: Optional[LogicalReduce] = field(
        default=None,
        metadata={
            "name": "logicalReduce",
            "type": "Element",
        }
    )
    remove: List[Remove] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    type: Optional[DataType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    typedef: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    shape: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    org_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "orgName",
            "type": "Attribute",
        }
    )


@dataclass
class Group:
    class Meta:
        name = "group"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    choice: List[object] = field(
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
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    org_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "orgName",
            "type": "Attribute",
        }
    )


@dataclass
class Aggregation:
    class Meta:
        name = "aggregation"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    choice: List[object] = field(
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
        }
    )
    variable_agg: List["Aggregation.VariableAgg"] = field(
        default_factory=list,
        metadata={
            "name": "variableAgg",
            "type": "Element",
        }
    )
    promote_global_attribute: List[PromoteGlobalAttribute] = field(
        default_factory=list,
        metadata={
            "name": "promoteGlobalAttribute",
            "type": "Element",
        }
    )
    cache_variable: List[CacheVariable] = field(
        default_factory=list,
        metadata={
            "name": "cacheVariable",
            "type": "Element",
        }
    )
    netcdf: List["Netcdf"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    scan: List["Aggregation.Scan"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    scan_fmrc: List["Aggregation.ScanFmrc"] = field(
        default_factory=list,
        metadata={
            "name": "scanFmrc",
            "type": "Element",
        }
    )
    type: Optional[AggregationType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    dim_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "dimName",
            "type": "Attribute",
        }
    )
    recheck_every: Optional[str] = field(
        default=None,
        metadata={
            "name": "recheckEvery",
            "type": "Attribute",
        }
    )
    time_units_change: Optional[bool] = field(
        default=None,
        metadata={
            "name": "timeUnitsChange",
            "type": "Attribute",
        }
    )
    fmrc_definition: Optional[str] = field(
        default=None,
        metadata={
            "name": "fmrcDefinition",
            "type": "Attribute",
        }
    )

    @dataclass
    class VariableAgg:
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )

    @dataclass
    class Scan:
        location: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        reg_exp: Optional[str] = field(
            default=None,
            metadata={
                "name": "regExp",
                "type": "Attribute",
            }
        )
        suffix: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        subdirs: bool = field(
            default=True,
            metadata={
                "type": "Attribute",
            }
        )
        older_than: Optional[str] = field(
            default=None,
            metadata={
                "name": "olderThan",
                "type": "Attribute",
            }
        )
        date_format_mark: Optional[str] = field(
            default=None,
            metadata={
                "name": "dateFormatMark",
                "type": "Attribute",
            }
        )
        enhance: Optional[bool] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )

    @dataclass
    class ScanFmrc:
        location: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        reg_exp: Optional[str] = field(
            default=None,
            metadata={
                "name": "regExp",
                "type": "Attribute",
            }
        )
        suffix: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        subdirs: bool = field(
            default=True,
            metadata={
                "type": "Attribute",
            }
        )
        older_than: Optional[str] = field(
            default=None,
            metadata={
                "name": "olderThan",
                "type": "Attribute",
            }
        )
        run_date_matcher: Optional[str] = field(
            default=None,
            metadata={
                "name": "runDateMatcher",
                "type": "Attribute",
            }
        )
        forecast_date_matcher: Optional[str] = field(
            default=None,
            metadata={
                "name": "forecastDateMatcher",
                "type": "Attribute",
            }
        )
        forecast_offset_matcher: Optional[str] = field(
            default=None,
            metadata={
                "name": "forecastOffsetMatcher",
                "type": "Attribute",
            }
        )


@dataclass
class Netcdf:
    class Meta:
        name = "netcdf"
        namespace = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"

    read_metadata: Optional[object] = field(
        default=None,
        metadata={
            "name": "readMetadata",
            "type": "Element",
        }
    )
    explicit: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    iosp_param: Optional[object] = field(
        default=None,
        metadata={
            "name": "iospParam",
            "type": "Element",
        }
    )
    choice: List[object] = field(
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
        }
    )
    location: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    enhance: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    add_records: Optional[bool] = field(
        default=None,
        metadata={
            "name": "addRecords",
            "type": "Attribute",
        }
    )
    iosp: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    iosp_param_attribute: Optional[str] = field(
        default=None,
        metadata={
            "name": "iospParam",
            "type": "Attribute",
        }
    )
    buffer_size: Optional[int] = field(
        default=None,
        metadata={
            "name": "bufferSize",
            "type": "Attribute",
        }
    )
    ncoords: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    coord_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "coordValue",
            "type": "Attribute",
        }
    )
    section: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
