import argparse
import os
import pandas as pd
import ast
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']

def print_write(f, curr_line):
    print(curr_line)
    f.write(curr_line)


def plot_wordcloud(args, data, cat, level):
    # https://towardsdatascience.com/how-to-create-beautiful-word-clouds-in-python-cfcf85141214
    # Custom Colormap: https://mubaris.com/posts/dataviz-wordcloud/
    colors = ["#0b1c4b", "#550a5e"]
    cmap = LinearSegmentedColormap.from_list("mycmap", colors)

    title = 'Wordcloud of {} of {} tags on {} level'.format(cat, args.title, level)
    cloud = WordCloud(width=1000,
                      height=750,
                      max_words=args.no_words_wc,
                      colormap=cmap,
                      background_color='white'
                      ).generate_from_frequencies(data)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(cloud)
    plt.axis('off')
    ax.set_title(title, fontsize=20)
    fig.tight_layout()
    fig.savefig(os.path.join(args.results_dir, 'wordcloud_{}_{}_{}.{}'.format(args.filename, cat, level, args.save_format)), dpi=300)


def plot_histogram(args, data, cat, no_bins, level, display_text=False):
    fig, axs = plt.subplots(1)
    fig.suptitle('Histogram of category {} of {} tags on {} level'.format(cat, args.title, level))

	# no of bins plotted depends on if it should display text along ticks or not
    bins = no_bins
    axs.bar(np.arange(bins), data.iloc[0:bins].to_numpy())
		
    axs.set_ylabel('No. of samples per tag')
    axs.set_title('Ordered based on no. of samples')
    axs.tick_params(axis='both', labelsize=8)
    
    if display_text == True:
        axs.set_xticks(np.arange(bins))
        axs.set_xticklabels(data.index[0:bins], rotation=90)
    
    fig.tight_layout()
    fig.savefig(os.path.join(args.results_dir, 
	'histogram_{}_{}_disptext{}_{}.{}'.format(args.filename, cat, display_text, level, args.save_format)), dpi=300)


def whole_df_stats(df, f):

    curr_line = 'Total number of files: {}\n'.format(len(df))
    print_write(f, curr_line)

    curr_line = 'Number of files by extension\n'
    print_write(f, curr_line)
    curr_line = str(df.groupby('file_ext').count()['id'])
    print_write(f, curr_line)

    mean_width, mean_height = df[['image_width', 'image_height']].mean()
    median_width, median_height = df[['image_width', 'image_height']].median()
    std_width, std_height = df[['image_width', 'image_height']].std()
    
    curr_line = '''\nMean, median, and standard deviation of image width and height:\n
    {}\t{}\t{}\n
    {}\t{}\t{}\n'''.format(mean_width, median_width, std_width,
    mean_height, median_height, std_height)
    print_write(f, curr_line)

    curr_line = 'Sample of data: {}\n'.format(str(df.head(5)))
    print_write(f, curr_line)


def tag_stats(df, f, args):
    '''
    Stats for the tags by category
    How many unique tags for each category
    Most counts for each category
    Average, median and std deviation # of tags for each category
    Average, median and std deviation # of tags for each image
    '''
    
    if not args.skip_cat34:
        tags_categories_list = ['tags_cat0', 'tags_cat3', 'tags_cat4']
    else:
        tags_categories_list = ['tags_cat0']
        
    for category in tags_categories_list:
        curr_line = 'For category "{}" at tag level:\n'.format(category)
        print_write(f, curr_line)
        single_df_stats(df, category, f, args, level='tag')

        if args.stats_wordlevel and category == 'tags_cat0':
            curr_line = 'For category "{}" at word level:\n'.format(category)
            print_write(f, curr_line)
            df['{}'.format(category)] = df['{}'.format(category)].apply(lambda x: ' '.join(map(str, x))).str.split(pat=' ')
            single_df_stats(df, category, f, args, level='word')


def single_df_stats(df, cat, f, args, level):
    '''stats per tag category
    each tag category includes a list composed of multiple strings
    Explode breaks the list items into separate rows
    str.len returns number of chars for strings or number of entries dictionaries, list or tuples
    How many unique tags, and how is the distribution of tags for each category (how often each tag is used)
    '''
    unique = df['{}'.format(cat)].explode().unique()
    tags_counts = df['{}'.format(cat)].explode().value_counts().sort_values(ascending=False)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also    
        curr_line = 'No of unique {}s: {}\n'.format(level, len(unique))
        print_write(f, curr_line)
        curr_line = 'Total no. of {}s: {}\n'.format(level, tags_counts.sum())
        print_write(f, curr_line)
        curr_line = str(tags_counts.head(args.text_top_k))
        print_write(f, curr_line)
        curr_line = '\nMean, median, and std deviation of {}s per tag category (how often each {} is used relative to category):\n{}\t{}\t{}\n'.format(
            level, level, tags_counts.mean(), tags_counts.median(), tags_counts.std())
        print_write(f, curr_line)
        
        # stats per image: distribution of how many tags for each category per image
        tags_cat_len = df['{}'.format(cat)].str.len()
        curr_line = '\nMean, median, and std deviation of {}s per image per tag category (how many {}s per image according to category):\n{}\t{}\t{}\n'.format(
            level, level, tags_cat_len.mean(), tags_cat_len.median(), tags_cat_len.std())
        print_write(f, curr_line)

        # distribution plot (one with tag text along axis labels and one without)
        plot_histogram(args, tags_counts, cat=cat, no_bins=args.no_bins_nodisplay, level=level, display_text=False)
        plot_histogram(args, tags_counts, cat=cat, no_bins=args.no_bins_display, level=level, display_text=True)

        # word cloud
        plot_wordcloud(args, tags_counts, cat=cat, level=level)

    
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default='Danbooru2020', type=str,
                        help="Title for plots/Dataset name")
    parser.add_argument("--file_path", required=True, type=str,
                        help="File path")
    parser.add_argument("--stats", choices=['tags', 'all'], 
                        default='tags', help="Print metadata stats if all (image width, height and types)")
    parser.add_argument("--results_dir", default="eda", type=str,
                        help="The directory where results will be stored")
    parser.add_argument("--text_top_k", default=1000, type=int,
                        help="No of top K tags to display")
    parser.add_argument("--no_bins_display", default=20, type=int,
                        help="No of bins for histogram when tag text is displayed")
    parser.add_argument("--no_bins_nodisplay", default=50, type=int,
                        help="No of bins for histogram when tag text isn't displayed")
    parser.add_argument("--no_words_wc", default=50, type=int,
                        help="No of words to display in wordcloud")
    parser.add_argument("--stats_wordlevel", action='store_true',
                        help="Print stats on word level if use this command")
    parser.add_argument("--save_format", choices=['pdf', 'png', 'jpg'], default='png', type=str,
                        help="Print stats on word level if use this command")
    parser.add_argument("--skip_cat34", action='store_true',
                        help="Skip cat 3 and 4 if use this command")
    args = parser.parse_args()

    generic = lambda x: ast.literal_eval(x)
    conv = {'tags_cat0': generic, 
        'tags_cat3': generic, 
        'tags_cat4': generic}
    df = pd.read_csv(args.file_path, converters=conv)

    filename = os.path.splitext(os.path.basename(args.file_path))[0] 
    args.filename = filename
    if not os.path.exists(args.results_dir):
        os.makedirs(args.results_dir)  
    f = open(os.path.join(args.results_dir, '{}_stats.txt'.format(filename)), 'w')
    
    if args.stats == 'all':
        whole_df_stats(df, f)
    tag_stats(df, f, args) 

    f.close()  

if __name__ == '__main__':
    main()

