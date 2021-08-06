import os
import argparse
import pandas as pd
import ast

def remove_profanity_tags(args, df, profanity_unique):
    '''remove profanities in profanity_unique from tags
    https://github.com/RobertJGabriel/Google-profanity-words/blob/master/list.txt
    https://github.com/ben174/profanity/blob/master/profanity/data/wordlist.txt
    https://github.com/snguyenthanh/better_profanity/blob/master/better_profanity/profanity_wordlist.txt
    '''

    print('Original length: ', len(df))
    for cat in [0]:
        print('No of unique tags in cat {} without removing profanity tags: {}'.format(
        cat, len(df['tags_cat{}'.format(cat)].explode().unique())))

        print(df.loc[:50, 'tags_cat{}'.format(cat)])
        
        df.loc[:, 'tags_cat{}'.format(cat)] = df['tags_cat{}'.format(cat)].apply(
            lambda row: [tag for tag in row if not any(prof in tag for prof in profanity_unique)])

        print(df.loc[:50, 'tags_cat{}'.format(cat)])
            
        print('No of unique tags in cat {} after removing profanity tags: {}'.format(
        cat, len(df['tags_cat{}'.format(cat)].explode().unique())))        
    
    print('Length after: ', len(df))
    return df



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata_df_path', required=True, 
    help='Path for metadata df (db****_metadata_condensed_v2.csv')
    parser.add_argument('--profanity_list_path', required=True, 
    help='Path for profanity_list.txt file with list of words to filter from.')
    args = parser.parse_args()

    filename = os.path.splitext(os.path.basename(args.metadata_df_path))[0] 

    generic = lambda x: ast.literal_eval(x)
    conv = {'tags_cat0': generic,
        'tags_cat3': generic,
        'tags_cat4': generic}
    df = pd.read_csv(args.metadata_df_path, converters=conv)

    with open(args.profanity_list_path, 'r') as myfile:
        profanity_list = myfile.read().splitlines()
        print(len(profanity_list))
        profanity_unique = set(profanity_list)
    
        df = remove_profanity_tags(args, df, profanity_unique)

    df.to_csv('{}_profsremoved.csv'.format(filename), index=False, header=True)
        

if __name__ == '__main__':
    main()
