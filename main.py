import pandas as pd

from helpers import create_df, get_data_identifier_url


def get_transactions(identifier: str) -> pd.DataFrame:
    """
    create df with columns IDENTIFIER, TIME_PERIOD and OBS_VALUE,
    corresponding to values of the identifier parameter, generic:ObsDimension tag
    and generic:ObsValue tag from the XML.
    :param identifier: transaction identifier and can be replaced
                       with any other (valid) identifier.
    :return: fetch the transaction data from the appropriate URL
            and convert it to a pandas DataFrame,
    """
    url = get_data_identifier_url(identifier)
    df = create_df(url)
    construct = {"IDENTIFIER": identifier, "TIME_PERIOD": df['TIME_PERIOD'], "OBS_VALUE": df['OBS_VALUE']}
    res = pd.DataFrame(construct)
    return res


def get_symmetric_identifier(identifier: str, swap_components: dict[int, int]) -> str:
    """
    function is swapping appropriate components (e.g.
    source and target, import and export)
    :param identifier: A transaction identifier
    :param swap_components: dictionary with swapped components
    :return: function should return a new identifier, obtained from the provided one,
            by swapping components, as indicated by the key-value pairs
    """
    splitted = identifier.split('.')
    mystring = ""

    for key, value in swap_components.items():
        _key_holder = splitted[key]
        splitted[key] = splitted[value]
        splitted[value] = _key_holder

    # TODO: check later for some list comprehension method which stores string
    for y in splitted:
        mystring += y + "."

    return mystring[:-1]


def get_asymmetries(
                     identifier: str,
                     swap_components: dict[int, int]
                    ) -> pd.DataFrame:
    """
    determine the symmetric counterpart of the provided identifier using the function
    from part #2 and fetch data for both, using the function from part #1.
    :return: df with calculated DELTA: absolute difference between OBS_VALUE columns
            of the provided and symmetric identifier, for the same TIME_PERIOD
    """
    asim_df_url = get_symmetric_identifier(identifier, swap_components)

    ident_df = get_transactions(identifier)
    asime_df = get_transactions(asim_df_url)

    ident_df = ident_df.set_index(ident_df['TIME_PERIOD']).drop(columns=['TIME_PERIOD'])
    asime_df = asime_df.set_index(asime_df['TIME_PERIOD']).drop(columns=['TIME_PERIOD'])

    ident_df.rename(columns={'OBS_VALUE': 'IDENTIF_OBS_VALUE'}, inplace=True)
    asime_df.rename(columns={'OBS_VALUE': 'ASIMET_OBS_VALUE'}, inplace=True)

    result = pd.concat([ident_df, asime_df], axis=1)
    result.dropna(inplace=True)

    result['DELTA'] = abs(result['IDENTIF_OBS_VALUE'] - result['ASIMET_OBS_VALUE'])
    df_dict = {"PROVIDED_ID": identifier, 'SYMMETRIC_ID': asim_df_url, "DELTA": result['DELTA']}

    df = pd.DataFrame(df_dict)
    # df.to_csv('./output/final_second_part.csv', sep=',', index=True)  # -> for exporting file
    return df


if __name__ == "__main__":
    kiska = get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7})
    print(kiska)


"""        
TIME_PERIOD  PROVIDED_ID                          DELTA           
2013-Q3      Q.HR.N.A.A20.A.1.AT.2000.Z01.E  ...  8866.696900
2013-Q4      Q.HR.N.A.A20.A.1.AT.2000.Z01.E  ...  8875.099521
2014-Q1      Q.HR.N.A.A20.A.1.AT.2000.Z01.E  ...  9036.292579
2014-Q2      Q.HR.N.A.A20.A.1.AT.2000.Z01.E  ...  8809.512144
"""



# TODO: This option can be valid for list comprehensio but dont know if its more readable
# identifier = "Q.HR.N.A.A20.A.1.AT.2000.Z01.E"
# xa = ["".join(y) for y in identifier.split('.')]
# print(xa)
# print(".".join(xa))
