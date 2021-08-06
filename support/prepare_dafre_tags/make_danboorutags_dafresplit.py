import os
import sys
import pandas as pd
import ast

def filter_only_dafre_ids(df_danbooru, df_dafre, dafre_filename):
    # return only the slice of the metadata corresponding to the images in daf:re
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

    try:
        mypath_danbooru = sys.argv[1]
        mypath_dafre = sys.argv[2]
    except:
        mypath_danbooru = 'db2018_metadata_essential_v1.csv'
        mypath_dafre = 'danbooru2018_faces_85.csv'
        #mypath_dafre = 'train_dafre.csv')
    dafre_filename = os.path.splitext(os.path.basename(os.path.normpath(mypath_dafre)))[0]

    df_danbooru = pd.read_csv(mypath_danbooru)
    df_dafre = pd.read_csv(mypath_dafre, sep=',', names=['class_id', 'dir'])
    
    filter_only_dafre_ids(df_danbooru, df_dafre, dafre_filename)

if __name__ == '__main__':
    main()
