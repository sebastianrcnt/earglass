import os
import pandas as pd
import numpy as np
import math
from settings import UPLOAD_DIR
from .utils import *


def null_count(df):
    total_row = len(df.index)
    col_null = dict()
    for col in df.columns:
        col_null[col] = total_row - df[col].count()
    return col_null

def duplicate_tuple(df):
    total_tuple_num = len(df.index)
    tmp = set()
    for k in range(df.shape[0]):
        tmp.add(tuple(df.iloc[k,:]))
    isol_tuple_num = len(tmp)
    duplicate_rate = 1 - (isol_tuple_num / total_tuple_num)
    duplicate = {"total_tuple_num": total_tuple_num,"duplicate_num":total_tuple_num - isol_tuple_num, "duplicate_rate":duplicate_rate}
    return duplicate

def system_score(file):
    """
    calculate system score of given file.
    input : filename is odsf
    output : system score
    """
    odsf = read_odsf_to_df(file)
    
    score_info = dict()
    # statistic analysis
    null_info = null_count(odsf)
    duplicate_info = duplicate_tuple(odsf)
      
    score_info['total_tuple_score'] = math.log2(duplicate_info['total_tuple_num'])*(7.5)*(30/100)
    score_info['duplicate_tuple_score'] = (1 - duplicate_info['duplicate_rate'])*(30)
    
    null_score_list = []
    for col in null_info.keys():
        tmp = 1 - (null_info[col] / duplicate_info['total_tuple_num'])
        null_score_list.append(tmp)
    
    score_info['col_null_score'] = (sum(null_score_list)/len(null_score_list))*(40)
    
    score_info['sys_score'] = score_info['total_tuple_score'] + score_info['duplicate_tuple_score'] + score_info['col_null_score']
    
    return score_info
