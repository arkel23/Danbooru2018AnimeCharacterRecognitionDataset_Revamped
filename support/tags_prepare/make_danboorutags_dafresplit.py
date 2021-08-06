import os
import argparse
import pandas as pd

def filter_only_dafre_ids(args):
    # return only the slice of the metadata corresponding to the images in daf:re
    dafre_filename = os.path.splitext(os.path.basename(os.path.normpath(args.dafre_path)))[0]

    df_danbooru = pd.read_csv(args.metadata_df_path)
    df_dafre = pd.read_csv(args.dafre_path, sep=',', names=['class_id', 'dir'])
    
    print(len(df_danbooru), len(df_dafre))
    
    df_dafre['id'] = ['{}'.format(
    x.split('/')[1].split('.', 1)[0]) for x in df_dafre['dir'].astype(str)]
    
    df_dafre['id'] = pd.to_numeric(df_dafre['id'])
    df_danbooru['id'] = pd.to_numeric(df_danbooru['id'])
    
    df_danbooru = df_danbooru[df_danbooru['id'].isin(df_dafre['id'])]
    
    # return the ones that are missing from the 2020 metadata
    #df_danbooru = df_dafre[~df_dafre['id'].isin(df_danbooru['id'])]
    
    df_danbooru = df_danbooru.merge(df_dafre, how='left')
    print(len(df_danbooru))
    df_danbooru = df_danbooru[['id', 'dir', 'class_id', 'tags_cat0', 'tags_cat3', 'tags_cat4']]
    df_danbooru.to_csv('{}_tags.csv'.format(dafre_filename), index=False, header=True)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata_df_path', required=True, 
    help='Path for metadata df (db****_metadata_condensed_v2_minlenX_minappY_undersremoved.csv')
    parser.add_argument('--dafre_path', required=True, 
    help='Path for dafre df ([dafre/train/val/test].csv) in format class_id,dir')
    args = parser.parse_args()
    
    filter_only_dafre_ids(args)

if __name__ == '__main__':
    main()
