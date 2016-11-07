import numpy as np

# Location of all the Pickle files, stored and used in the Project
PICKLE_LOCATION = 'pickle_data/'

# file names, that includes data thats has been read from files, Starting form Line 3
PROCESSED_FILE = 'processed_file.pkl'

# file names, that includes data thats has been read from files, Starting form Line ZERO
UN_PROCESSED_FILE = 'un_processed_file.pkl'

# file name, that will hold the domain processed data
DOMAIN_PROCESSED_FILE = 'domain_processed_file.pkl'

# List of all the files on which algos need to run
#file_names = [PROCESSED_FILE,'1000.pkl', '2000.pkl','3000.pkl','4000.pkl','5000.pkl','6000.pkl',DOMAIN_PROCESSED_FILE,'domain_1000.pkl', 'domain_2000.pkl','domain_3000.pkl','domain_4000.pkl','domain_5000.pkl','domain_6000.pkl']
file_names = ['2000.pkl','3000.pkl','4000.pkl','5000.pkl','6000.pkl',DOMAIN_PROCESSED_FILE,'domain_1000.pkl', 'domain_2000.pkl','domain_3000.pkl','domain_4000.pkl','domain_5000.pkl','domain_6000.pkl']

# To save all the Plot files
PLOT_FILES_LOCATION = 'plot_files/'

# ALPHA values List
ALPHAS = np.arange(0.01,1.01,0.05)
#ALPHAS = np.arange(0.80,1.01,0.90)

