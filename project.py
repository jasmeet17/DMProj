import os.path
import glob
import linecache
import time
import pickle
import collections
from tld import get_tld
from operator import itemgetter


# Lines from which to read the Text files
READ_FROM_LINE = 3

# Location of all the Pickle files, stored and used in the Project
PICKLE_LOCATION = 'pickle_data/'

# file names, that includes data thats has been read from files, Starting form Line 3
PROCESSED_FILE = 'processed_file.pkl'

# file names, that includes data thats has been read from files, Starting form Line ZERO
UN_PROCESSED_FILE = 'un_processed_file.pkl'

# RAW text files
RAW_DATA = 'data/*'

# Fetch top x domains
TOP_DOMAINS = 200

# file holds the key=category : value=Top domains
TOP_DOMAINS_LISITING = 'top_domains_listing.pkl'

# file name, that will hold the domain processed data
DOMAIN_PROCESSED_FILE = 'domain_processed_file.pkl'


class Data(object):

    def __init__(self):
        # store processed files in array and put them in Dictionary correspodig to category Name
        # Top 3 lines not included
        self.processed_Data = {}

        # store files in array starting from line ZERO
        self.un_Processed_Data = {}

        # If PKL File exists Therefore no need to read data from raw files.
        # data start from line=3
        if self.checkFileExists(PICKLE_LOCATION+PROCESSED_FILE):
            # read from the pkl file
            self.processed_Data = self.readFromPickle(PICKLE_LOCATION+PROCESSED_FILE)
        else:
            self.processed_Data = self.loadData(PROCESSED_FILE,READ_FROM_LINE)
            self.processed_Data = self.readFromPickle(PICKLE_LOCATION+PROCESSED_FILE)

            # split data in seperate files
            self.seperateData('',self.processed_Data)

        # If PKL File exists Therefore no need to read data from raw files.
        # data startinf from line=Zero
        if self.checkFileExists(PICKLE_LOCATION+UN_PROCESSED_FILE):
            # read from the pkl file
            self.un_Processed_Data = self.readFromPickle(PICKLE_LOCATION+UN_PROCESSED_FILE)
        else:
            self.loadData(UN_PROCESSED_FILE,0)
            self.un_Processed_Data = self.readFromPickle(PICKLE_LOCATION+UN_PROCESSED_FILE)

            # split data in seperate files
            self.seperateData('raw_',self.un_Processed_Data)

    # put the top TOP_DOMAINS in the TOP_DOMAINS_LISITING file
    # that can be used to later to seperate dat based on domains
    def domainAnalysis(self):
        if self.checkFileExists(PICKLE_LOCATION+TOP_DOMAINS_LISITING):
            print 'Domains list file already exists'
        else:
            # folders contains all the folders that have data
            folders = glob.glob(RAW_DATA)

            # will hold the top domains key=category : value=list of top domains
            top_domains = {}

            for folder in folders:
                # files_path contains path for the text files from a folder
                files_paths =  glob.glob(folder+"/*.txt")

                domain_Names = []
                for file_path in files_paths:
                    # URL - get the first Line of the Text, which is URL always
                    URL = self.readFirstLine(file_path)

                    try:
                        res = get_tld(URL, as_object=True)
                        # get domain name using - res.domain; add in domain_Names
                        domain_Names.append(res.domain)
                    except Exception, e:
                        #print e
                        #print file_path
                        continue

                # convert the domains_Names - >collection object and then convert to tuple list
                domain_counts = collections.Counter(domain_Names).items()

                # sort the tuple list and store them again to domain_counts(over_ride)
                # in decreasing order
                domain_counts= sorted(domain_counts, key=lambda x: x[1],reverse=True)

                # category Number(as str)
                categoryName = self.getCategoryName(folder)

                # make sure we have min of TOP_DOMAINS; ELSE use all domain_counts
                if len(domain_counts)>TOP_DOMAINS:
                    top_domains[categoryName] = map(itemgetter(0), domain_counts[:TOP_DOMAINS])
                else:
                    top_domains[categoryName] = map(itemgetter(0), domain_counts)

            # save the top domains listing in pkl file
            self.saveProcessedData(PICKLE_LOCATION+TOP_DOMAINS_LISITING,top_domains)

    # save the data based on domain, in the pkl file
    def domainBasedData(self):

        # if the pkl data of file exists read it from there; Else Domain analysis
        if self.checkFileExists(PICKLE_LOCATION+TOP_DOMAINS_LISITING):
            top_domains = self.readFromPickle(PICKLE_LOCATION+TOP_DOMAINS_LISITING)
        else:
            self.domainAnalysis()
            top_domains = self.readFromPickle(PICKLE_LOCATION+TOP_DOMAINS_LISITING)

        # folders contains all the folders that have data
        folders = glob.glob(RAW_DATA)

        # data , Dictionary contains all data key:category, value:List of the text files text
        # starting from line_no
        data={}
        for folder in folders:
            # category Number(as str)
            categoryName = self.getCategoryName(folder)

            # files_path contains path for the text files from a folder
            files_paths =  glob.glob(folder+"/*.txt")

            # put all the files into array
            files_text_array = []
            # iterate through all files in a particular folder
            for file_path in files_paths:

                # URL - get the first Line of the Text, which is URL always
                URL = self.readFirstLine(file_path)

                try:
                    res = get_tld(URL, as_object=True)

                    # get domain name using - res.domain;
                    # if the article domains is in the TOP_DOMAINS
                    # time.sleep(0.3)

                    # print "Out Side"
                    # print res.domain
                    # print len(top_domains[categoryName])
                    # print "++++++++++"

                    if res.domain in top_domains[categoryName]:
                        # print URL
                        # print categoryName
                        # print 'Goes Inside'

                        # text starting from Line READ_FROM_LINE
                        text = self.readFileFromLine(file_path,READ_FROM_LINE)
                        files_text_array.append(text)

                except Exception, e:
                    #print e
                    #print file_path
                    continue

            # save files_text_array, which constains all the text files
            # data into dictionary corresponding to category name
            data[categoryName] = files_text_array

        # save the Processed Data
        self.saveProcessedData(PICKLE_LOCATION+DOMAIN_PROCESSED_FILE,data)

        # split data in seperate files domain based
        self.seperateData('domain_',data)

    # read the data from the RAW text files, from a particular line
    # and save them in the 'file_name + .pkl'
    def loadData(self,file_name,line_no):
        # folders contains all the folders that have data
        folders = glob.glob(RAW_DATA)

        # data , Dictionary contains all data key:category, value:List of the text files text
        # starting from line_no
        data={}
        for folder in folders:
            # category Number(as str)
            categoryName = self.getCategoryName(folder)

            # files_path contains path for the text files from a folder
            files_paths =  glob.glob(folder+"/*.txt")

            # put all the files into array
            files_text_array = []
            # iterate through all files in a particular folder
            for file_path in files_paths:
                # text starting from Line READ_FROM_LINE
                text = self.readFileFromLine(file_path,line_no)
                files_text_array.append(text)

            # save files_text_array, which constains all the text files
            # data into dictionary corresponding to category name
            data[categoryName] = files_text_array

        # save the Processed Data
        self.saveProcessedData(PICKLE_LOCATION+file_name,data)



    # Seperate data according to [1000,2000,3000,4000,5000,6000] length
    # file_prefix is the prefix of the pkl file to be saved
    # example Greater than 1000 saved as 'file_prefix + 1000.pkl'
    def seperateData(self,file_prefix,data):
        # Process the Data for lengths [1000,2000,3000,4000,5000]
        for length in [1000,2000,3000,4000,5000,6000]:

            data_for_length = {}

            for key in data.keys():
                category_data = []
                for x in data[key]:
                    if len(x)>=length:
                        category_data.append(x)
                data_for_length[key] = category_data

            # save the data in pkl for length, with file_name = file_prefix + length.pkl
            self.saveProcessedData(PICKLE_LOCATION+file_prefix+str(length)+".pkl",data_for_length)

    # Read the first line of the file_name
    # @returns - First
    def readFirstLine(self,file_name):
        filez = open(file_name,'r')
        line = filez.readline()
        filez.close()

        return line

    # Reads the text from file_name starting from particular line_no
    # returns the text
    def readFileFromLine(self,file_name,line_no):
        filez = open(file_name,'r')
        lines = filez.readlines()[line_no:]

        # text = text starting from Line line_no
        text = ''.join(lines)
        filez.close()

        return text

    # Check whether the file exists
    # Return True If exists; Else False
    def checkFileExists(self,file_name):
        if os.path.isfile(file_name):
            return True
        else:
            return False

    # Read the object from the Pickle file
    # Make sure you called checkFileExists, before calling this
    def readFromPickle(self,file_name):

        if os.path.isfile(file_name):
            # read the pickle file and put the object in object_Read and return same
            file_pkl = open(file_name, 'rb')
            object_Read = pickle.load(file_pkl)
            file_pkl.close()

            return object_Read

    # Save save_Object as pkl file at file_name
    def saveProcessedData(self,file_name,save_Object):
        if os.path.isfile(file_name):
            print "File :" + file_name + " already exist"
        else:
            print "File :" + file_name + "  Doesn't exist"
            # write the object to the file
            output = open(file_name, 'wb')
            pickle.dump(save_Object, output)
            output.close()


    # get the category name from the give folder
    def getCategoryName(self,folder_name):
        categoryName = folder_name[-2:]
        return categoryName




# Load the Data
t0 = time.time()
data = Data()
print("Time taken to load Data: %s seconds ---" % (time.time() - t0))

print "Domain Analysis"
t0 = time.time()
data.domainAnalysis()
data.domainBasedData()
print("Time taken to Domain Analyse Data: %s seconds ---" % (time.time() - t0))

# dictionary = data.readFromPickle(PICKLE_LOCATION+TOP_DOMAINS_LISITING)
# for key in dictionary.keys():
#     print key
#     print dictionary[key]
#     print "****"

