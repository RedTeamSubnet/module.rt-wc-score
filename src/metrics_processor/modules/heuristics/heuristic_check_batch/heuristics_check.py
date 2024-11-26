import logging
import pandas as pd
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)


class HeuristicsCheck(ABC):
    _count_threshold = 0
    _all_heuristic_columns = []

    def __init__(self) -> None:
        super().__init__()

    def check(self, column: pd.Series, mask: pd.Series = None) -> pd.DataFrame:
        """
        Perform a heuristic check on the given column of data.

        Parameters:
        - column (pd.Series): The data column on which to perform the heuristic check.
        - mask (pd.Series, optional): A boolean mask indicating the subset of the data to check.

        Returns:
        - pd.DataFrame: A DataFrame containing the results of the heuristic check.
        """
        result = pd.DataFrame(index=column.index,
                              columns=self._all_heuristic_columns)

        if mask is not None:
            target_subset = column[mask]
            non_target_subset = column[~mask]

            result.loc[mask] = self._check_target_subset(
                target_subset)

            result.loc[~mask] = self._check_non_target_subset(
                non_target_subset, self._all_heuristic_columns)

            result = result.astype(bool)

        else:
            result = self._check_target_subset(column).astype(bool)

        return result

    @abstractmethod
    def _check_target_subset(self, target_subset: pd.Series) -> pd.DataFrame:
        """ Perform the heuristic check on the target subset of the data. """
        pass

    def _check_non_target_subset(self, non_target_subset: pd.Series, columns: list[str]) -> pd.DataFrame:
        """
        Set default False values for the given columns in the non-target subset.

        Parameters:
        - non_target_subset (pd.Series): The data column for the non-target subset.
        - columns (List[str]): The list of column names to set to False by default.

        Returns:
        - pd.DataFrame: A DataFrame with the specified columns set to False.
        """
        if columns and len(columns) > 0:
            return pd.DataFrame(False, index=non_target_subset.index, columns=columns)

        return non_target_subset
