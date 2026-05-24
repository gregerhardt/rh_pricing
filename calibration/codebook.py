"""Helpers for applying the CMAP HTS codebook to pandas DataFrames.

The codebook ships as two CSVs in calibration/docs/:
  - value_labels.csv        (table, variable, value, label)
  - variable_description.csv (source, variable, table, description, data_type, logic)

Typical use:
    from codebook import Codebook
    cb = Codebook()
    person["transit_freq_f"] = cb.as_categorical(person["transit_freq"], "person", "transit_freq")
    cb.describe("person", "transit_freq")
"""

from pathlib import Path
import pandas as pd

_DEFAULT_DOCS = Path(__file__).parent / "docs"


class Codebook:
    def __init__(self, docs_dir: Path | str = _DEFAULT_DOCS):
        docs_dir = Path(docs_dir)
        self.value_labels = pd.read_csv(docs_dir / "value_labels.csv")
        self.variables = pd.read_csv(docs_dir / "variable_description.csv")

    def labels(self, table: str, variable: str) -> dict:
        """Return {value: label} for one variable in one table."""
        m = self.value_labels.query("table == @table and variable == @variable")
        return dict(zip(m["value"], m["label"]))

    def as_categorical(
        self, series: pd.Series, table: str, variable: str, ordered: bool = True
    ) -> pd.Categorical:
        """Pandas equivalent of R's factor() built from the codebook."""
        m = self.value_labels.query("table == @table and variable == @variable")
        if m.empty:
            raise KeyError(f"No value labels for {table}.{variable}")
        return pd.Categorical(
            series.map(dict(zip(m["value"], m["label"]))),
            categories=m["label"].tolist(),
            ordered=ordered,
        )

    def decode(self, series: pd.Series, table: str, variable: str) -> pd.Series:
        """Lightweight code -> label mapping (no ordering, no category dtype)."""
        return series.map(self.labels(table, variable))

    def describe(self, table: str, variable: str) -> dict:
        """Return the variable_description row as a dict (description, data_type, logic, ...)."""
        m = self.variables.query("table == @table and variable == @variable")
        if m.empty:
            raise KeyError(f"No description for {table}.{variable}")
        return m.iloc[0].to_dict()

    def variables_in(self, table: str) -> pd.DataFrame:
        """List all variables documented for a given table."""
        return self.variables.query("table == @table").reset_index(drop=True)
