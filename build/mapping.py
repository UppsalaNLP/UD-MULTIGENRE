#!/usr/bin/python3
from collections import defaultdict


##################
# create mapping #
##################

map_lang = defaultdict(dict)

map_lang['Italian']['TWITTIRO'] = {'social' : []}
map_lang['Italian']['PoSTWITA'] = {'social' : []}
map_lang['Italian']['ISDT'] = {'news' : ['sent_id = 2Parole', 'sent_id = isst_tanl'], 
                               'parliament' : ['sent_id = 2_Europarl'],
                              'QA' : ['sent_id = quest'], 
                               'wiki' : ['sent_id = .*WIKI'], 
                               'legal' : ['sent_id = splet']
                              }
map_lang['Italian']['ParlaMint'] = {'parliament' : []}
map_lang['Italian']['MarkIT'] = {'learner_essays' : []}
###############
map_lang['English']['GUMReddit'] = {'social' : []}
map_lang['English']['Tweebank'] = {'social' : []} 
map_lang['English']['EWT'] = {'social' : ['sent_id = newsgroup'],
                             'QA' : ['sent_id = answers'],
                             'reviews' : ['sent_id = reviews'],
                             'blog' : ['sent_id = weblog'],
                             'email' : ['sent_id = email']
                             }
map_lang['English']['GUM'] = {'news' : ['sent_id = GUM_news'], 
                              'fiction' : ['sent_id = GUM_fiction'],
                             'academic' : ['sent_id = GUM_academic'],
                            'nonfiction_prose' : ['newdoc id = GUM_bio'],
                             'parliament' : ['sent_id = GUM_speech'], 
                             'spoken' : ['sent_id = GUM_conversation'],
                             'guide' : ['sent_id = GUM_whow', 'sent_id = GUM_voyage'], 
                              'interview' : ['sent_id = GUM_interview'],
                              'textbook' : ['sent_id = GUM_textbook']
                             } 
map_lang['English']['Atis'] = {'spoken' : []}
map_lang['English']['LinES'] = {'fiction' : ['sent_id = .*doc[234678]'],
                               'parliament': ['sent_id = .*doc5']}
###############
map_lang['Estonian']['EDT'] = {'news' : ['sent_id = aja'],
                               'academic' : ['sent_id = tea'], 
                               'fiction' : ['sent_id = ilu']}
map_lang['Estonian']['EWT'] = {'social' : ['sent_id = .*foorum', 'sent_id = kom']}
###############
map_lang['Erzya']['JR'] = {
                           'nonfiction_prose': ['sent_id = NujanjVidjaz2007'],
                          'fiction': [
                              #train
                                'sent_id = Dunjashin',
                                'sent_id = Gluxov',
                                'sent_id = Kutorkin',
                                'sent_id = AuthorIDАбрамов',
                                'sent_id = AuthorIDAbramovK',
                                'sent_id = Erina',
                                'sent_id = GanchinA',
                                'sent_id = ProxorovP',
                                'sent_id = KutorkinA',
                                'sent_id = DoroninA',
                              #dev
                              'sent_id = Chetvergov',
                              'sent_id = Bryzhinskij',
                              'sent_id = Anoshkin'                         
                          ]}
###############
map_lang['Belarusian']['HSE'] = {'social' : ['genre = social'], 
                                 'news' : ['genre = news'],
                                 'nonfiction_prose' : ['sent_id = Narodnaja-proza-belarusau-Padzvinnja'], 
                                 'fiction' : ['genre = fiction'], 
                                 'wiki' : ['genre = wiki']}

###############
map_lang['Russian']['Taiga'] = {'social' : ['genre = social'],
                                'QA' : ['genre = QA'], 
                                'reviews' : ['genre = review']
                               }
