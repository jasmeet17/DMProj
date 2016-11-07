import pickle
import sys
import os.path
import macros
from sklearn import cross_validation
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif


# Location of all the Pickle files, stored and used in the Project
PICKLE_LOCATION = 'pickle_data/'

# file names, that includes data thats has been read from files, Starting form Line 3
PROCESSED_FILE = 'pickle_data/processed_file.pkl'


### Read the pickle file from file_name; Default using the PROCESSED_FILE
### returns 4 list , training articles,training labels, test articles, test labels
### test_size is the percentage of events assigned to the test set
def process(file_name=PROCESSED_FILE,test_size=0.1,random_state=42):
    ### checks whether the file exists or not
    if not checkFileExists(file_name):
        ### If file not found, Stop Execution and print message
        print "method - process from data_processes"
        sys.exit("File : " + file_name + " Doesn't exists.")
    else:
        t0 = time.time()

        ### Dictionary of { category_name : [articles]
        raw_dict = readFromPickle(file_name)
        X = []
        Y = []

        for category in raw_dict.keys():

            ### creat an array of lablels(as all labels are same for a particular raw_dict object)
            label_id = int(category)
            labels = [label_id] * len(raw_dict[category])

            X.extend(raw_dict[category])
            Y.extend(labels)

        X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X,Y,test_size=test_size,random_state=random_state)

        '''
        ### Text preprocessing, tokenizing and filtering of stopwords
        ### transform documents to feature vectors
        count_vect = CountVectorizer()
        X_train_counts = count_vect.fit_transform(X_train)

        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        '''

        ### text vectorization--go from strings to lists of numbers
        vectorizer = TfidfVectorizer(stop_words='english')
        X_train_transformed = vectorizer.fit_transform(X_train)
        X_test_transformed  = vectorizer.transform(X_test)

        ### feature selection, because text is super high dimensional and
        ### can be really computationally chewy as a result
        selector = SelectPercentile(f_classif, percentile=1)
        selector.fit(X_train_transformed, Y_train)
        features_train_transformed = selector.transform(X_train_transformed).toarray()
        features_test_transformed  = selector.transform(X_test_transformed).toarray()

        print("Time taken to load and process Data: %s seconds ---" % (time.time() - t0))

        #return X_train_tfidf, X_test, Y_train, Y_test
        return features_train_transformed, features_test_transformed, Y_train, Y_test


### Read the object from the Pickle file
### Make sure you called checkFileExists, before calling this
def readFromPickle(file_name):

    if checkFileExists(file_name):
        ### read the pickle file and put the object in object_Read and return same
        file_pkl = open(file_name, 'rb')
        object_Read = pickle.load(file_pkl)
        file_pkl.close()

        return object_Read

### Check whether the file exists
### Return True If exists; Else False
def checkFileExists(file_name):
    if os.path.isfile(file_name):
        return True
    else:
        return False

### save plot as image with name:file_name at macros.PLOT_FILES_LOCATION
### value_list - list of the values
def savePlot(file_name,value_list):
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(0,1,0.1))
    ax.set_yticks(np.arange(0,1.,0.1))
    plt.plot(macros.ALPHAS.tolist(), value_list, 'ro')
    plt.xlabel("Alphas 0.01 to 1.00")
    plt.ylabel("Accuracies")
    plt.axis([0, 1, 0, 1])
    #plt.show()
    plt.draw()
    plt.savefig(macros.PLOT_FILES_LOCATION+file_name,dpi=100)
    plt.clf()
    plt.close(fig)
