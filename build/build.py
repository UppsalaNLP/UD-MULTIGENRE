#!/usr/bin/python3

import argparse, sys, os, re, logging
from collections import defaultdict
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split

# local imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from UD_dataclasses import *
from mapping import *

logger = logging.getLogger('dataset_constructor')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


def parse_arguments():
    arg_parser = argparse.ArgumentParser(description='UD-MULTIGENRE: build training and development sets')
    arg_parser.add_argument('ud_path', help='path to UD folder')

    return arg_parser.parse_args()


def split_list(list_to_split, test_size):
    """creates training and development splits"""

    train_data, test_data = train_test_split(list_to_split, test_size=test_size, random_state=42)
    return train_data, test_data


def load_f(fname):
    with open(fname, 'rb') as inp:
        return pickle.load(inp)


def create_data_df(final):
    """creates a pandas df with columns 'language', 'corpus', 'genre', 'sentences'"""

    df_data = []

    for language, lang_data in final.items():
        for corpus, corpus_data in lang_data.items():
            for genre, genre_data in corpus_data.items():
                df_data.append([language, corpus, genre, genre_data])
    final_df = pd.DataFrame(df_data, columns=['language', 'corpus', 'genre', 'sentences'])
    return final_df


def assign_data_to_df(df, data, c, g):
    """assigns sample of sentences to treebank and genre"""
    df.loc[(df.corpus == c) & (df.genre == g), 'sentences'] = [data]
    return df


def extract_instances(tb, lang, name):
    """groups sentences by genre within treebanks based on metadata if it is available"""
    genre_group = defaultdict(list)

    for genre in map_lang[lang][name]:

        if len(map_lang[lang][name][genre]) > 0:

            _comment_regex_list = map_lang[lang][name][genre]
            group = []

            # group by genre from Romanian RRT based on newdoc id
            if (lang == 'Romanian') & (name == 'RRT'):

                tpls = [(tb.get_sentences().index(sentence), comment) for sentence in tb.get_sentences() for comment in
                        sentence.get_comments() if 'newdoc id' in comment]
                group = []

                for _comment_regex in _comment_regex_list:

                    start = next(obj for obj in tpls if _comment_regex in obj[1])
                    startid = tpls.index(start)

                    for obj in tpls[startid:]:

                        if _comment_regex not in obj[1]:
                            end = obj[0]
                            break

                    group += tb.get_sentences()[start[0]:end]

                    # group by genre from other tbs that have patterns available for genres
            else:

                for sentence in tb.get_sentences():
                    for comment in sentence.get_comments():

                        for _comment_regex in _comment_regex_list:
                            if re.match(_comment_regex, comment):
                                group.append(sentence)

        else:

            group = tb.get_sentences()

        genre_group[genre] = group

    return genre_group


def write_files(sentences, ftxt, fconllu):
    """writes training and development sets to .txt and .conllu"""
    if sentences:
        with open(fconllu, 'w') as f:
            for sent in sentences:

                conllu = '\n'.join(sent._comments) + '\n' if sent._comments else ''

                conllu_tok_seq = []
                for tok in sent._tokens:
                    for w in tok._words:
                        if w.head == None:
                            w.head = '_'
                    conllu_tok_seq.append(tok.to_conllu())

                conllu += '\n'.join(conllu_tok_seq)
                conllu += '\n\n'
                f.write(conllu)

        with open(ftxt, 'w') as f:
            for sent in sentences:
                f.write(sent.to_text() + '\n')

df_dev = pd.DataFrame()

def create_dataset(df_training):
    """creates a folder named UD-multigenre that contains genre subfolders. Under each genre subfolder
    you'll find treebank folders with the corresponding subsets. Treebank folder names are in UD format"""
    global df_dev

    language = df_training['language']
    tb_name = df_training['corpus']
    genre = df_training['genre']

    UD_folder = 'UD-multigenre'
    main_folder = f'{genre}'
    sub_folder_name = f'UD_{language}-{tb_name}'

    folders_to_create = [UD_folder, f'{UD_folder}/{main_folder}', f'{UD_folder}/{main_folder}/{sub_folder_name}']

    for folder in folders_to_create:
        if not os.path.exists(folder):
            os.makedirs(folder)

    main_path = f'{UD_folder}/{main_folder}/{sub_folder_name}'

    path_train_conllu = os.path.join(main_path, f'{genre}-train.conllu')
    path_train_txt = os.path.join(main_path, f'{genre}-train.txt')

    sentences_train = df_training['sentences']

    try:
        sentences_dev = \
            df_dev[(df_dev.language == language) & (df_dev.corpus == tb_name) & (df_dev.genre == genre)][
                'sentences'].tolist()[
                0]

        path_dev_conllu = os.path.join(main_path, f'{genre}-dev.conllu')
        path_dev_txt = os.path.join(main_path, f'{genre}-dev.txt')

        write_files(sentences_dev, path_dev_txt, path_dev_conllu)
        write_files(sentences_train, path_train_txt, path_train_conllu)

    except:

        write_files(sentences_train, path_train_txt, path_train_conllu)

    return None


