import os
import argparse
import pandas as pd
import ast
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.transform import resize
from PIL import Image

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
    inp = None
    i = 0

    while not inp:

        curr_index = perm[i]

        tag_cat0 = df.iloc[curr_index]['tags_cat0']
        tag_cat3 = df.iloc[curr_index]['tags_cat3']
        tag_cat4 = df.iloc[curr_index]['tags_cat4']

        class_id = df.iloc[curr_index]['class_id']
        class_name = df_classes.loc[df_classes['class_id']==class_id]['class_name'].item()

        print('Description tags (cat0):', tag_cat0)
        print('Series/show/medium tags (cat3):', tag_cat3)
        print('Character name/series tags (cat4):', tag_cat4)
        print('Class name (DAF:re): ', class_name)

        if args.mode == 'face_grey':
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
        img_combined = np.hstack((img_1, img_2))

        plt.imshow(img_combined)
        plt.show()
        
        inp = input('Enter anything that is not blank to stop visualizing: ')
        i += 1

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_data_root', required=True, help='Path for dataset root')
    parser.add_argument('--path_file_list', required=True, help='Path for file list')
    parser.add_argument('--mode', type=str, choices=['faces_full', 'faces_grey', 'full_grey'], 
    default='faces_full', help='Visualize full vs faces or faces rgb vs grey or full rgb vs grey')
    parser.add_argument('--height', type=int, default=256, help='args.height for resized images')
    parser.add_argument('--width', type=int, default=256, help='Width for resized images')
    args = parser.parse_args()

    visualize_random_images(args)
