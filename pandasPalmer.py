import pandas as pd
import os.path as path
# try:
#     from urllib.parse import urlparse
#     from urllib.request import request
# except ImportError:
#     try:
#         from urlparse import urlparse
#         from urlrequest import request
#     except ImportError:
#         print('Sorry ran out of options')

import urllib.parse as urlparse
import urllib.request as request

def import_func(file_or_url):
    # Locate the text at the last period '.'
    _, extn = path.splitext(file_or_url)
    extn_fns = {  '.csv':pd.read_csv
                , '.xls':pd.read_excel
                , '.xlsx':pd.read_excel
                , '.json':pd.read_json
                , '.html':pd.read_html
            }
    return extn_fns[extn]
def is_valid_url(url):
    rslt = urlparse.urlparse(url)
    is_url = all([rslt.scheme, rslt.netloc, rslt.path])
    
    is_url_valid = False
    
    if is_url:
        try:
            with request.urlopen(url) as resp:
                is_url_valid = (resp.status == 200)
        except Exception as exn:
            is_url_valid = False
            print(f'There was an error {exn}')
        else:
            is_url_valid = True
            
    return is_url_valid
def apply_index(df, idx=None):
    right_type = type(idx) == list or type(idx) == str
    idx_in_df = set(idx).issubset(set(df))

    if right_type and idx_in_df:
        df.set_index(keys=idx,inplace=True)
    else:
        # TODO: Fix this later, check if the index already exists
        #print(f"Index not applied {idx} [Type {right_type}] [Subset {idx_in_df}]")
        pass

    return df

def CreateDataFrame(file_name, idx=None, remove_nulls=True):
    file_name = file_name.strip()
    state = []

    apply_func = import_func(file_name)
    if is_valid_url(file_name):
        state.append('Valid url')
    else:
        if not path.exists(file_name):
            print(f'Had problems locating the data [{file_name}]')
            return pd.DataFrame()

    # Import File based on file extension
    df = apply_func(file_name, index_col=idx, parse_dates=True, infer_datetime_format=True)
    state.append('imported')

    # TODO: Index already applied
    #if idx is not None:
    #    df = apply_index(df, idx=idx)

    if remove_nulls:
        df.dropna(inplace=True)

    print(state)

    return df

from datetime import datetime
def Get_Qtr(xdate:datetime):
    """ This function takes various datetime objects and returns the Quarter associated with the values passed in
        So for an array, it will return an array of quarters as string.  If a single value was passed the
        a single quarter will be returned."""

    import numpy as np
    typ = type(xdate)
    if typ is datetime or typ is datetime.date:
        q = (xdate.month+2)//3
        y = xdate.year
        return (f"{y}Q{q}")
    elif typ is np.ndarray:
        lst_date = [Get_Qtr(x) for x in xdate]
        return lst_date
    elif typ is pd.Series or typ is list:
        lst_date = [Get_Qtr(x[1]) for x in xdate.iteritems()]
        return lst_date
    elif typ is pd.core.indexes.multi.MultiIndex:
        lst_date = [Get_Qtr(x[1].date()) for x in xdate.values]
        return lst_date
    elif typ is pd.core.indexes.datetimes.DatetimeIndex:
        lst_date = [Get_Qtr(x.date()) for x in xdate]
        return lst_date
    elif typ is str:
        return Get_Qtr(datetime.strptime(xdate, '%Y-%m-%d'))
    else:
        #print(f'The type is {type(xdate)} not planned for.')
        d = xdate
        q = (d.month+2)//3
        y = d.year
        return (f"{y}Q{q}")
def Get_Date(xdate:datetime):
    """ This function takes various datetime objects and returns the Date associated with the values passed in.
        So for an array, it will return an array of datetime dates.  If a single value was passed the
        a single date will be returned."""
    if xdate is None:
        return None

    print(f'{xdate.mro}')
    
    import numpy as np
    import pandas as pd

    typ = type(xdate)
    if typ is datetime or typ is datetime.date:
        return datetime(xdate.year,xdate.month,xdate.day)
    elif (typ is np.ndarray):
        lst_date = [Get_Date(x) for x in xdate]
        return lst_date
    elif (typ is pd._libs.tslibs.timestamps.Timestamp):
        print('pd._libs.tslibs.timestamps.Timestamp')
        return [Get_Date(x) for x in xdate]
    elif typ is pd.Series or typ is list:
        lst_date = [Get_Date(x[1]) for x in xdate.iteritems()]
        return lst_date
    elif typ is pd.core.indexes.multi.MultiIndex:
        lst_date = [Get_Date(x[1].date()) for x in xdate.values]
        return lst_date
    elif typ is pd.core.indexes.datetimes.DatetimeIndex:
        lst_date = [Get_Date(x.date()) for x in xdate]
        return lst_date
    elif typ is str:
        return datetime.strptime(xdate, '%Y-%m-%d')
    else:
        print(type(xdate))
        print(f'{xdate.mro}')
        return xdate
        #return datetime(xdate.year, xdate.month, xdate.day)
Linker = lambda sym,dtx: f"{sym}{Get_Date(dtx).strftime('%Y%m%d')}"


if __name__ == "__main__":
    # execute only if run as a script
    # if is_valid_url('https://www.youtube.com/watch?v=ucY6NwQTI3M&list=RDMMnQWFzMvCfLE&index=9'):
    #     print(urlparse.urlparse('https://www.youtube.com/watch?v=ucY6NwQTI3M&list=RDMMnQWFzMvCfLE&index=9'))
    #main()
    print(Get_Date())
    print(Get_Qtr('2012-12-2'),Get_Qtr(datetime(2012,12,2)),Get_Date('2019-10-30'),Linker('AAL','2012-11-20'))