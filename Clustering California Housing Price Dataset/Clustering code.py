import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import math
from kmodes.kmodes import KModes
from scipy.spatial.distance import cdist 
from sklearn import metrics 
import time
from sklearn import preprocessing
import math
from scipy import stats
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics.pairwise import cosine_similarity

"""

1. longitude: A measure of how far west a house is; a higher value is farther west

2. latitude: A measure of how far north a house is; a higher value is farther north

3. housingMedianAge: Median age of a house within a block; a lower number is a newer building

4. totalRooms: Total number of rooms within a block

5. totalBedrooms: Total number of bedrooms within a block

6. population: Total number of people residing within a block

7. households: Total number of households, a group of people residing within a home unit, for a block

8. medianIncome: Median income for households within a block of houses (measured in tens of thousands of US Dollars)

9. medianHouseValue: Median house value for households within a block (measured in US Dollars)

10. oceanProximity: Location of the house w.r.t ocean/sea

--

example of data:
longitude                               -122.23
housing_median_age                           41
total_rooms                                 880
total_bedrooms                              129
population                                  322
households                                  126 
median_income                            8.3252
median_house_value                       452600
ocean_proximity       [0.0, 0.0, 0.0, 1.0, 0.0] # <- this changed!!
#print(df['ocean_proximity'])    #{'<1H OCEAN', 'ISLAND', 'NEAR BAY', 'INLAND', 'NEAR OCEAN'}


Best score:
PCA(test6):
silhouette = 0.95!!

"""
def bin_data(dataframe,column_name,cat_column_name,num_cat):
    column = dataframe[column_name]
    max_c = column.max()
    min_c = column.min()
    cat_col = []
    range_c = max_c - min_c
    if(num_cat==4):
        for elem in dataframe[column_name]:
            if elem==None: cat_col.append(None)
            elif min_c<=elem<=range_c/4: cat_col.append("low pop")
            elif range_c/4 < elem <= range_c/2 : cat_col.append("medium-low pop")
            elif range_c/2 < elem <= 3*range_c/4 : cat_col.append("medium-high pop")
            elif 3*range_c/4 < elem <= max_c : cat_col.append("high pop")
        dataframe[cat_column_name] = cat_col

    elif(num_cat==3):
        for elem in dataframe[column_name]:
            if elem==None: cat_col.append(None)
            elif min_c<=elem<=range_c/3: cat_col.append("low pop")
            elif range_c/3 < elem <= 2*range_c/3 : cat_col.append("medium pop")
            elif 2*range_c/3 < elem <= max_c : cat_col.append("high pop")
        dataframe[cat_column_name] = cat_col
    return dataframe

def elbow_method(data,n_cluster,verbose,init,print_graphs):
    distortions = [] 
    inertias = [] 
    mapping1 = {} 
    mapping2 = {} 
    silhouette_score_arr = []
    K = n_cluster

    t = time.time()

    for k in n_cluster: 
        #Building and fitting the model 
        kmeanModel = KMeans(n_clusters=k,init=init,verbose=verbose)
        kmeanModel.fit(data)    
        if(k<2):    #il coeff di silhouette da problemi calcolato con k=1
            relative_score_for_k = 0
            silhouette_score_arr.append(relative_score_for_k)
        else:
            relative_score_for_k = silhouette_score(data, kmeanModel.labels_, metric='euclidean')
            silhouette_score_arr.append(relative_score_for_k)
        
        distortions.append(sum(np.min(cdist(data, kmeanModel.cluster_centers_, 
                        'euclidean'),axis=1)) / data.shape[0]) 
        inertias.append(kmeanModel.inertia_) 
    
        mapping1[k] = sum(np.min(cdist(data, kmeanModel.cluster_centers_, 
                    'euclidean'),axis=1)) / data.shape[0] 
        mapping2[k] = kmeanModel.inertia_ 


    t1 = time.time()
    print("elbow method fitted in %0.3fs" % (t1-t))

    if(print_graphs):
        plt.plot(K, inertias, 'bx-') 
        plt.xlabel('Values of K') 
        plt.ylabel('Inertia') 
        plt.title('The Elbow Method using Inertia') 
        plt.show()

        plt.plot(K, distortions, 'bx-') 
        plt.xlabel('Values of K') 
        plt.ylabel('Inertia') 
        plt.title('The Elbow Method using distortions') 
        plt.show()

        plt.plot(K, silhouette_score_arr, 'bx-') 
        plt.xlabel('Values of K') 
        plt.ylabel('silhouette score') 
        plt.title('Optimal k using silhouette score') 
        plt.show()

    return kmeanModel

