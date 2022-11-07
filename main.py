"""This module contains tools to produce a fake pandas dataframe from an existing one."""

import random
import io

import pandas as pd
from pandas.testing import assert_frame_equal
from pandas.api.types import is_string_dtype


def assert_frame_not_equal(*args, **kwargs):
    """inverse of pandas.testing.assert_frame_equal(..)"""
    try:
        assert_frame_equal(*args, **kwargs)
    except AssertionError:
        # frames are not equal
        pass
    else:
        # frames are equal
        raise AssertionError


def munge_string(input_str: str, as_noun=False) -> str:
    """returns a randomly shuffled version of an input string, optionally capitalizing it"""
    _x = input_str.lower()
    # split the string into a list of chars
    _x = [*_x]

    random.shuffle(_x)
    if as_noun:
        _x[0] = _x[0].upper()

    # return a string
    return "".join(_x)


def shuffle_dataframe(
    original_df: pd.DataFrame, munge: bool = True, as_noun: bool = True
) -> pd.DataFrame:
    """returns a shuffled copy of the original dataframe, optionally munging strings"""
    shuffled_df = original_df.copy()
    for col in shuffled_df.columns:
        shuffled_df[col] = shuffled_df[col].sample(frac=1).values
        if munge and is_string_dtype(shuffled_df[col]):
            shuffled_df[col] = shuffled_df[col].apply(munge_string, as_noun=as_noun)

    return shuffled_df


if __name__ == "__main__":
    # include data in sample code for simplicity
    csv_data = io.StringIO(
        """
    Cust_ID,First_Name,Surname
    108,"Roger","Pearson"
    102,"Sheila","Jenkins"
    117,"Helen","Lin"
    104,"Peter","O'Malley"
    122,"Lee","Robbins"
    114,"Janice","Burr"
    109,"Franklin","Cross"
    121,"Miriam","Garner"
    """
    )

    # read the csv data from above
    customers_df = pd.read_csv(csv_data, index_col=False)
    print("original df")
    print(customers_df)
    fake_df = shuffle_dataframe(customers_df, munge=False)
    print("fake df")
    print(fake_df)

    # prove that the dataframes are different
    assert_frame_not_equal(customers_df, fake_df)
    # prove that the dataframes are statistically identical
    assert_frame_equal(customers_df.describe(), fake_df.describe())