#also modern poetry in Taiga
map_lang['Russian']['SynTagRus'] = {'news' : ['sent_id = newsYa'
                                             ], 
                                    'fiction' : ['genre = fiction',
                                                 'sent_id = uppsalaBitov'
                                                ],
                                   'academic' : [#train
                                                   'sent_id = 2020_Corpus2_0Kto_nasledil', #science: https://nplus1.ru/material/2020/09/17/trace
                                                   'sent_id = 2017Apresyan_1', #science: https://www.trv-science.ru/2017/02/yuri-apresyan-mathwalks/
                                                   'sent_id = .*Kriptografiya', #popular science journal, contains interview parts: https://poisknews.ru/magazine/15295/
                                                  #dev                                                    #dev
                                                   'sent_id = 2007Chuvstvo_spravedlivosti.xml', #https://www.nkj.ru/archive/articles/3387/ #Science and life, Article by Yu. Frolov, 
                                                   'sent_id = 2003Biologiya.xml', #https://zoom.cnews.ru/rnd/article/item/evolyutsionnaya_biologiya_i_vysokie_tehnologii_simbioz_budushchego
                                                   'sent_id = 2006Lunnye_kamni.xml', # https://www.nkj.ru/archive/articles/2418/ - Science & Life
                                                   'sent_id = 2017Chto_gubit_nauku.xml', #https://www.ras.ru/digest/showdnews.aspx?id=55f4524a-3bfd-4f33-bd73-5a8fa9cfc7a4&print=1, Russian Academy of Sciences
                                                   'sent_id = 2018Gorod-sad_Singapur.xml', #popular science, https://znanie-sila.su/themes/planetearth/gorod-sad-singapur
                                                   'sent_id = 2011Nano.xml', #https://hij.ru/read/661/, popular science journal "Chemistry and life"
                                                   'sent_id = 2011Radioastron.xml', #https://www.trv-science.ru/2011/07/mezhdu-proshlym-i-budushhim/
                                                   'sent_id = 2011Sverkhkorotkoe_vremya.xml', #https://www.techinsider.ru/science/7434-dyrokol-nestrashnye-chernye-dyrochki/
                                                   'sent_id = 2006Informtekhnologii.xml', #https://www.nkj.ru/archive/articles/2081/
                                                    ],
                                    
                                    'nonfiction_prose' : [
                                                 
                                                    #autobiographical narratives:
                                                    #train
                                                    'sent_id = 2020_Corpus2_0Kakie_nashi_gody', #https://znamlit.ru/publication.php?id=7536 memoires of Anna Rodionova
                                                    'sent_id = 2020_RFFIIndoneziya_ot_ada_do_raya.xml_700', #http://www.nm1925.ru/Archive/Journal6_2019_3/Content/Publication6_7138/Default.aspx 
                                                    'sent_id = 2020_Corpus2_0Velikoe_pereselenie', #https://www.vestnik-evropy.ru/issues/night-the-great-migration.htmljournal: "Vestnik Evropy", literature, politics, philosophy,culture
                                                    'sent_id = 2018V_strane_mormonov.xml', #https://magazines.gorky.media/druzhba/2017/12/moya-amerika-zhizn-v-strane-mormonov.html
                                                    'sent_id = 2019Lingvistika_i_morzhevanie.xml' #https://snob.ru/profile/28809/blog/85851/
                                                    #dev
                                                    'sent_id = 2003A_on_myatezhnyi.xml'#https://www.nkj.ru/archive/articles/2542/
                                                    'sent_id = 2007Chelovek_na_tribune.xml'#biography of Roman Abramovich
                                                         ],
                                    'interview' : ['sent_id = .*Interviyu'],
                                    'wiki' : ['genre = wiki', 
                                              'sent_id = 2013Algoritm.xml', #https://ru.wikipedia.org/wiki/Алгоритм
                                              'sent_id = 2012Galileo_Galilei.xml'#https://ru.wikipedia.org/wiki/Галилей,_Галилео                                                      }
                                             ]
                                    
                                   }


map_lang['Russian']['GSD'] = {'wiki' : []}
###############
map_lang['Hindi']['HDTB'] = {'news' : []}
###############
map_lang['Turkish']['BOUN'] = {'news' : ['sent_id = news'], 
                               'guide' : ['sent_id = ins'], #contains sentences from a recipe and some nonfiction
                               'nonfiction_prose' : ['sent_id = bio',#biographies
                                                    'sent_id = ess'#essays
                                                    ]}
