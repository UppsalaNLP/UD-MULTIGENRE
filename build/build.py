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


def load_f(fname):
    with open(fname, 'rb') as inp:
        return pickle.load(inp)


def create_data_df(data_dict: dict) -> pd.DataFrame:
    """Creates a pandas DataFrame from a nested dictionary of data."""
    df_data = []
    for language, lang_data in data_dict.items():
        for corpus, corpus_data in lang_data.items():
            for genre, sentences in corpus_data.items():
                df_data.append([language, corpus, genre, sentences])
    return pd.DataFrame(df_data, columns=['language', 'corpus', 'genre', 'sentences'])

def filter_sentences_by_regex(sentences, regex_list):
    """Filters sentences based on comments matching a list of regex patterns."""
    if not regex_list:
        return sentences
    
    filtered_sentences = []
    for sentence in sentences:
        for comment in sentence.get_comments():
            for regex in regex_list:
                if re.match(regex, comment):
                    filtered_sentences.append(sentence)
                    break
    return filtered_sentences

def extract_instances(tb, lang, name):
    """Extracts sentences and groups them by genre using mapping rules."""
    genre_group = defaultdict(list)
    sentences = tb.get_sentences()

    if lang == 'Romanian' and name == 'RRT':
        # 'newdoc_id' at the start of each document containing multiple sentences; this part 
        # identifies the segments separated by 'newdoc_id'

        tpls = [(sentences.index(sentence), comment) for sentence in sentences for comment in sentence.get_comments() if 'newdoc id' in comment]
        for genre, regex_list in map_lang[lang][name].items():
            for regex in regex_list:
                try:
                    start_obj = next(obj for obj in tpls if regex in obj[1])
                    start_id = tpls.index(start_obj)
                    end_id = next((i for i, obj in enumerate(tpls[start_id+1:]) if regex not in obj[1]), len(tpls)) + start_id +1
                    end_idx = tpls[end_id][0] if end_id < len(tpls) else len(sentences)

                    group = sentences[start_obj[0]:end_idx]
                    genre_group[genre].extend(group)
                except StopIteration:
                    continue
    else:
        for genre, regex_list in map_lang[lang][name].items():
            genre_group[genre].extend(filter_sentences_by_regex(sentences, regex_list))

    return genre_group


def write_files(sentences: list, ftxt: str, fconllu: str):
    """Writes sentence data to .txt and .conllu files."""
    if not sentences:
        return
        
    with open(fconllu, 'w', encoding='utf-8') as f_conllu, open(ftxt, 'w', encoding='utf-8') as f_txt:
        for sent in sentences:
            # Write text file
            f_txt.write(sent.to_text() + '\n')
            
            # Write CoNLL-U file
            conllu_output = '\n'.join(sent._comments) + '\n' if sent._comments else ''
            conllu_tok_seq = []
            for tok in sent._tokens:
                for w in tok._words:
                    if w.head is None:
                        w.head = '_'
                conllu_tok_seq.append(tok.to_conllu())
            
            f_conllu.write(conllu_output + '\n'.join(conllu_tok_seq) + '\n\n')


