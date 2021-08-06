import os
import ast
import argparse
import pandas as pd

def fill_empty(df):
    '''Replaces empty ('') or any number of white space and nothing else to 'unlabeled'''

    print('Pre-filtering empty tag categories: ', len(df))

    for cat in [4, 3, 0]:
        print('No of unique tags in cat {} without filtering/filling for images with empty lists in either category: {}'.format(
        cat, len(df['tags_cat{}'.format(cat)].apply(lambda x: ast.literal_eval(str(x))).explode().unique())))

        df.loc[:, 'tags_cat{}_str'.format(cat)] = df['tags_cat{}'.format(cat)].apply(lambda x: ast.literal_eval(str(x))).apply(lambda x: ', '.join(map(str, x)))
        print('Empty strings (originally): ', len(df[df['tags_cat{}_str'.format(cat)].eq('')==True]))
        df.replace({'tags_cat{}_str'.format(cat): r'^\s*$'}, {'tags_cat{}_str'.format(cat): r'unlabeled'}, regex=True, inplace=True)
        print('Empty strings (after): ', len(df[df['tags_cat{}_str'.format(cat)].eq('')==True]))

        df.loc[:, 'tags_cat{}'.format(cat)] = df['tags_cat{}_str'.format(cat)].str.split(pat=', ')
        df.drop(columns=['tags_cat{}_str'.format(cat)], inplace=True)
        print('No of unique tags in cat {} after filtering/filling for empty lists: {}'.format(
        cat, len(df['tags_cat{}'.format(cat)].apply(lambda x: ast.literal_eval(str(x))).explode().unique())))
        print('Length after filtering category {}: {}'.format(cat, len(df)))

    print('Post-filtering empty tag categories: ', len(df))
    return df


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata_df_path', required=True, 
    help='Path for metadata df (db****_metadata_condensed_v1.csv')
    args = parser.parse_args()

    filename = os.path.splitext(os.path.basename(args.metadata_df_path))[0] 
 
    df = pd.read_csv(args.metadata_df_path)
    df = fill_empty(df)

    df.to_csv('{}_filledempty.csv'.format(filename), index=False, header=True)


if __name__ == '__main__':
    main()