map_lang['Turkish']['Tourism'] = {'reviews' : []}
map_lang['Turkish']['Atis'] = {'spoken' : []}
#######################
map_lang['Western Armenian']['ArmTDP'] = {'nonfiction_prose' : ['sent_id = nonfiction-002I',
                                                               ],#https://inknagir.org/?author=13 #'sent_id = nonfiction-(?!002I)'
                                          
                                          #dev
                                          'academic':['sent_id = nonfiction-0009'],#https://www.academia.edu/40230759/Նեմեսիս_Շահան_Նաթալի_Թուրքերը_եւ_մենք_Վերագնահատումներ_Հրատարակիչ_Հայրենիք_Ակումբ_Երեւան_2011
                                          
                                          'news' : ['sent_id = news'], #https://www.civilnet.am/news
                                         'fiction' : ['sent_id = fiction'], 
                                          'blog' : ['sent_id = blog'],#https://hayerenblog.wordpress.com/2021/12/23/%D5%A1%D6%82%D5%BD%D5%BF%D6%80%D5%AB%D5%B8%D5%B5-%D5%B4%D5%A7%D5%BB-%D5%B0%D5%AB%D5%B6%D5%A3-%D5%A1%D5%B4%D5%AB%D5%BD-%D5%AA%D5%A2/
                                          #https://darperag21.net/%D5%B6%D5%A5%D6%80%D5%A3%D5%A1%D5%B2%D5%A9%D5%B6-%D5%A7-%D5%B8%D6%80-%D5%A9%D5%A7%D5%9B-%D5%A1%D6%80%D5%BF%D5%A1%D5%BD%D5%A1%D5%B0%D5%B4%D5%A1%D5%B6%D5%AB-%D5%BF%D5%A1%D6%80%D5%BF%D5%B2%D5%B6%D5%B8/
                                          'reviews':['sent_id = reviews'],
                                          'social' : ['sent_id = social'], 
                                          'wiki' : ['sent_id = wiki'],
                                          'spoken' : ['sent_id = spoken']
                                         }
map_lang['Armenian']['ArmTDP'] = {
                                'nonfiction_prose':['sent_id = nonfiction-005F',
                                                    #dev
                                                    'sent_id = nonfiction-006Q',#- reflective prose. It discusses the concept of youthfulness and responsibility                                     
                                                   ], #https://hrantmatevossian.org/hy/works/id/i-skzbane-er-bann autobiographical
                                'blog':['sent_id = blog','sent_id = nonfiction-006U'],#https://manukyanmarianna.wordpress.com/2021/11/18/համբերություն-քեզ-մարդ-ջան-գուրգեն-խ/
                                 'fiction':['sent_id = fiction'],
                                 'news':['sent_id = news'], #golosarmenii.am
                                 'legal':['sent_id = legal'],
    
                                 }
#test - https://www.grakantert.am/archives/6614 - fiction
map_lang['Armenian']['BSUT'] = {'nonfiction_prose' : ['sent_id = nonfiction'], #dev https://granish.org/qnarakan-poemi-herosy/ - biographical narrative
                                
                                #dev
                                'blog':['sent_id = blog'],
                                 'fiction':['sent_id = fiction'],
                                 'news':['sent_id = news'],
                                 'legal':['sent_id = legal', 'sent_id = government'],
                               'wiki' : ['sent_id = wiki']}
#nonfiction test: literary survey https://granish.org/anmoruuki-pakuughi/
###############
map_lang['Dutch']['LassySmall'] = {'wiki' : []}
map_lang['Dutch']['Alpino'] = {'news' : ['sent_id = cdb'],
                              'QA' : ['sent_id = qa', 'sent_id = wpspel']}
#sent_id = WR-P-P-H: dev and train-periodicals and magazines
# http://nederbooms.ccl.kuleuven.be/eng/lassytb
###############
map_lang['Slovenian']['SSJ'] = {'wiki' : ['sent_id = .*sl']}
map_lang['Slovenian']['SST'] = {'spoken' : []}
###############
map_lang['French']['Sequoia'] = {'wiki' : ['sent_id = frwiki'],
                                'academic' : ['sent_id = emea-fr'], #a mix of guide and academic
                                'parliament' : ['sent_id = Europar'],
                                'news' : ['sent_id = annodis.er']}
