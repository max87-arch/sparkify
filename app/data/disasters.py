import pandas as pd
from sqlalchemy import create_engine


def get_data(path_db='../data/DisasterResponse.db'):
    """
    The function returns the data
    :param path_db: path to db
    :return: DataFrame data
    """
    # load data
    engine = create_engine('sqlite:///' + path_db)
    df = pd.read_sql_table('message_with_categories', engine)
    return df
