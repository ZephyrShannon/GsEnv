# <codecell>


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def split_and_standardization(test_ratio, data):
    X_train,X_test,y_train,  y_test = train_test_split(data['X'],data['y'],test_size = test_ratio, random_state=42 )
    dataset_dic=dict()
    scaler = StandardScaler().fit(X_train)
    dataset_dic['X_train'] = scaler.transform(X_train)
    dataset_dic['X_test'] = scaler.transform(X_test)
    dataset_dic['y_train'] = y_train
    dataset_dic['y_test'] = y_test
    return dataset_dic


# <codecell>

