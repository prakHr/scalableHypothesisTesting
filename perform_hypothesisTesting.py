import medstat
import pandas as pd
from pprint import pprint
import multiprocessing
from mpire import WorkerPool
from pprint import pprint

def get_hypothesis_test_from_csv_file(df,name,list_of_columns):
    result = []
    for name2 in list_of_columns:
        var = medstat.test_hypothesis(df,name,name2)
        result.append(var)
    return {"name":name,"list_of_columns":list_of_columns,"result":result}

def get_hypothesis_tests_from_csv_file(csv_file_path,progress_bar):
    df = pd.read_csv(csv_file_path)
    list_of_columns = list(df.columns)
    results = []
    for name in list_of_columns:
        my_dict = {
            "df":df,
            "name":name,
            "list_of_columns":list_of_columns
        }
        results.append(my_dict)
    num_cores = max(multiprocessing.cpu_count()//2,1)
    with WorkerPool(n_jobs=num_cores,daemon=False) as pool:
        results = pool.map(get_hypothesis_test_from_csv_file, results,
progress_bar = progress_bar)
    return results

if __name__=="__main__":
    csv_file_path = r"C:\Users\gprak\anaconda3\envs\py310\Lib\site-packages\pymatgen\analysis\hhi_data.csv"
    progress_bar = True
    rv = get_hypothesis_tests_from_csv_file(csv_file_path,progress_bar)
    # pprint(rv)
    # pprint(len(rv))