def clustering_raw_data(df, keep_ocean_proximity, want_apply_elbow, n_cluster_for_not_using_elbow, want_print_hist_features, print_scatter_matrix, plot_feature_distr_clusters, plot_lonlat):
    dataframe = df.copy()
    dataframe = dataframe.dropna()               #in this way I drop the nan rows
    del dataframe['ocean_proximity']
    
    if(keep_ocean_proximity):
        df = pd.get_dummies(df)     #turn ocean_proximity categorical feature into numerical one
    else:
        del df['ocean_proximity']
    df = df.dropna()               #in this way I drop the nan rows

    #print(df['total_bedrooms'].isnull().values.any()) #return false, the dropna worked!

    print(df)
    data = df.to_numpy()

    if(want_apply_elbow):
        kmeanModel = elbow_method(data,n_cluster=range(1,10),verbose=1,init='k-means++',print_graphs=True)  #best result for k=5
    else: 
        kmeanModel = KMeans(n_clusters=n_cluster_for_not_using_elbow,init='k-means++',verbose=1)
        kmeanModel.fit(data)

    if(want_print_hist_features):
        figure = df.hist(figsize=[40,30],bins = 50,xlabelsize=8,ylabelsize=8)
        for x in figure.ravel():
           x.title.set_size(8)
        plt.show()

    if(print_scatter_matrix):
        ax = pd.plotting.scatter_matrix(df, alpha=0.2, figsize = [20, 15], c=kmeanModel.labels_)
        for x in ax.ravel():
            x.title.set_size(8)
        plt.show()

    if(plot_feature_distr_clusters):
        dataframe["clusters"] = kmeanModel.labels_
        column_list = list(dataframe.columns)
        column_list.remove("clusters")
        for col in column_list:
            df[col].hist(figsize=[10,5],bins = 50,xlabelsize=8,ylabelsize=8,by=dataframe["clusters"],layout=[1,5])
            plt.suptitle(col)
            plt.show()

    if(plot_lonlat):  
        lon = df['longitude'] #x
        lat = df['latitude'] #y

        pic, axpic = plt.subplots()
        scatter = axpic.scatter(lon,lat,c=kmeanModel.labels_ )
        legend1 = axpic.legend(*scatter.legend_elements(),
                    loc="lower left", title="Clusters")
        axpic.add_artist(legend1)
        plt.show()

