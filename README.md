# UD-MULTIGENRE
A dataset of instance-level text genre annotations from the paper:

[**"UD-MULTIGENRE - a UD-based dataset of instance-level genre annotations"**](https://aclanthology.org/2023.mrl-1.19/) (Danilova & Stymne, MRL-WS EMNLP 2023)

It is a reorganization of 63 treebanks from UD version 2.11 [Universal Dependencies](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-4923). It currently covers 17 text genres in 38 languages. The total size of the dataset (training and development) in tokens is 11096.9k, and in sentences - 657.4k. In addition, the test set currently includes data from 17 treebanks for five genres and 14 low-resource languages (119k tokens and 7.2k sentences).

The dataset enables new research as well as re-evaluation and a deeper understanding of prior research on genre-based data selection for cross-lingual dependency parsing. In addition, it is highly relevant for the research direction that investigates cross-lingual genre representation and classification.

The repository contains the following data: 
- **train:dev** Under each genre-specific directory, you'll find a list of treebank folders with the corresponding training and development .conllu and .txt files
- **test** In each genre-specific directory, you'll find a list of treebank folders with test data in .conllu and .txt formats
- **genre_prefix_map.json** This file stores the details on the identified sources for each prefix pattern. It has the following levels:
     * **Level-1:** Genre
     * **Level-2:** Language
     * **Level-3:** Treebank name
     * **Level-4:** Prefix patterns accompanied with descriptions and source where possible:
```
{
    "QA": {
        "Dutch": {
            "Alpino": {
                "sent_id = qa": "questions  used in a QA project (source)[https://github.com/UniversalDependencies/UD_Dutch-Alpino/tree/master]",
                "sent_id = wpspel": "questions  used in a QA project (source)[https://github.com/UniversalDependencies/UD_Dutch-Alpino/tree/master]"
            }
        },
        "English": {
            "EWT": {
                "sent_id = answers": "Question-answers are posts from Yahoo!s community-driven question-answering web site, Yahoo! Answers, where individuals submit and answer questions which may be on any topic. This data was collected in 2011 (source)[https://catalog.ldc.upenn.edu/LDC2012T13]"
            }
        },
...
```
**nopattern** value of prefix pattern is used for single-genre treebanks where the whole treebank is assigned to a specific genre.


## Genre selection criteria

| Genre            | In UD        | Criteria                                                                                                      |
|------------------|--------------|----------------------------------------------------------------------------------------------------------------|
| academic         | ✔            | Scientific articles and reports from different fields (medicine, oil and gas, humanities, computer science), and popular science articles |
| blog             | ✔            | Texts proceeding from blogging platforms like WordPress                                                        |
| email            | ✔            | Email messages                                                                                                |
| fiction          | ✔            | Fiction novels, stories, fairy tales. Documentation and patterns tend to include author or story names         |
| guide            |              | Wikihow, travel guides, instructions                                                                          |
| interviews       |              | Prepared interviews with celebrities, politicians, and businessmen                                            |
| learner\_essays  | ✔            | Essays of language learners on different topics that tend to contain grammar errors                            |
| legal            | ✔            | Legal and administrative texts, including texts from governmental websites                                     |
| news             | ✔            | Mainstream daily (online) news, Wikinews. We stick to short articles and exclude long-read newspaper articles since they often belong to popular science |
| nonfiction\_prose |            | Documentary prose, biographies, autobiographical narratives, memoirs, essays                                   |
| parliament       |              | Transcriptions of parliamentary speeches and debates                                                           |
| QA               |              | Data from Question Answering competitions                                                                     |
| reviews          | ✔            | Messages containing reviews and opinions                                                                      |
| social           | ✔            | Informal social media posts and discussions (e.g., Twitter, Telegram, Reddit, forum messages, and comments, etc.) |
| spoken           | ✔            | Transcriptions of spontaneous spoken speech: monologues and conversations                                     |
| textbook         |              | Educational literature, textbooks                                                                              |
| wiki             | ✔            | Main Wikipedia articles. Wikihow, Wikinews, Wikitravel, and Wikianswers are not considered in this category    |

## References

Vera Danilova and Sara Stymne. 2023. UD-MULTIGENRE – a UD-Based Dataset Enriched with Instance-Level Genre Annotations. In Proceedings of the 3rd Workshop on Multi-lingual Representation Learning (MRL), pages 253–267, Singapore. Association for Computational Linguistics.
