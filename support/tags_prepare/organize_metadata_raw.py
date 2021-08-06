import os
import argparse
import pandas as pd

def read_organize_save(file_name):
    '''reads_df and only keeps relevant columns
    then filters by boolean metadata and separates tags
    by categories, then saves into csv'''

    col_names = ['id', 'image_width', 'image_height', 'file_ext', 
    'is_pending', 'is_flagged', 'is_deleted', 'is_banned', 'rating',
    'tags']
    df = pd.read_json(file_name, lines=True)[col_names]
    
    df = filter_tags(df)
    df.to_csv('{}.csv'.format(file_name), 
    index=False, header=True)

    return df

def filter_tags(df):
    '''Filters tags to only keep:
    category 0: description
    category 3: series/origin
    category 4: character names/series'''

    df['tags_cat0'] = [[tag['name'] for tag in tag_iter if (
        tag['category']=='0')] for tag_iter in df['tags']]
    df['tags_cat3'] = [[tag['name'] for tag in tag_iter if (
        tag['category']=='3')] for tag_iter in df['tags']]
    df['tags_cat4'] = [[tag['name'] for tag in tag_iter if (
        tag['category']=='4')] for tag_iter in df['tags']]
    df.drop(['tags'], axis=1, inplace=True)

    return df

def main():
    '''returns all files in a given dir then process each'''
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata_raw_path', required=True, 
    help='Path where to look for metadata files. Should only contain raw metadata.')
    args = parser.parse_args()

    mypath = args.metadata_raw_path    
    files = [os.path.join(mypath, f) for f in os.listdir(
        mypath) if os.path.isfile(os.path.join(mypath, f))]
    
    for f in files:
        print(f)
        read_organize_save(f)

if __name__ == '__main__':
    main()