def main():

    global df_dev

    logger.info('Prepares for loading UD data ...')

    args = parse_arguments()

    # check if UD  data folder exists
    if not os.path.exists(args.ud_path):
        print(
            r"[Error] Please introduce a valid UD folder path and try again. Could not find the path '{args.ud_path}'")
        exit(1)

    # Load Nynorsk data
    nyblogtrain = load_f('Nynorsk_data/Nynorsk_blog_train.pkl')
    nyparltrain = load_f('Nynorsk_data/Nynorsk_parl_train.pkl')
    nyretrain = load_f('Nynorsk_data/Nynorsk_legal_train.pkl')
    nynewstrain = load_f('Nynorsk_data/Nynorsk_news_train.pkl')

    nyblogdev = load_f('Nynorsk_data/Nynorsk_blog_dev.pkl')
    nyparldev = load_f('Nynorsk_data/Nynorsk_parl_dev.pkl')
    nyredev = load_f('Nynorsk_data/Nynorsk_legal_dev.pkl')
    nynewsdev = load_f('Nynorsk_data/Nynorsk_news_dev.pkl')
    logger.info('Nynorsk data loaded successfully')

    # Load treebanks
    ud_path = args.ud_path
    ud = UniversalDependencies.from_directory(ud_path, ud_filter=None, verbose=True)
    logger.info('UD data loaded successfully')

    # Initialize train and dev dicts
    training_data = defaultdict(dict)
    dev_data = defaultdict(dict)

    # Populate training and development data dicts
    for tb in ud.get_treebanks():

        lang = tb.get_language()
        name = tb.get_treebank_name()

        # Norwegian Nynorsk
        if (lang == 'Norwegian') & (name == 'Nynorsk'):

            if 'train' in tb.get_name():
                training_data[lang][name] = {'blog': nyblogtrain,
                                             'parliament': nyparltrain,
                                             'legal': nyretrain,
                                             'news': nynewstrain}

            elif 'dev' in tb.get_name():
                dev_data[lang][name] = {'blog': nyblogdev,
                                        'parliament': nyparldev,
                                        'legal': nyredev,
                                        'news': nynewsdev}

        # German GSD
        if (lang == 'German') & (name == 'GSD'):

            metagenre = 'reviews'

            if 'train' in tb.get_name():

                group_gsd = []

                for sentence in tb.get_sentences():
                    for comment in sentence.get_comments():
                        if 'sent_id' in comment:
                            if int(re.findall(r'(?<=sent_id = train-s)\d+', comment)[0]) <= 1500:
                                group_gsd.append(sentence)

                training_data[lang][name] = {'reviews': group_gsd,
                                             }

            elif 'dev' in tb.get_name():

                group_gsd = []

                for sentence in tb.get_sentences():
                    for comment in sentence.get_comments():
                        if 'sent_id' in comment:
                            if int(re.findall(r'(?<=sent_id = dev-s)\d+', comment)[0]) <= 500:
                                group_gsd.append(sentence)

                dev_data[lang][name] = {'reviews': group_gsd}

        # Other tbs with patterns available
        if (lang in map_lang) & (name in map_lang[lang]):

            if 'train' in tb.get_name():

                training_data[lang][name] = extract_instances(tb, lang, name)


            elif 'dev' in tb.get_name():

                dev_data[lang][name] = extract_instances(tb, lang, name)

            # Cases where we don't have sufficient training/development data for dev

            # too few samples in train, so we include test
            elif (lang == 'Italian') & (name == 'ParlaMint') & ('test' in tb.get_name()):

                genre_group = {'parliament': tb.get_sentences()}
                dev_data[lang][name] = genre_group

            else:
                continue
    logger.info('Training and development data is loaded for each genre')

    # Create train and dev dataframes
    df_train = pd.DataFrame()

    df_train = create_data_df(training_data)
    df_dev = create_data_df(dev_data)

    # In cases where we don't have sufficient training/development data,
    # we add from either training to development or vice versa in case sufficient data is available
    # we consider 10k tokens per train as sufficient for our experiments
    test_size = 0.2
    lt_train, lt_dev = split_list(
        df_train[(df_train.corpus == 'ALKSNIS') & (df_train.genre == 'academic')].sentences.tolist()[0], test_size)
    Taigareviews_train, Taigareviews_dev = split_list(
        df_train[(df_train.corpus == 'Taiga') & (df_train.genre == 'reviews')].sentences.tolist()[0], test_size)
    TaigaQA_train, TaigaQA_dev = split_list(
        df_train[(df_train.corpus == 'Taiga') & (df_train.genre == 'QA')].sentences.tolist()[0], test_size)
    Alpinoqa_train, Alpinoqa_dev = split_list(
        df_train[(df_train.corpus == 'Alpino') & (df_train.genre == 'QA')].sentences.tolist()[0], test_size)
    Alpinon_train, Alpinon_dev = split_list(
        df_train[(df_train.corpus == 'Alpino') & (df_train.genre == 'news')].sentences.tolist()[0], test_size)
    SNKfic_train, SNKfic_dev = split_list(
        df_train[(df_train.corpus == 'SNK') & (df_train.genre == 'fiction')].sentences.tolist()[0], test_size)
    Indo_train, Indo_dev = split_list(
        df_train[(df_train.corpus == 'CSUI') & (df_train.genre == 'news')].sentences.tolist()[0], test_size)
    SST_train, SST_dev = split_list(
        df_train[(df_train.corpus == 'SST') & (df_train.genre == 'spoken')].sentences.tolist()[0], test_size)
    SNTRusnews_train, SNTRusnews_dev = split_list(
        df_train[(df_train.corpus == 'SynTagRus') & (df_train.genre == 'news')].sentences.tolist()[0], test_size)
    SNTRusnewsnonfico_train, SNTRusnewsnonfico_dev = split_list(
        df_train[(df_train.corpus == 'SynTagRus') & (df_train.genre == 'nonfiction_prose')].sentences.tolist()[0],
        test_size)
    sk_wiki_train, sk_wiki_dev = split_list(
        df_dev[(df_dev.corpus == 'SNK') & (df_dev.genre == 'wiki')].sentences.tolist()[0], 0.1)

    # Assign data to train
    df_train.loc[(df_train.corpus == 'Taiga') & (df_train.genre == 'reviews'), 'sentences'] = [Taigareviews_train]
    df_train.loc[(df_train.corpus == 'Taiga') & (df_train.genre == 'QA'), 'sentences'] = [TaigaQA_train]
    df_train.loc[(df_train.corpus == 'ALKSNIS') & (df_train.genre == 'academic'), 'sentences'] = [lt_train]
    df_train.loc[(df_train.corpus == 'Alpino') & (df_train.genre == 'QA'), 'sentences'] = [Alpinoqa_train]
    df_train.loc[(df_train.corpus == 'Alpino') & (df_train.genre == 'news'), 'sentences'] = [Alpinon_train]
    df_train.loc[(df_train.corpus == 'SNK') & (df_train.genre == 'fiction'), 'sentences'] = [SNKfic_train]
    df_train.loc[(df_train.corpus == 'SynTagRus') & (df_train.genre == 'nonfiction_prose'), 'sentences'] = [
        SNTRusnewsnonfico_train]
    df_train.loc[(df_train.corpus == 'SynTagRus') & (df_train.genre == 'news'), 'sentences'] = [SNTRusnews_train]
    df_train.loc[(df_train.corpus == 'CSUI') & (df_train.genre == 'news'), 'sentences'] = [Indo_train]
    df_train.loc[(df_train.corpus == 'SST') & (df_train.genre == 'spoken'), 'sentences'] = [SST_train]
    df_train.loc[(df_train.corpus == 'SNK') & (df_train.genre == 'wiki'), 'sentences'] = [sk_wiki_train]

    # Assign data to dev
    assign_data_to_df(df_dev, TaigaQA_dev, 'Taiga', 'QA')
    assign_data_to_df(df_dev, Taigareviews_dev, 'Taiga', 'reviews')
    assign_data_to_df(df_dev, lt_dev, 'ALKSNIS', 'academic')
    assign_data_to_df(df_dev, Alpinoqa_dev, 'Alpino', 'QA')
    assign_data_to_df(df_dev, Alpinon_dev, 'Alpino', 'news')
    assign_data_to_df(df_dev, SNTRusnews_dev, 'SynTagRus', 'news')
    assign_data_to_df(df_dev, SNTRusnewsnonfico_dev, 'SynTagRus', 'nonfiction_prose')
    assign_data_to_df(df_dev, Indo_dev, 'CSUI', 'news')
    assign_data_to_df(df_dev, SST_dev, 'SST', 'spoken')
    assign_data_to_df(df_dev, SNKfic_dev, 'SNK', 'fiction')
    assign_data_to_df(df_dev, sk_wiki_dev, 'SNK', 'wiki')

    # Create and populate UD-multigenre folder
    df_train.apply(lambda df: create_dataset(df), axis=1)


if __name__ == '__main__':
    main()
