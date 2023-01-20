import pandas as pd

from helpers import create_df, get_data_identifier_url


def get_transactions(identifier: str) -> pd.DataFrame:
    """

    :param identifier:
    :return:
    """
    url = get_data_identifier_url(identifier)
    df = create_df(url)
    construct = {"IDENTIFIER": identifier, "TIME_PERIOD": df['TIME_PERIOD'], "OBS_VALUE": df['OBS_VALUE']}
    res = pd.DataFrame(construct)
    return res


def get_symmetric_identifier(identifier: str, swap_components: dict[int, int]) -> str:

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

    :param identifier:
    :param swap_components:
    :return:
    """
    asim_df_url = get_symmetric_identifier(identifier, swap_components)

    iden_df = get_transactions(identifier)
    asim_df = get_transactions(asim_df_url)

    iden_df = iden_df.set_index(iden_df['TIME_PERIOD']).drop(columns=['TIME_PERIOD'])
    asim_df = asim_df.set_index(asim_df['TIME_PERIOD']).drop(columns=['TIME_PERIOD'])

    iden_df.rename(columns={'OBS_VALUE': 'IDENTIFIC_OBS_VALUE'}, inplace=True)
    asim_df.rename(columns={'OBS_VALUE': 'ASIM_OBS_VALUE'}, inplace=True)

    result = pd.concat([iden_df, asim_df], axis=1)
    result.dropna(inplace=True)

    result['DELTA'] = abs(result['IDENTIFIC_OBS_VALUE'] - result['ASIM_OBS_VALUE'])
    df_dict = {"PROVIDED_ID": identifier, 'SYMMETRIC_ID': asim_df_url, "DELTA": result['DELTA']}

    df = pd.DataFrame(df_dict)
    # df.to_csv('./output/final_second_part.csv', sep=',', index=True)  # -> for exporting file
    return df


kiska = get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7})
print(kiska)




# TODO: This option can be valid for list comprehensio but dont know if its more readable
# identifier = "Q.HR.N.A.A20.A.1.AT.2000.Z01.E"
# xa = ["".join(y) for y in identifier.split('.')]
# print(xa)
# print(".".join(xa))
