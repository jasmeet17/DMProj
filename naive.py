import data_processes
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
import time
import macros

# Location of all the Pickle files, stored and used in the Project
PICKLE_LOCATION = 'pickle_data/'

# file names, that includes data thats has been read from files, Starting form Line 3
PROCESSED_FILE = 'processed_file.pkl'

# file names, that includes data thats has been read from files, Starting form Line ZERO
UN_PROCESSED_FILE = 'un_processed_file.pkl'


class Naive(object):

    def __init__(self,file_name,test_size=0.1):
        self.X_train, self.X_test, self.Y_train, self.Y_test = data_processes.process(file_name)

    def performMultinomail(self, alpha=1.0):
        t0 = time.time()
        clf = MultinomialNB()
        clf.fit(self.X_train,self.Y_train)
        print("Time taken to Train: %s seconds ---" % (time.time() - t0))

        t0 = time.time()
        accuracy = clf.score(self.X_test,self.Y_test)
        print("Time taken to Tests: %s seconds ---" % (time.time() - t0))
        print "Accuracy : %s" % accuracy

        return accuracy

    def performBernoulli(self, alpha=1.0):
        t0 = time.time()
        clf = BernoulliNB(alpha=alpha)
        clf.fit(self.X_train,self.Y_train)
        print("Time taken to Train: %s seconds ---" % (time.time() - t0))

        t0 = time.time()
        accuracy = clf.score(self.X_test,self.Y_test)
        print("Time taken to Tests: %s seconds ---" % (time.time() - t0))
        print "Accuracy : %s" % accuracy

        return accuracy

    def performGaussian(self):
        t0 = time.time()
        clf = GaussianNB()
        clf.fit(self.X_train,self.Y_train)
        print("Time taken to Train: %s seconds ---" % (time.time() - t0))

        t0 = time.time()
        accuracy = clf.score(self.X_test,self.Y_test)
        print("Time taken to Tests: %s seconds ---" % (time.time() - t0))
        print "Accuracy : %s" % accuracy

        return accuracy


for file_name in macros.file_names:

    print "DATA USED: "+ file_name

    accuracy_Multinomail = []
    accuracy_Bernoulli = []

    for alpha in macros.ALPHAS:

        naive = Naive(PICKLE_LOCATION+file_name,0.3)

        print "==========MultinomialNB=========="
        accuracy_Multinomail.append(naive.performMultinomail(alpha))

        print "\n==========BernoulliNB=========="
        accuracy_Bernoulli.append(naive.performBernoulli(alpha))
        print"============================="
        print


    data_processes.savePlot("MultinomialNB_" + file_name.replace(".pkl", '.png') ,value_list=accuracy_Multinomail)
    data_processes.savePlot("BernoulliNB_" + file_name.replace(".pkl", '.png') ,value_list=accuracy_Bernoulli)