def main():

    logger.info('Prepares for loading UD data ...')
    args = parse_arguments()

    # check if UD  data folder exists
    if not os.path.exists(args.ud_path):
        print(
            r"[Error] Please introduce a valid UD folder path and try again. Could not find the path '{args.ud_path}'")
        exit(1)

    # Initialize Data Dicts
    training_data = defaultdict(lambda: defaultdict(dict))
    dev_data = defaultdict(lambda: defaultdict(dict))
    
    # Load pre-processed Nynorsk data
    ny_data_path = 'Nynorsk_data'
    training_data['Norwegian']['Nynorsk'] = {
        'blog': load_f(os.path.join(ny_data_path, 'Nynorsk_blog_train.pkl')),
        'parliament': load_f(os.path.join(ny_data_path, 'Nynorsk_parl_train.pkl')),
        'legal': load_f(os.path.join(ny_data_path, 'Nynorsk_legal_train.pkl')),
        'news': load_f(os.path.join(ny_data_path, 'Nynorsk_news_train.pkl'))
    }
    dev_data['Norwegian']['Nynorsk'] = {
        'blog': load_f(os.path.join(ny_data_path, 'Nynorsk_blog_dev.pkl')),
        'parliament': load_f(os.path.join(ny_data_path, 'Nynorsk_parl_dev.pkl')),
        'legal': load_f(os.path.join(ny_data_path, 'Nynorsk_legal_dev.pkl')),
        'news': load_f(os.path.join(ny_data_path, 'Nynorsk_news_dev.pkl'))
    }
    logger.info('Nynorsk data loaded successfully.')

    # Load treebanks
    ud_path = args.ud_path
    ud = UniversalDependencies.from_directory(ud_path, ud_filter=None, verbose=True)
    logger.info('UD data loaded successfully')

    # Populate training and development data dicts
    for tb in ud.get_treebanks():

        lang, name = tb.get_language(), tb.get_treebank_name()
        lang = '_'.join(lang.split())
        
        # Determine if the treebank is train, dev, or test split
        tb_split = 'dev' if 'dev' in tb.get_name() else 'test' if 'test' in tb.get_name() else 'train'
        
        # Skip Nynorsk as it's already loaded
        if lang == 'Norwegian' and name == 'Nynorsk':
            continue

        # Handle German GSD manually
        if lang == 'German' and name == 'GSD':
            filtered_sents = []
            if tb_split == 'train':
                for s in tb.get_sentences():
                    match = re.search(r'sent_id = train-s(\d+)', '\n'.join(s.get_comments()))
                    if match and int(match.group(1)) <= 1500:
                        filtered_sents.append(s)
                training_data[lang][name]['reviews'] = filtered_sents
            elif tb_split == 'dev':
                for s in tb.get_sentences():
                    match = re.search(r'sent_id = dev-s(\d+)', '\n'.join(s.get_comments()))
                    if match and int(match.group(1)) <= 500:
                        filtered_sents.append(s)
                dev_data[lang][name]['reviews'] = filtered_sents

        # Other tbs with patterns available
        if (lang in map_lang) & (name in map_lang[lang]):
            if tb_split == 'train':
                training_data[lang][name] = extract_instances(tb, lang, name)

            elif tb_split == 'dev':
                dev_data[lang][name] = extract_instances(tb, lang, name)

            # Cases where we don't have sufficient training/development data for dev
            # too few samples in train, so we include test
            if lang == 'Italian' and name == 'ParlaMint' and tb_split == 'test':
                dev_data[lang][name] = {'parliament': tb.get_sentences()}

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
    # Configuration for corpora that need re-splitting from the training set
    # Configuration for corpora that need re-splitting from the training set
    resplit_config = [
        ('ALKSNIS', 'academic', 0.2), ('Taiga', 'reviews', 0.2), ('Taiga', 'QA', 0.2),
        ('Alpino', 'QA', 0.2), ('Alpino', 'news', 0.2), ('SNK', 'fiction', 0.2),
        ('CSUI', 'news', 0.2), ('SST', 'spoken', 0.2), ('SynTagRus', 'news', 0.2),
        ('SynTagRus', 'nonfiction_prose', 0.2), ('SNK', 'wiki', 0.1)
    ]

    for corpus, genre, test_size in resplit_config:

        if (corpus == 'SNK') & (genre == 'wiki'):
            df_train_sentences = df_dev[(df_dev.corpus == 'SNK') & (df_dev.genre == 'wiki')].sentences.tolist()[0]
            train_sents, dev_sents = train_test_split(df_train_sentences, test_size=test_size, random_state=42)
        else:
            df_train_sentences = df_train[(df_train.corpus == corpus) & (df_train.genre == genre)].sentences.tolist()[0]
            train_sents, dev_sents = train_test_split(df_train_sentences, test_size=test_size, random_state=42)
            
        df_train.loc[(df_train.corpus == corpus) & (df_train.genre == genre), 'sentences'] = [train_sents]
        df_dev.loc[(df_dev.corpus == corpus) & (df_dev.genre == genre), 'sentences'] = [dev_sents]

    # * Write Files *
    UD_folder = 'UD-multigenre'
    logger.info(f"Writing files to '{UD_folder}' folder...")

    for _, train_row in df_train.iterrows():
        lang, corpus, genre = train_row['language'], train_row['corpus'], train_row['genre']
        train_sents = train_row['sentences']

        # Define output paths
        output_path = os.path.join(UD_folder, genre, f'UD_{lang}-{corpus}')
        os.makedirs(output_path, exist_ok=True)

        # Write training files
        write_files(train_sents,
                    os.path.join(output_path, f'{genre}-train.txt'),
                    os.path.join(output_path, f'{genre}-train.conllu'))

        # Find and write corresponding development files
        dev_row = df_dev[(df_dev.language == lang) & (df_dev.corpus == corpus) & (df_dev.genre == genre)]
        if not dev_row.empty:
            dev_sents = dev_row['sentences'].iloc[0]
            write_files(dev_sents,
                        os.path.join(output_path, f'{genre}-dev.txt'),
                        os.path.join(output_path, f'{genre}-dev.conllu'))

    logger.info('All files written successfully.')


if __name__ == '__main__':

    main()
