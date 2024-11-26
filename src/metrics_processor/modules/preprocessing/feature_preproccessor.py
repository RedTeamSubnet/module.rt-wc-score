# importing  neccessary libraries
## Standard libraries
from datetime import datetime
import math
## Third party libraries
import pandas as pd


def is_nan(feature_name, value):
    if value is None:
        # log_error(f'ignoring nan value in {feature_name}:{value}')
        return True
    if isinstance(value, float) and math.isnan(value):
        # log_error(f"ignored NaN value in {feature_name}:{value}")
        return True
    elif isinstance(value, pd.Series) and value.isna().any():
        # nan_indices = value.index[value.isna()]
        # for index in nan_indices:
        # log_error(f"NaN value found for feature '{feature_name}' at index '{index}'")
        return True
    # else:
    return False


class PreProccessData:
    """Class to precess data. Converts string json to json and etc...

    Attributes:
        df                (DataFrame, required): Pandas DataFrame to process data
        __datetime_format (str      , optional): Defaults "%Y-%m-%dT%H:%M:%S.%fZ". Data formate to convert data time objects

    Methods:
        parse (df: DataFrame): Main function which recieves data and delivers to other subfunctions to process it
    """
    _datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    def parse(self, df:pd.DataFrame) -> pd.DataFrame:
        """Function for receiving input dataFrame and delivering to other functions

        Attributes:
            df (DataFrame, required): Pandas DataFrame to process data

        Returns:
            pd.DataFrame: Processed Pandas DataFrame
        """
        print("Cleaning JSON object and flattening...")
        df = self.parse_datetime_values(df)

        return df

    def parse_datetime_values(self, df):
        """Function for receiving input dataFrame and delivering to other functions

        Attributes:
            df (DataFrame, required): Pandas DataFrame to process data

        Returns:
            pd.DataFrame: Processed Pandas DataFrame
        """
        # Apply the process_row function across all rows
        processed_data = df[
            [
                "ui_clicks",
                "ui_mouseMovements",
            ]
        ].apply(self.process_row, axis=1)

        # Convert the resulting Series of dictionaries to a DataFrame and join it with the original df
        processed_df = pd.DataFrame(processed_data.tolist(), index=df.index)
        df = df.join(processed_df)

        return df

    def process_row(self, row):
        return {
            "ui_clicks_list": self._mouse_data_parser(row["ui_clicks"]),
            "ui_mouseMovements_list": self._mouse_data_parser(row["ui_mouseMovements"]),
        }

    def _mouse_data_parser(self, mouse_data):
        if is_nan("mouse_data", mouse_data):
            return None

        return [self._coord_point_parser(clk) for clk in mouse_data]

    def _coord_point_parser(self, point):
        if is_nan("click_point", point):
            return None

        if not all(k in point for k in ("x", "y", "timestamp")):
            return None

        return {
            "x": point["x"],
            "y": point["y"],
            "timestamp": datetime.strptime(point["timestamp"], self._datetime_format),
        }
