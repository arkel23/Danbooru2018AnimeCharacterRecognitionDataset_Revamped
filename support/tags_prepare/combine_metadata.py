import os
import argparse
import pandas as pd

def make_data_dic(df, version, year=2020):
    '''Saves three df:
    1. With all metadata extracted in previous step
    2. With all the needed information (id, path, and tags)
    2. With minimal information
    to connect all other df: id, path to image,
    and csv file with metadata'''

    df_full = df
    df_full.to_csv('db{}_metadata_condensed_v{}.csv'.format(year, version), index=False, header=True)

    df_needed = df[['id', 'path_img', 'tags_cat0', 'tags_cat3', 'tags_cat4']]
    df_needed.to_csv('db{}_metadata_essential_v{}.csv'.format(year, version), index=False, header=True)

    df_minimal = df[['id', 'path_img', 'path_metadata']]
    df_minimal.to_csv('db{}_filelist_v{}.csv'.format(year, version), index=False, header=True)


def read_single(file_name):
    '''Reads single df,
    adds paths to img and metadata,
    then checks images can be opened and are RGB'''

    df = pd.read_csv(file_name)
    
    print('{}\nPre-filtering: {}'.format(file_name, len(df)))
    
    df['path_img'] = ['0{}/{}.jpg'.format(
    x.strip()[-3:], x) 
    for x in df['id'].astype(str)] #+ df['file_ext']
    df['path_metadata'] = file_name
    
    return df

def main():
    '''returns all files in a given dir then process each'''
    
        
    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata_organized_path', required=True, 
    help='''Path where to look for organized metadata files. 
    Should contain metadata .csv files after passing through organize_metadata_raw.py''')
    parser.add_argument('--year', default=2020, type=int, 
    help='Year of metadata files. Default=2020 (2018 for DAF:re')
    args = parser.parse_args()

    mypath = args.metadata_organized_path
    files = [os.path.join(mypath, f) for f in os.listdir(
        mypath) if f.endswith('.csv')]
    
    df_list = []

    for f in files:
        df_list.append(read_single(f))
    
    df = pd.concat(df_list)
    make_data_dic(df, version=1, year=args.year)
    
if __name__ == '__main__':
    main()
