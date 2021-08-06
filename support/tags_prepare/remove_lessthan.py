import os
import argparse
import pandas as pd
import ast

def remove_lessthan_lenx_tags(args, df):
    '''remove less than x character tags such as ?, ., :d, etc'''

    print('Original length: ', len(df))
    for cat in [0, 3, 4]:
        print('No of unique tags in cat {} without removing less than {} char tags: {}'.format(
        cat, args.min_len, len(df['tags_cat{}'.format(cat)].explode().unique())))

        print(df.loc[:50, 'tags_cat{}'.format(cat)])
        
        if args.return_less_than:
            df.loc[:, 'tags_cat{}'.format(cat)] = df['tags_cat{}'.format(cat)].apply(
                lambda row: [tag for tag in row if (len(tag) - tag.count(' ')) <= args.min_len])
        else:
            df.loc[:, 'tags_cat{}'.format(cat)] = df['tags_cat{}'.format(cat)].apply(
                lambda row: [tag for tag in row if (len(tag) - tag.count(' ')) > args.min_len])

        print(df.loc[:50, 'tags_cat{}'.format(cat)])
            
        print('No of unique tags in cat {} after removing less than {} char tags: {}'.format(
        cat, args.min_len, len(df['tags_cat{}'.format(cat)].explode().unique())))        
    
    print('Length after: ', len(df))
    return df


def remove_lessthan_xappearances_tags(args, df):
    '''remove tags that appear less than args.min_tag_apperances times'''

    print('Original length: ', len(df))
    for cat in [0, 3, 4]:
        print("No of unique tags in cat {} before removing tags that don't appear at least {} times: {}".format(
        cat, args.min_tag_appearances, len(df['tags_cat{}'.format(cat)].explode().unique())))

        tags_counts = df['tags_cat{}'.format(cat)].explode().value_counts()
            
        df.loc[:, 'tags_cat{}'.format(cat)] = df['tags_cat{}'.format(cat)].apply(
            lambda row: [tag for tag in row if tags_counts['{}'.format(tag)] >= args.min_tag_appearances])
                        
        print("No of unique tags in cat {} after removing tags that don't appear at least {} times: {}".format(
        cat, args.min_tag_appearances, len(df['tags_cat{}'.format(cat)].explode().unique())))        
    
    print('Length after: ', len(df))
    return df


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata_df_path', required=True, 
    help='Path for metadata df (db****_metadata_condensed_v2.csv')
    parser.add_argument('--min_tag_appearances', default=2, type=int,
    help='How many times should a tag appear to be kept in the tag list')
    parser.add_argument('--min_len', default=2, type=int,
    help='Minimum number of characters in tag to be kept in the tag list')
    parser.add_argument('--return_less_than', action='store_true',
    help='If use this flag then it returns only tags with less or equal length than min_len')
    args = parser.parse_args()

    filename = os.path.splitext(os.path.basename(args.metadata_df_path))[0] 

    generic = lambda x: ast.literal_eval(x)
    conv = {'tags_cat0': generic,
        'tags_cat3': generic,
        'tags_cat4': generic}
    df = pd.read_csv(args.metadata_df_path, converters=conv)
    
    df = remove_lessthan_lenx_tags(args, df)

    if args.return_less_than:
        if not args.min_tag_appearances:
            df.to_csv('{}_maxlen{}.csv'.format(filename, args.min_len), index=False, header=True)
        else:
            df = remove_lessthan_xappearances_tags(args, df)
            df.to_csv('{}_maxlen{}_minapp{}.csv'.format(filename, args.min_len, args.min_tag_appearances), index=False, header=True)
    else:
        if not args.min_tag_appearances:
            df.to_csv('{}_minlen{}.csv'.format(filename, args.min_len), index=False, header=True)
        else:
            df = remove_lessthan_xappearances_tags(args, df)
            df.to_csv('{}_minlen{}_minapp{}.csv'.format(filename, args.min_len, args.min_tag_appearances), index=False, header=True)
        

if __name__ == '__main__':
    main()
