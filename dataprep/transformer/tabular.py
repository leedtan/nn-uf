
from .base import Transformer
import pandas as PD


def _to_numeric(column):
    return PD.to_numeric(column, errors='coerce')


def _to_categorical(column):
    return column.astype(str)


_column_types = {
        "numeric": _to_numeric,
        "categorical": _to_categorical,
        }


def _check_types(schema_values):
    for t in schema_values:
        if t not in _column_types:
            raise ValueError('unknown column type %s' % t)


class TabularSchemaTransformer(Transformer):
    '''
    Transforms a tabular dataset according to given schema.

    For each column, if the column type given in the schema is "numeric",
    TabularSchemaTransformer would try converting the values there into
    real numbers, replacing those "invalid" values by NaNs.  If the
    column type is "categorical", the transformer would convert values
    there into strings, and treat each distinct string as a category.

    If the schema is given as a dict, the transformer will transform
    all the columns whose names are given, leaving other columns
    untouched.

    If the schema is given as a list, the number of elements in the
    schema should match the number of columns in the dataset, or an
    ValueError would be thrown otherwise.

    Parameters
    ----------
    schema : list of str, or dict of (str, str)
        Specifies the type of each column via a list of string, each
        element of which can be either "numeric" or "categorical".
    '''

    def __init__(self, schema):
        # Throws ValueError if the schema is not in correct format
        if isinstance(schema, dict):
            _check_types(schema.values())
        else:
            _check_types(schema)

        self._schema = schema

    def _transform(self, dataset):
        if isinstance(self._schema, dict):
            pairs = self._schema.items()
        else:
            if len(dataset.columns) != len(self._schema):
                raise ValueError(
                        'number of columns does not match that of schema'
                        )
            pairs = zip(dataset.columns, self._schema)
        for c, t in pairs:
            op = _column_types[t]
            dataset[c] = op(dataset[c])
        return dataset