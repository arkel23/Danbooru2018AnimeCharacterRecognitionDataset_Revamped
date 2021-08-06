import os
import argparse
import pandas as pd
import ast

def remove_underscores(df):
    # https://regex101.com/ 
    # https://stackoverflow.com/questions/64235312/how-to-implodereverse-of-pandas-explode-based-on-a-column    
    '''separate numbers from text and remove symbols/punctuations (_, ., /) from strings, then replace original tags_catX'''

    print('Original length: ', len(df))
    for cat in [0, 3, 4]:
        print('No of unique tags in cat {}: {}'.format(
        cat, len(df['tags_cat{}'.format(cat)].explode().unique())))

        print(df.loc[:50, 'tags_cat{}'.format(cat)])
        df.loc[:, 'tags_cat{}_str'.format(cat)] = df['tags_cat{}'.format(cat)].apply(lambda x: ', '.join(map(str, x)))
        
        df.replace({'tags_cat{}_str'.format(cat): r'(\d{1})([girl|boy]+)'}, {'tags_cat{}_str'.format(cat): r'\g<1> \g<2>'}, regex=True, inplace=True)
        df.replace({'tags_cat{}_str'.format(cat): r'(6\+)(\w+)'}, {'tags_cat{}_str'.format(cat): r'\g<1> \g<2>'}, regex=True, inplace=True)
        df.replace({'tags_cat{}_str'.format(cat): r'[\\~\#\%\&\*\{\}\<\>\?\!\|\"\-\^\;\.\:\_\/]+'}, {'tags_cat{}_str'.format(cat): r' '}, regex=True, inplace=True)
        
        df.loc[:, 'tags_cat{}'.format(cat)] = df['tags_cat{}_str'.format(cat)].str.split(pat=', ')
        df.loc[:, 'tags_cat{}'.format(cat)] = df['tags_cat{}'.format(cat)].apply(
                lambda row: [tag for tag in row if (len(tag) - tag.count(' ')) > 0])

        print(df.loc[:50, 'tags_cat{}'.format(cat)])
        df.drop(columns=['tags_cat{}_str'.format(cat)], inplace=True)
        
        print('No of unique tags in cat {}: {}'.format(
        cat, len(df['tags_cat{}'.format(cat)].explode().unique())))

        print('Length after filtering category {}: {}'.format(cat, len(df)))

    print('Length after: ', len(df))
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata_df_path', required=True, 
    help='Path for metadata df (db****_metadata_condensed_v2_minlenX_minappY.csv')
    args = parser.parse_args()
 
    filename = os.path.splitext(os.path.basename(args.metadata_df_path))[0] 
    
    generic = lambda x: ast.literal_eval(x)
    conv = {'tags_cat0': generic,
        'tags_cat3': generic,
        'tags_cat4': generic}
    df = pd.read_csv(args.metadata_df_path, converters=conv)
    
    df = remove_underscores(df)

    df.to_csv('{}_symbolsremoved.csv'.format(filename), index=False, header=True)
   
if __name__ == '__main__':
    main()
