import os
import json
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
        return filename
    except:
        return ""

def read_table_data_to_df(file):
    filename = os.path.join(UPLOAD_DIR + "/table_data/", file)
    try:
        # read table_data file
        df = pd.read_csv(filename, encoding='utf-8')
    except:
        df = pd.DataFrame()
    
    return df

def save_df(type, file, df):
    try:
        filename = os.path.join(UPLOAD_DIR + f"/{type}/", file)
        df.to_csv(filename, index=False, encoding='utf-8')
        return filename
    except:
        return ""

def add_pdsf_to_taskdata(task_name, user_id, pdsf_id, odt_id):

    pdsf = services.estimator.pdsf_file_info(pdsf_id)
    odsf_type_id = pdsf["FK_idORIGIN_DSF"]

    odsf_type = services.submitter.odsf_type_schema_info(odsf_type_id)
    schema_map = json.loads(odsf_type['MappingInfo'])
    task_data_schema = set(schema_map.keys())
    pdsf_data_schema = set(schema_map.values())
    schema_map["submitter_name"] = "submitter_name"
    schema_map["origin_type"] = "origin_type"

    cols = [schema_map[key] for key in schema_map.keys()]

    # pdsf dataframe
    pdsf_filename = services.estimator.pdsf_file_info(pdsf_id)["ParsingFile"]
    pdsf_df = pd.read_csv(pdsf_filename, columns, encoding='utf-8')
    pdsf_df = pdsf_df[cols]

    # name column
    series1 = {"submitter_name" : [user_id]*(pdsf_df.shape[0]),}
    df_name = pd.DataFrame(data=series1)

    series2 = {"origin_type" : [odsf_type_id]*(pdsf_df.shape[0]),}
    df_odt = pd.DataFrame(data=series2)

    # task data table dataframe
    task_data_table_file = services.estimator.task_detail(task_name)["TaskDataTableName"]
    task_data_df = pd.read_csv(task_data_table_file, encoding='utf-8')

    # concat pdsf, name
    pdsf_df = pd.concat([pdsf_df, df_name, df_odt], axis=1)

    # concat task data table, pdsf
    task_data_df = pd.concat([task_data_df, pdsf_df], axis=0)
    
    # save table data
    file = task_data_table_file.split("/")[-1]
    filename = save_df("table_data", file, task_data_df)

    return filename

def count_total_row(task_name, user_id):

    file = f"{task_name}_data_table.csv"
    df = read_table_data_to_df(file)
    num = df[df["submitter_name"] == user_id].shape[0]

    return num 

def count_row_by_origin_type(task_name, odt_list):

    file = f"{task_name}_data_table.csv"
    df = read_table_data_to_df(file)

    count_odt = {"total" : df.shape[0]}
    for odt in odt_list:
        num = df[df["origin_type"] == odt].shape[0]
        count_odt[odt] = num

    return count_odt