def clustering_engineered_data(df,keep_ocean_proximity,want_apply_elbow,pca_component,use_cosine_similarity,n_cluster_for_not_using_elbow,print_scatter_matrix,plot_latlon,plot_pca,plot_feature_distr_clusters):
    print(df)
    df = df.dropna()               #in this way I drop the nan rows
    df = bin_data(df,'population','population_range',3)


    ocean = df['ocean_proximity']
    pop_cat = df['population_range']
    del df['ocean_proximity']
    del  df['population_range']
    lon=df['longitude']
    lat=df['latitude']
    df['people_per_rooms'] = df['households']/df['total_rooms']
    df['non_bedroom_rooms'] = df['total_rooms'] - df['total_bedrooms']
    df['unnecessary_rooms_per_median_income'] = df['non_bedroom_rooms']/df['median_income']
    df['median_age_per_square'] = df['housing_median_age']/((df['longitude'])**2 + (df['latitude'])**2 )
    df['sum_of_income_of_households_in_block'] = df['median_income']*df['households'] #APPROXIMATION! MEAN =/= MEDIAN.
    df['sum_of_income_of_households_per_square'] = df['sum_of_income_of_households_in_block']/((lon)**2 + (lat)**2 )
    df['people_per_bedroom'] = df['households']/df['total_bedrooms']                          
    df['median_income_per_median_house_value'] = df['median_income']/df['median_house_value']


    schema = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 
            'population','households', 'median_income', 'median_house_value','people_per_rooms',
            'non_bedroom_rooms','unnecessary_rooms_per_median_income','median_age_per_square',
            'sum_of_income_of_households_in_block','sum_of_income_of_households_per_square',
            'people_per_bedroom','welfare_of_a_block', 'ocean_proximity','population_range']

    #schema = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value', 'ocean_proximity']

    print(df)
    x = df.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled)
    df = df.assign(ocean_proximity = ocean)
    df = df.assign(population_range = pop_cat)
    df.columns = schema 
    print(df)

    del df['population']
    del df['total_rooms']
    del df['total_bedrooms']
    del df['housing_median_age']
    del df['households']
    del df['welfare_of_a_block']
    df_lonlan = df.copy()
    del df['median_house_value']
    del df['median_income']
    del df['longitude']
    del df['latitude']
    df_for_scat = df.copy()
    del df_for_scat['ocean_proximity']
    del df_for_scat['population_range']
    # ['people_per_rooms','non_bedroom_rooms','unnecessary_rooms_per_median_income',
    # 'median_age_per_square', 'ocean_proximity','people_per_bedroom','median_income_per_median_house_value','ocean_proximity','population_range']

    if(keep_ocean_proximity):
        df = pd.get_dummies(df)     #turn ocean_proximity categorical feature into numerical one
    else:
        del df['ocean_proximity']

    x1 = df.values

    if(use_cosine_similarity):
        dist = 1 - cosine_similarity(x1)
        pca = PCA(n_components=pca_component)
        principalComponents = pca.fit_transform(dist)
    else: 
        pca = PCA(n_components=pca_component)
        principalComponents = pca.fit_transform(x1)
    if(pca_component==2): principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])#,'principal component 3','principal component 4'])
    elif(pca_component==3): principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2','principal component 3'])
    print(principalDf)
    
    #data = df.to_numpy()
    data = principalDf.to_numpy()

    if(want_apply_elbow):
        kmeanModel = elbow_method(data,n_cluster=range(1,10),verbose=1,init='k-means++',print_graphs=True)  #best result for k=5
    else: 
        kmeanModel = KMeans(n_clusters=n_cluster_for_not_using_elbow,init='k-means++',verbose=1)
        kmeanModel.fit(data)

    if(plot_latlon):
        lon = df_lonlan['longitude'] #x
        lat = df_lonlan['latitude'] #y

        pic, axpic = plt.subplots()
        scatter = axpic.scatter(lon,lat,c=kmeanModel.labels_, s = list(100*df_lonlan['median_house_value']) )
        legend1 = axpic.legend(*scatter.legend_elements(),
                    loc="lower left", title="Clusters")
        axpic.add_artist(legend1)
        plt.show()


    if(print_scatter_matrix):
        
        ax = pd.plotting.scatter_matrix(df_for_scat, alpha=0.2, figsize = [20, 15], c=kmeanModel.labels_)
        for x in ax.ravel():
            x.title.set_size(8)
        plt.show()
        

    if(plot_pca):
        if(pca_component==2):
            sequence_containing_x_vals = principalDf['principal component 1']
            sequence_containing_y_vals = principalDf['principal component 2']
            plt.scatter(sequence_containing_x_vals,sequence_containing_y_vals,c=kmeanModel.labels_)
            plt.show()

        elif(pca_component==3):
            fig = plt.figure()
            ax1 = Axes3D(fig)    
            centers = kmeanModel.cluster_centers_   
            sequence_containing_x_vals = principalDf['principal component 1']
            sequence_containing_y_vals = principalDf['principal component 2']
            sequence_containing_z_vals = principalDf['principal component 3']
            ax1.scatter(sequence_containing_x_vals, sequence_containing_y_vals, sequence_containing_z_vals,c=kmeanModel.labels_,marker=",")
            ax1.scatter(centers[0][0], centers[0][1],centers[0][2], marker="D", color='r')
            ax1.scatter(centers[1][0], centers[1][1],centers[1][2], marker="D", color='r')
            ax1.scatter(centers[2][0], centers[2][1],centers[2][2], marker="D", color='r')
            if(n_cluster_for_not_using_elbow==4): ax1.scatter(centers[3][0], centers[3][1],centers[3][2], marker="D", color='r')
            plt.show()

    if(plot_feature_distr_clusters):
        df_for_scat["clusters"] = kmeanModel.labels_
        # ['people_per_rooms','non_bedroom_rooms','unnecessary_rooms_per_median_income',
        # 'median_age_per_square', 'ocean_proximity','people_per_bedroom','median_income_per_median_house_value','ocean_proximity','population_range']
        column_list = list(df_for_scat.columns)
        column_list.remove("clusters")
        for col in column_list:
            df_for_scat[col].hist(figsize=[10,5],bins = 50,xlabelsize=8,ylabelsize=8,by=df_for_scat["clusters"],layout=[1,3])
            plt.suptitle(col)
            plt.show()




#-------------------
#for both kind of data: changing the corresponding boolean variables is it 
# possible to handle the prints of the different graphs.
# To swap from raw to engineered data, change the boolean value at line 397

# for engineered data:
#the code is ready to be launched with PCA_component=3, n_cluster_for_not_using_elbow=3
# with different numbers, some graphs and visualization may fail,although the kmeans algorithm will run

# for raw data:
# the code is ready to be launched with or without the elbow method.
#--------------------

want_to_cluster_on_engineered_data=True

if __name__ == "__main__":
        
    df = pd.read_csv("C:/Users/rikuh/Desktop/Data Mining/homeworks/DM_Homework_3_1912588_Matteo_Emanuele/housing.csv")
    print(df)
    
    if(want_to_cluster_on_engineered_data):
        clustering_engineered_data(df,keep_ocean_proximity=True,want_apply_elbow=False,pca_component=3,
        use_cosine_similarity=True,n_cluster_for_not_using_elbow=3,print_scatter_matrix=False,
        plot_latlon=True,plot_pca=True,plot_feature_distr_clusters=True)
    else: 
        clustering_raw_data(df,keep_ocean_proximity=False,want_apply_elbow=False,
        n_cluster_for_not_using_elbow=3,want_print_hist_features=True,print_scatter_matrix=False,
        plot_feature_distr_clusters = False, plot_lonlat=True)
