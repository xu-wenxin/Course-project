import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


class Data():
    def __init__(self) -> None:
        pass
    
    # read dataset
    def read_data(self):
        data_path='https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv'
        data=pd.read_csv(data_path,sep=';')
        
        return data
    
    # split dataset into x and y
    def split_x_y(self,data):
        # numpy format
        data_np =np.array(data)
        
        # split x and y from column 11
        xs, ys = np.split(data_np,[11], axis=1 )
        # transpose ys
        ys = ys.reshape(-1)
        
        return xs,ys
    
    # Noise processing of data sets
    def data_noise(self,feature_num,xs):
        from sklearn.decomposition import PCA
        
        # downscale the data set to 'feature_num'
        pca=PCA(feature_num)
        xs_trans=pca.fit_transform(xs)  # downscale
        xs_pca=pca.inverse_transform(xs_trans)  #upgrading
        
        return xs_trans,xs_pca

    def data_processing(self,xs,ys,nomal=None):
        # saparate training and testing data and random
        # train: 80%; test:20%
        xs_train, xs_test, ys_train, ys_test = train_test_split(xs, ys, test_size = 0.2,random_state=0)

        # If the user enters True, use z-score for normalization
        if nomal:
            # normalization with z-score
            mu = np.mean(xs_train, axis=0)
            sigma = np.std(xs_train, axis=0)

            xs_train = (xs_train - mu)/sigma
            xs_test = (xs_test - mu)/sigma
            xs = (xs - mu)/sigma
        else:
            pass
        
        return xs, xs_train, xs_test, ys_train, ys_test
        