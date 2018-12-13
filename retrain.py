import pickle
from sklearn.cluster import KMeans as km

def retrain(clusters):
    pickle_file = open("train_data.pickle", "rb")
    arr = pickle.load(pickle_file)
    pickle_file.close()

    clt = km(n_clusters = clusters)
    clt.fit(arr)

    pickle_file = open("clt.pickle", "wb")
    pickle.dump(clt, pickle_file)
    pickle_file.close()

if __name__ == '__main__':
    retrain(5)