map_lang['French']['Rhapsodie'] = {'spoken' : []}
map_lang['French']['ParisStories'] = {'spoken' : []}
###############
# code-switch
map_lang['Turkish German']['SAGT'] = {'spoken' : []}
#map_lang['Hindi English']['HIENCS'] = {'social' : []}
###############
map_lang['Naija']['NSC'] = {'spoken' : []}
###############
map_lang['Norwegian']['NynorskLIA'] = {'spoken' : []}
###############
map_lang['Finnish']['TDT'] = {'wiki' : ['sent_id = w\d+'],
                             'news' : ['sent_id = wn\d+'],
                             'legal' : ['sent_id = j'],
                             'blog' : ['sent_id = b'],
                             'fiction' : ['sent_id = f'],
                             'parliament' : ['sent_id = e']}
###############
map_lang['Slovak']['SNK'] = {#'blog' : ['sent_id = blogsme'],
                             'fiction' : ['sent_id = rozpravky',
                                         'sent_id = orwell',
                                         'sent_id = mojaprvalaska',
                                         'sent_id = psiakoza',
                                         'sent_id = milosferko'],
                             'legal' : ['sent_id = programvyhlasenie'],#goverment
                             # 'nonfiction_religious' : ['sent_id = patmos'], #religious #https://patmos.sk/
                             'news' : ['sent_id = inzine', 'sent_id = sme' ],#news https://sk.wikipedia.org/wiki/InZine, sme.sk 
                             'wiki' : ['sent_id = wikipedia']
} 
###############
map_lang['Czech']['CAC'] = {
    'legal' : ['sent_id = a'],#administrative
    'news' : ['sent_id = n'], #newspapers
    'academic' : ['sent_id = s']}
# the "s20w" part identifies the source document, where "w" means "written", "20" is the document id number and "s" means scientific (while "a20w" is the twentieth document from the administrative genre, and "n20w" from newspapers).
map_lang['Czech']['PDT'] = {
    'news' : ['sent_id = l', 'sent_id = m'],
    'academic' : ['sent_id = v']#popular scientific articles
    #,l (ln) and m (mf) are mainstream daily papers (news, commentaries, but also
  #sports results and TV programs) #c (cmpr) is a business weekly #v #(vesm) contains popular scientific articles (the hardest to parse: long
}
map_lang['Czech']['FicTree'] = {'fiction' : []}
###############
map_lang['Polish']['LFG'] = {'social' : ['genre = social'],
                            'news' : ['genre = news'],
                            'fiction' : ['genre = fiction'],
                             'academic' : ['genre = academic'],
                             'spoken' :['genre = spoken']
                            }
# LFG About 42.1% of sentences represent the fiction genre, 39.1% – news, 7.4% – nonfiction, 7.3% – spoken, 3% – interactive Internet texts (forums, chatrooms, etc.), and there are also traces of static Internet pages (0.8%), academic style (0.3%) and legal texts (0.1%). For each sentence, genre is explicitly given in a comment to this sentence.
###############
map_lang['Bulgarian']['BTB'] = {'fiction' : ['sent_id = bg-lit', 'sent_id = for-lit', 'sent_id = kamu'],
                               'legal' : ['sent_id = constitution'],
                               'academic' : ['sent_id = kleinke', 'sent_id = euro'],
                                'nonfiction_prose' : ['sent_id = girl'],
                                'news' : ['sent_id = Novinar', 'sent_id = Sega', 'sent_id = president'],
                               'interview' : ['sent_id = Standard']#mix of interview and news
                                }                               
###############
map_lang['Catalan']['AnCora'] = {'news' : []}
# EFE (75,000) ACN (225,000) El Periódico: (200,000)
###############
map_lang['Croatian']['SET'] = {'news' : ['sent_id = news', 'sent_id = set']
                              }
