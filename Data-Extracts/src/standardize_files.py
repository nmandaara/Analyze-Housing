"""
This program will loop through the files that are downloaded from Zillow and 
converts columns to rows. 
"""
import os
import glob
import pandas as pd

src_files = os.path.realpath(__file__).rsplit("\\", 2)[0]+"\\resources\\*.csv"

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
