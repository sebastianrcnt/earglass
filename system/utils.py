import os
import pandas as pd
import services
from settings import UPLOAD_DIR

def encoding(file):
    filename = os.path.join(UPLOAD_DIR + "/odsf/", file)

    try:
        df = pd.read_csv(filename)
        df.to_csv(filename, encoding='utf-8', index=False)
        return True
    except:
        pass

    try:
        df = pd.read_csv(filename, encoding='euc-kr')
        df.to_csv(filename, encoding='utf-8', index=False)
        return True
    except:
        pass

    try:
        df = pd.read_csv(filename, encoding='cp949')
        df.to_csv(filename, encoding='utf-8', index=False)
        return True
    except:
        pass

    return False


def read_odsf_to_df(file):
    filename = os.path.join(UPLOAD_DIR + "/odsf/", file)
    try:
        # read odsf file
        df = pd.read_csv(filename, encoding='utf-8')
    except:
        df = pd.DataFrame()
    
    return df

def save_df(type, file, df):
    try:
        filename = os.path.join(UPLOAD_DIR + f"/{type}/", file)
        df.to_csv(filename, index=False, encoding='utf-8')
        return True
    except:
        return False

def add_pdsf_to_taskdata(task_name, user_id, pdsf_id):

    # task data table dataframe
    task_data_table_file = services.estimator.task_detail(task_name)["TaskDataTableName"]
    task_data_df = pd.read_csv(task_data_table_file, encoding='utf-8')

    # pdsf dataframe
    pdsf_filename = services.estimator.pdsf_file_info(pdsf_id)["ParsingFile"]
    pdsf_df = pd.read_csv(pdsf_filename, encoding='utf-8')

    # name column
    series = {"submitter_name" : [user_id]*(pdsf_df.shape[0]),}
    df_name = pd.DataFrame(data=series)

    # concat pdsf, name
    pdsf_df = pd.concat([pdsf_df, df_name], axis=1)

    # concat task data table, pdsf
    task_data_df = pd.concat([task_data_df, pdsf_df], axis=0)
    
    # save table data
    file = task_data_table_file.split("/")[-1]
    save_df("table_data", file, task_data_df)

