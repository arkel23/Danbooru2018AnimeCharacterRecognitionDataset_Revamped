import os
import argparse
import pandas as pd

def filter_only_dafre_ids(df_danbooru, df_dafre, dafre_filename):
    # return only the slice of the metadata corresponding to the images in daf:re
    print(len(df_danbooru), len(df_dafre))

    df_danbooru['id'] = ['{}'.format(x.rsplit('/', 1)[1].split('.', 1)[0]) for x in df_danbooru['dir_long'].astype(str)]
    df_danbooru['size'] = ['{}'.format(x.split('/')[1]) for x in df_danbooru['dir_long'].astype(str)]
    df_danbooru = df_danbooru[df_danbooru['size'].isin(['512px', 'original'])]

    df_dafre['id'] = ['{}'.format(x.split('/')[1].split('.', 1)[0]) for x in df_dafre['dir'].astype(str)]

    df_dafre['id'] = pd.to_numeric(df_dafre['id'])
    df_danbooru['id'] = pd.to_numeric(df_danbooru['id'])

    df_danbooru = df_danbooru[df_danbooru['id'].isin(df_dafre['id'])]
    print(len(df_danbooru))

    df_danbooru_512jpg = df_danbooru[df_danbooru['size']=='512px']['dir_long']
    df_danbooru_512jpg.to_csv('{}_512jpg.txt'.format(dafre_filename), index=False, header=False)

    df_danbooru_originalext = df_danbooru[df_danbooru['size']=='original']['dir_long']
    df_danbooru_originalext.to_csv('{}_originalext.txt'.format(dafre_filename), index=False, header=False)

    print(len(df_danbooru_512jpg), len(df_danbooru_originalext))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--path_danboorufull", default="filelist_original.txt", help="Path for the df with full metadata.")
    parser.add_argument("--path_dafre", default="train.csv", help="Path for the daf:re split.")
    args = parser.parse_args()

    dafre_filename = os.path.splitext(os.path.basename(os.path.normpath(args.path_dafre)))[0]

    df_danbooru = pd.read_csv(args.path_danboorufull, names=['dir_long'])
    df_dafre = pd.read_csv(args.path_dafre, sep=',', names=['class_id', 'dir'])

    filter_only_dafre_ids(df_danbooru, df_dafre, dafre_filename)

if __name__ == '__main__':
    main()

