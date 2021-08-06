import os
import argparse
import pandas as pd
import ast
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.transform import resize
from PIL import Image

def print_plot(df, df_classes, curr_index, img_combined):
    
    tag_cat0 = df.iloc[curr_index]['tags_cat0']
    tag_cat3 = df.iloc[curr_index]['tags_cat3']
    tag_cat4 = df.iloc[curr_index]['tags_cat4']

    class_id = df.iloc[curr_index]['class_id']
    class_name = df_classes.loc[df_classes['class_id']==class_id]['class_name'].item()

    title = []
        
    curr_line = 'Description tags (cat0): {}\n'.format(tag_cat0)
    title.append(curr_line)
    print(curr_line)
        
    curr_line = 'Series/show/medium tags (cat3): {}\n'.format(tag_cat3)
    title.append(curr_line)
    print(curr_line)
        
    curr_line = 'Character name/series tags (cat4): {}\n'.format(tag_cat4)
    title.append(curr_line)
    print(curr_line)

    curr_line = 'Class name (DAF:re): {}\n'.format(class_name)
    title.append(curr_line)
    print(curr_line)

    plt.imshow(img_combined)
    plt.title(''.join(title), fontsize=6, wrap=True)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
        

def visualize_random_images(args):
    '''return random images from dafre along
    with their tags, input anything that is not empty to exit
    '''
    
    df = pd.read_csv(args.path_file_list)
    df_classes = pd.read_csv(os.path.join(args.path_data_root, 'labels', 'classid_classname.csv'),
                sep=',', header=None, names=['class_id', 'class_name'],
                dtype={'class_id': 'UInt16', 'class_name': 'object'})

    no_images = len(df)
    perm = np.random.permutation(no_images)
    
    for curr_index in perm:

        if args.mode == 'faces_grey':
            img_1 = mpimg.imread(os.path.join(args.path_data_root, 'faces', df.iloc[curr_index]['dir']))
            img_2 = np.stack((Image.open(os.path.join(args.path_data_root, 'faces', df.iloc[curr_index]['dir'])).convert('L'),)*3, axis=-1)
        elif args.mode == 'full_grey':
            img_1 = mpimg.imread(os.path.join(args.path_data_root, 'fullMin256', df.iloc[curr_index]['dir']))
            img_2 = np.stack((Image.open(os.path.join(args.path_data_root, 'fullMin256', df.iloc[curr_index]['dir'])).convert('L'),)*3, axis=-1)
        else:
            img_1 = mpimg.imread(os.path.join(args.path_data_root, 'fullMin256', df.iloc[curr_index]['dir']))
            img_2 = mpimg.imread(os.path.join(args.path_data_root, 'faces', df.iloc[curr_index]['dir']))
        
        img_1 = resize(img_1, (args.width, args.height))
        img_2 = resize(img_2, (args.width, args.height))
        
        if args.mode in ['faces_grey', 'full_grey', 'faces_full']:
            img_combined = np.hstack((img_1, img_2))
        elif args.mode == 'faces_only':
            img_combined = img_2
        else: # full_only
            img_combined = img_1

        print_plot(df, df_classes, curr_index, img_combined)

        inp = input('Enter anything that is not blank to stop visualizing: ')
        if inp:
            break
            

def visualize_bytag(args):
    '''return random images from danbooru along
    with their tags, input anything that is not empty to exit
    '''
    df = pd.read_csv(args.path_file_list)
    df_classes = pd.read_csv(os.path.join(args.path_data_root, 'labels', 'classid_classname.csv'),
                sep=',', header=None, names=['class_id', 'class_name'],
                dtype={'class_id': 'UInt16', 'class_name': 'object'})
    
    inp = None
    while not inp:

        cat = int(input('Search by tag cat: 0 (descriptions), 3 (franchise), 4 (character). Your choice: '))
        assert cat in [0, 3, 4], "Tag cat not 0, 3 or 4."
        tag_cand = str(input('Tag text candidate: '))
        
        df.loc[:, 'tags_cat{}'.format(cat)] = df['tags_cat{}'.format(cat)].apply(lambda x: ast.literal_eval(str(x)))
        df.loc[:, 'tags_cat{}_str'.format(cat)] = df['tags_cat{}'.format(cat)].apply(lambda x: ', '.join(map(str, x)))

        tags_unique_all = df['tags_cat{}'.format(cat)].explode().unique()
        tags_candidates = [tag for tag in tags_unique_all if '{}'.format(tag_cand) in tag]
        print('No of tags that meet search results out of total number of tags: {}/{}'.format(
        len(tags_candidates), len(tags_unique_all)))
        print(tags_candidates)
        
        tag_final = input('Choose among one of the tags that meet the candidate search results: ')
        df_bytag = df[df['tags_cat{}_str'.format(cat)].str.contains('{}'.format(tag_final))]
        print('Total no of images that meet the string search result: ', len(df_bytag))
        
        perm = np.random.permutation(df_bytag.index)
        for curr_index in perm:
            
            img = mpimg.imread(os.path.join(args.path_data_root, 'fullMin256', df.iloc[curr_index]['dir']))
            
            print_plot(df, df_classes, curr_index, img)
            
            inp_2 = input('Enter anything that is not blank to stop visualizing: ')

            if inp_2:
                break
        
        df.drop(columns=['tags_cat{}_str'.format(cat)], inplace=True)
        
        inp = input('Enter anything that is not blank (again) to stop visualizing: ')

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_data_root', required=True, help='Path for dataset root')
    parser.add_argument('--path_file_list', required=True, help='Path for file list')
    parser.add_argument('--mode', type=str, 
    choices=['faces_full', 'faces_grey', 'full_grey', 'faces_only', 'full_only'], 
    default='faces_full', help='Visualize full vs faces or faces rgb vs grey or full rgb vs grey')
    parser.add_argument('--height', type=int, default=256, help='args.height for resized images')
    parser.add_argument('--width', type=int, default=256, help='Width for resized images')
    parser.add_argument('--search_bytag', action='store_true', help='if use this flag then allows to search by tag cat and string')
    args = parser.parse_args()

    if not args.search_bytag:
        visualize_random_images(args)
    else:
        visualize_bytag(args)