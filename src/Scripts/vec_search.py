##### Takes a search query as input and get the vectors from the whole dataset to compare.
import spacy
import pickle
import numpy as np
from scipy import spatial
import sys
import unidecode
#from sklearn.decomposition import PCA
#QUERY  Neighbours Ids_and_Score_bool
directory='../'
argv=sys.argv
nlp = spacy.load("fr_core_news_lg")
pca = pickle.load(open(directory+'models/pca_30.pkl','rb'))
pca_space= np.load(directory+'models/vectors_pca_30.npy', allow_pickle=True)
id_table=list(np.load(directory+'../data/id_table.npy', allow_pickle=True))
tree = spatial.KDTree(pca_space)
from spacy.lang.fr.stop_words import STOP_WORDS
from spacy.lang.fr import French
parser=French()
stopwords = list(STOP_WORDS)

def process_query(search_query):
    query=str(search_query).lower()
    clean_query = unidecode.unidecode(query)
    tokens=parser(clean_query)
    tokens = [ word.lower_ for word in tokens ]
    tokens = [ word for word in tokens if word not in stopwords]
    tokens = " ".join([i for i in tokens])
    return (tokens)

def query2vec(search_query):
    x=nlp(search_query).vector #spacy 300d
    y=pca.transform([x])[0] #pca 30d
    return(y)

def get_id(idx):
    dataset_id=id_table[idx-1]
    return(dataset_id)

def get_idx(ids):
    dataset_idx=id_table.index(ids)+1
    return(dataset_idx)

def id2vec(ids):
    return(pca_space[get_idx(ids)])

def neighbours(vector, n):
    n_ids=[]
    score=[]
    dist, pos=tree.query(vector, k=n)
    for j in range(len(pos)):
        n_ids.append(get_id(pos[j]))
        score.append(1-dist[j]/50) ##very approximate metric 
    return(n_ids, score)

def main(search_query, n):
    n_ids, score=neighbours(query2vec(process_query(search_query)), n)
    print(n_ids, score)
    return(n_ids, score)

def Similarity(ids, n):
    n_ids, score=neighbours(id2vec(ids), n)
    return(n_ids, score)
    
if __name__ == "__main__":
    main(argv[1], int(argv[2]))


    
    
    