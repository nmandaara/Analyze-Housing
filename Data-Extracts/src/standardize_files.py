"""
This program will loop through the files that are downloaded from Zillow and 
converts columns to rows. 
"""
import os
import glob
import logging
import pandas as pd

log = logging.getLogger(__name__)

def process_files():
    """
    Method to process the files and generate new target files
    """
    try:
        src_files = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','resources','*.csv'))
        for fname in glob.glob(src_files):
            id_variables = ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName"]
            if "growth" in fname:
                id_variables = ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName", "BaseDate"]
            df = pd.read_csv(fname)
            new_df = pd.melt(df, id_vars = id_variables,
                                var_name= "EOM_Date",
                                value_name = "Value")
            new_fname = fname[:-4]+"_TGT.csv"
            new_df.to_csv(new_fname, index=False)
    except FileNotFoundError as err:
        log.error(err)
        print(f"File/Folder not found {err}")
    except KeyError as  err:
        log.error(err)
        print(f"Column not found: {err}")