# SET Times news
###############
map_lang['Portuguese']['PetroGold'] = {'academic' : []}
#academic texts from the oil & gas domain in Brazilian Portuguese processed in full: only elements such as summary, abstract, appendices and bibliographic references were excluded, as well as figures, graphs, formulas and tables. 
###############
map_lang['Romanian']['RRT'] = {'legal' : ['newdoc id = Acquis', 'newdoc id = JRC'],
                               'news' : ['newdoc id = Agenda'],
                               'fiction' : ['newdoc id = 1984Orwell',
                                            'newdoc id = Literatura'],
                               'academic' : ['newdoc id = PhysicsCompSciMath',
                                              'newdoc id = DGLR', 
                                             'newdoc id = EMEA'],#mix of academic and guide
                               'wiki' : ['newdoc id = Wikipedia']
                               
}
map_lang['Romanian']['SiMoNERo'] = {'academic' : []}
###############
map_lang['German']['GSD'] = {'reviews' : []}
# train: Reviews=s1-s1500, News=s1501-s2200, Web=s2201-s14118 
# By searching for a selection of sentences in the s2201-s14118 
# range, i.e. the new ones in version 2.0, 
# it looks like they are from Wikipedia and 
# other websites. dev: Reviews=s1-s500, News=s501-s799 
# test: Reviews=s1-s301, News=s302-s977
map_lang['German']['HDT'] = {'news' : []}
#The content of the articles ranges from formulaic periodic updates on new BIOS revisions and processor models or quarterly earnings of tech companies over features about general trends in the hardware and software market to general coverage of social, legal and political issues in cyberspace, sometimes in the form of extensive weekly editorial comments. 
###############
map_lang['Greek']['GDT'] = {'news' : ['sent_id = .*elwikinews'],
                            'parliament' : ['sent_id = .*ep-sessions']}
###############
map_lang['Hebrew']['HTB'] = {'news' : []} #`Ha'aretz` newspaper
map_lang['Hebrew']['IAHLTwiki'] = {'wiki' : []}
###############
map_lang['Icelandic']['Modern'] = {'parliament' : ['sent_id = ALTHINGI'], #speeches
                                   'news' : ['sent_id = RUV']}#sports
###############
map_lang['Indonesian']['CSUI'] = {'news' : []}
# news in formal Indonesian (the majority is economic news)
###############
# news nonfiction legal scientific
map_lang['Lithuanian']['ALKSNIS'] = {'academic' : ['sent_id = .*rec', 'sent_id = mok_santr'],
                                     'legal' : [
                                             #train
                                             'sent_id = Veiklos_ataskaita', 
                                            'sent_id = 2005_daugiabuciu',
                                            'sent_id = Smulkiojo_ir_vidutinio', 
                                            'sent_id = Nutarimas_kulturos_politikos',
                                            #dev
                                            'send_id = 2004_AM_Isak', 'sent_id = 2009_komunikatas'],
                                     'news' : ['sent_id = kd'],
                                
                                    'fiction' : ['sent_id = Navakas', 'sent_id = Katkus', 'sent_id = Parulskis', 'sent_id = Jonuskaite',
                                                #dev
                                                 'sent_id = Serelyte'
                                                ]
                                    }
###############
map_lang['Scottish Gaelic']['ARCOSG'] = {'fiction' : ['sent_id = f0'],
                                        'news' : ['sent_id = ns'],
                                        'spoken' : ['sent_id = c', 'sent_id = n\d'],
                                        'interview' : ['sent_id = p\d']
                                        }
###############
map_lang['Chinese']['GSD'] = {'wiki' : []}
###############
map_lang['Maltese']['MUDT'] = {'fiction' : ['sent_id = .*F'],
                               'parliament': ['sent_id = .*P']} #also newspaper interviews
#J NEWS annotation includes op-eds, opinion-based articles
#nonfiction N also includes blogs, wikipedia, which we consider separate genres
###############
map_lang['Uyghur']['UDT'] = {'fiction' : []}
# The sentences come from literature texts / 
# reading material for primary and middle school, 
# including stories, records and reports.
###############
map_lang['Swedish']['LinES'] = {'fiction' : ['sent_id = .*doc[234678]'],
                               'parliament': ['sent_id = .*doc5']}
###############
map_lang['Afrikaans']['AfriBooms'] = {'legal': []}
###############
