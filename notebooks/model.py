import pandas as pd
import numpy as np
import pickle
# from tqdm.notebook import tqdm


import string # библиотека для работы со строками
import nltk   # Natural Language Toolkit
# загружаем библиотеку для лемматизации
import pymorphy2 # Морфологический анализатор

#вычисляем tf-idf
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Binarizer

from data_types import AuthorsDB
from data_types import PublicationsDB
from data_types import AbstractsDB
from collections import defaultdict


def get_authors_rating(df, coef):
    rating = defaultdict(int)
    
    for index in range(len(df)):
        # print(f'index = {index}, row = {df.iloc[index]}')        
        for author in df.iloc[index]['author_id']:  
            # print(index)          
            # print(f'add coef = {coef[index]} to author = {author}')
            rating[author] += coef[index]            
            # print(rating)
    # dict(sorted(rating.items(), key=lambda item: item[1]))
    rating_list = [ (k,v) for k, v in sorted(rating.items(), key=lambda item: item[1], reverse=True)]
    return rating_list



class Model():
    
    def __init__(self, path='../data/'):        
        self.path = path
        # print("self.path = ", self.path)
        self.audb = AuthorsDB(path)
        self.audb.load()
        pubdb = PublicationsDB(path)
        pubdb.load()
        self.pub = pd.DataFrame.from_dict(pubdb.db,orient='index')
        self.absdb = AbstractsDB(path)
        self.absdb.load()
        self.abstracts = self.absdb.db[self.absdb.db['abstract'].notna()].copy()
                
        self.vectorizer_uni = self.load_vectorizer('vectorizer_uni')
        self.vectorizer_bi = self.load_vectorizer('vectorizer_bi')
        self.vectorizer_tri = self.load_vectorizer('vectorizer_tri')
        
        self.tf_idf_matrix_uni = self.load_tf_idf_matrix('tf_idf_matrix_uni')
        self.tf_idf_matrix_bi = self.load_tf_idf_matrix('tf_idf_matrix_bi')
        self.tf_idf_matrix_tri = self.load_tf_idf_matrix('tf_idf_matrix_tri')
        
        self.authors_dict = None
        self.load_authors_dict()
        
        # filename = "../data/mathnet_iam_authors_dict.pkl"
        # with open(filename,'rb') as inp:
        #     authors_dict = pickle.load(inp)
        stop_words_filename = path+'ru_stop_words.pkl'
        # nltk.download('stopwords')
        # self.stop_words = nltk.corpus.stopwords.words('russian')
        stop_words = ['']
        with open(stop_words_filename,'rb') as inp:
            stop_words = pickle.load(inp)
        self.stop_words = stop_words
        self.word_tokenizer = nltk.WordPunctTokenizer()
        self.morph = pymorphy2.MorphAnalyzer()
            
        
    def load_vectorizer(self,name):        
        filename_vec = self.path + name+'.pkl'
        with open(filename_vec,'rb') as inp:
            vectorizer = pickle.load(inp)         
        return vectorizer

    def load_tf_idf_matrix(self,name):            
        filename_tf_idf = self.path + name+'.pkl'
        with open(filename_tf_idf,'rb') as inp:
            tf_idf_matrix = pickle.load(inp)         
        return tf_idf_matrix
        
    def load_authors_dict(self):
        filename = self.path + "mnid_author_dict.pkl"
        with open(filename,'rb') as inp:            
            self.authors_dict = pickle.load(inp)
            
    def process_request(self, data):        
        text_lower = data.lower()
        tokens = self.word_tokenizer.tokenize(text_lower)
        tokens = [word for word in tokens if (word not in string.punctuation and word not in self.stop_words and not word.isnumeric())]        
        texts = ' '.join(tokens)         
        return [self.morph.parse(texts)[0].normal_form]
            
    def get_model_response(self, request):
        max_number_of_articles = 30
        low_bound = 0.01
        max_output_pubs = 5
        max_output_authors = 5
        
        # request = self.process_request(request)
        request = self.process_request(request)
        print('request = ', request)    
        vect_req_uni = self.vectorizer_uni.transform(request)
        vect_req_bi = self.vectorizer_bi.transform(request)
        vect_req_tri = self.vectorizer_tri.transform(request)
        
        onehot = Binarizer()
        ohe_request_uni = onehot.fit_transform(vect_req_uni.toarray())    
        ohe_request_bi = onehot.fit_transform(vect_req_bi.toarray())    
        ohe_request_tri = onehot.fit_transform(vect_req_tri.toarray())    
        
        coef_uni = (self.tf_idf_matrix_uni.dot(ohe_request_uni.T)).flatten()
        coef_bi = (self.tf_idf_matrix_bi.dot(ohe_request_bi.T)).flatten()
        coef_tri = (self.tf_idf_matrix_tri.dot(ohe_request_tri.T)).flatten()

        coef = coef_uni + coef_bi + coef_tri        
                
        # print(vect_req_uni)        
        # print(np.sort(ohe_request_uni[0])[::-1][:10])
        # index_cu = np.argsort(ohe_request_uni[0])[::-1][:10]
        # print('index_cu= ',index_cu)        
        # print(self.vectorizer_uni.get_feature_names_out()[index_cu])
        
        # print(vect_req_bi)        
        # print(np.sort(ohe_request_bi[0])[::-1][:10])
        # index_cb = np.argsort(ohe_request_bi[0])[::-1][:10]
        # print('index_cb= ',index_cb)        
        # print(self.vectorizer_bi.get_feature_names_out()[index_cb])
        
        # print(vect_req_tri)        
        # print(np.sort(ohe_request_tri[0])[::-1][:10])
        # index_ct = np.argsort(ohe_request_tri[0])[::-1][:10]
        # print('index_ct= ',index_ct) 
        # print(self.vectorizer_tri.get_feature_names_out()[index_ct])
        pubs_index = np.argsort(coef)[::-1][:max_number_of_articles]        
        low_bound_pub_index  = [ind for ind in pubs_index if coef[ind]>low_bound]
        req_pups = list(self.abstracts.iloc[low_bound_pub_index].index)    
        top_pubs = self.pub.loc[req_pups]['reference']
        top_autors = get_authors_rating(self.pub.loc[req_pups],coef[pubs_index])
            
        index = 0
        answer = []
        for item in top_autors:        
            if index >= max_output_authors:
                break
            if item[0] in self.authors_dict:
                index +=1
                answer.append(f'Expert: {self.authors_dict[item[0]]}, rating: {round(item[1],2)}\n')    
        if len(answer)>0:        
            answer.append('-----------\n')
            answer.append('Список работ с наибольшим рейтингом:\n')
            for item in top_pubs[:max_output_pubs]:
                answer.append(item+'\n') 
        else: 
            answer.append('Не обнаружено публикаций с такими словами в аннотации')
        
        answer = ''.join(answer)            
        # print(type(answer))                
        return answer
    
    def get_authors_last_papers(self, surname):
        output = ['']
        surname = surname.strip('.,? ')
        # regex = surname+'\s'        
        findme = surname + ' '
        
        for id,name in self.authors_dict.items():            
            if findme not in name:
                continue
            else:                
                # result = re.match(regex,name)
                # print(output)
                # print(findme)
                # print(ascii(findme))                
                result = name.find(findme)
                # print(result)
                # if result is not None: 
                if result>-1:
                    if output[-1] != '':
                        output.append(' ---|- -|-|- -|--- \n')
                                                 
                    output.append(f"На данный момент у автора: {name} учтено {len(self.audb.db[id])} статьи. Вот некоторые из них:\n")        
                    local_res = [(k,v) for k, v in sorted(self.audb.db[id].items(), key=lambda item: item[1]['year'],reverse=True)]
                       # print(mod.audb.db[k][item]['year'])
                    for item in local_res[:5]:
                        print(item[0])
                        output.append(self.pub.loc[item[0]]['reference']+'\n')
        print("len(output) = ",len(output))
        if len(output) == 1:
            output = [f'Не удалось найти автора по фамилии: {surname}']
        return ''.join(output)