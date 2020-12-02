import os
import json
import pandas as pd
import numpy as np
import math
from settings import UPLOAD_DIR
from .statistic import *
import services
from .utils import *


def validate_odsf_schema(file, odsf_type_id):
    """
    Check validate of file schema
    """
    odsf = read_odsf_to_df(file)
    
    file_schema = set(odsf.columns)
    odsf_type = services.submitter.odsf_type_schema_info(odsf_type_id)
    schema = json.loads(odsf_type['MappingInfo'])
    schema = set(schema.keys())

    if file_schema == schema:
        return True
    else:
        return False

def validate_odsf_data(file, MNR, MDR):
    """
    Check validate of odsf file's duplicate tuple
    input : filename is odsf, MaxNullRatioPerColumn, MaxDuplicatedRowRatio
    output : boolean
    """
    odsf = read_odsf_to_df(file)
    
    # statistic analysis
    null_info = null_count(odsf)
    duplicate_info = duplicate_tuple(odsf)
    
    # calculate null ratio
    for col, null in null_info.items():
        null_ratio = null / duplicate_info['total_tuple_num']
        if null_ratio > MNR/100:
            null_info[col] = False
        else:
            null_info[col] = True
    
    # calculate duplicate ratio
    if duplicate_info['duplicate_rate'] > MDR/100:
        null_info['duplicate_ratio'] = False
    else:
        null_info['duplicate_ratio'] = True
    
    return null_info