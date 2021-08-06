import os
import argparse
import pandas as pd
from PIL import Image

from combine_metadata import make_data_dic

def filter_boolean(df):
    '''Filters by metadata based on boolean attributes'''

    print('Pre-filtering boolean: ', len(df))

    df = df.loc[(df['is_pending']==False) & 
    (df['is_flagged']==False) & 
    (df['is_deleted']==False) & 
    (df['is_banned']==False)]
    
    df.drop(['is_pending', 'is_flagged', 'is_deleted', 'is_banned'], axis=1, inplace=True)

    print('Post-filtering boolean: ', len(df))

    return df


def filter_rating(df):
    '''Filters by image rating: safe (s)'''

    print('Pre-filtering by rating (safe only): ', len(df))

    df = df.loc[(df['rating']=='s')]
    df.drop(['rating'], axis=1, inplace=True)
    
    print('Post-filtering by rating (safe only): ', len(df))

    return df


def filter_exist(df):
    '''Filters images that don't exist/can't be found'''

    print('Pre-filtering by exist (can be found): ', len(df))

    df = df[df['path_img'].apply(lambda x: os.path.isfile(os.path.join('512px', x)))]
    
    print('Post-filtering by exist (can be found): ', len(df))

    return df


def filter_openrgb(df):
    '''Filters images that don't exist/can't be found'''

    print('Pre-filtering not RGB: ', len(df))

    df = df[df['path_img'].apply(lambda x: Image.open(os.path.join('512px', x)).mode=='RGB')]
    
    print('Post-filtering not RGB: ', len(df))  
    
    return df

def filter_emptytagcat(df):
    '''convert tags to string columns and then delete those that are empty (no NaN)
    https://stackoverflow.com/questions/52232742/how-to-use-ast-literal-eval-in-a-pandas-dataframe-and-handle-exceptions'''

    print('Pre-filtering empty tag categories: ', len(df))

    for cat in [4, 3, 0]:
        print('No of unique tags in cat {} without filtering for images with empty lists in either category: {}'.format(
        cat, len(df['tags_cat{}'.format(cat)].apply(lambda x: ast.literal_eval(str(x))).explode().unique())))

        df.loc[:, 'tags_cat{}_str'.format(cat)] = df['tags_cat{}'.format(cat)].apply(lambda x: ast.literal_eval(str(x))).apply(lambda x: ', '.join(map(str, x)))
        df = df[df['tags_cat{}_str'.format(cat)].eq('')==False]

        df.drop(columns=['tags_cat{}_str'.format(cat)], inplace=True)
        print('No of unique tags in cat {} after filtering for empty lists: {}'.format(
        cat, len(df['tags_cat{}'.format(cat)].apply(lambda x: ast.literal_eval(str(x))).explode().unique())))
        print('Length after filtering category {}: {}'.format(cat, len(df)))

    print('Post-filtering empty tag categories: ', len(df))
    return df


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata_df_path', required=True, 
    help='Path for metadata df (db****_metadata_condensed_v1.csv')
    parser.add_argument('--year', default=2020, type=int, 
    help='Year of metadata files. Default=2020 (2018 for DAF:re')
    parser.add_argument('--filt_bool', action='store_false',
    help='Filter by boolean categories (is_pending, is_flagged, is_deleted, is_banned')
    parser.add_argument('--filt_rating', action='store_false',
    help='Filter by safe rating (in contrast to questionable or explicit.')
    parser.add_argument('--filt_exist', action='store_false',
    help='Filter by if file exists')
    parser.add_argument('--filt_rgb', action='store_false',
    help='Filter by if file can be opened as RGB using PIL.Image')
    parser.add_argument('--filt_emptytag', action='store_false',
    help='Filter files if tag is empty')
    args = parser.parse_args()
 
    df = pd.read_csv(args.metadata_df_path)

    if args.filt_bool:
        df = filter_boolean(df)
    if args.filt_rating:
        df = filter_rating(df)
    if args.filt_exist:
        df = filter_exist(df)
        make_data_dic(df, version=2, year=args.year)
    if args.filt_rgb: 
        df = filter_openrgb(df)
        make_data_dic(df, version=2, year=args.year)
    if args.filt_emptytag:
        df = filter_emptytagcat(df)
    make_data_dic(df, version=2, year=args.year)

if __name__ == '__main__':
    main()
