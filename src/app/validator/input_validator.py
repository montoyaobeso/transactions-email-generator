from pandera import Column, DataFrameSchema, Check, Index
from pandera.engines import pandas_engine

schema = DataFrameSchema(
    {
        "Id": Column(
            int,
            Check(lambda x: x >= 0),
            nullable=False,
        ),
        "Date": Column(
            pandas_engine.DateTime(to_datetime_kwargs={"format": "%m/%d/%Y"}),
            nullable=False,
        ),
        "Transaction": Column(
            float,
            nullable=False,
        ),
    },
    strict=True,
    coerce=True,
)
