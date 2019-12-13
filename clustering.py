from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import numpy.matlib as ml


def get_from_file():

    file = open("Deck - Scion of the Ur-Dragon-CHEAP.txt")
    line = file.readline()
    tmp = []
    while line != '':
        tmp.append(line[2:].replace(' ', '').replace(',', '').replace('\'', '').replace('-', '').replace('//', '')
                   .strip().lower())
        line = file.readline()
    return tmp


def cluster_by_commander(cards):

    # vectorization of the texts
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(cards)
    # used words (axis in our multi-dimensional space)
    words = vectorizer.get_feature_names()

    number_of_seeds_to_try=10
    max_iter = 300
    number_of_process=2 # seads are distributed
    max_clusters = 6
    distortions = []
    for y in range(1, max_clusters):

        model = KMeans(n_clusters=y).fit(X)
        distortions.append(model.inertia_)

    avg_slopes = []
    for y in range(2, max_clusters-2):
        slope1 = (distortions[0] - distortions[y-1])/(1 - y)
        slope2 = (distortions[y-1] - distortions[max_clusters-2])/(y - max_clusters-1)
        avg_slopes.append(abs(slope1-slope2))

    curve = distortions
    nPoints = len(curve)
    allCoord = np.vstack((range(nPoints), curve)).T
    np.array([range(nPoints), curve])
    firstPoint = allCoord[0]
    lineVec = allCoord[-1] - allCoord[0]
    lineVecNorm = lineVec / np.sqrt(np.sum(lineVec**2))
    vecFromFirst = allCoord - firstPoint
    scalarProduct = np.sum(vecFromFirst * ml.repmat(lineVecNorm, nPoints, 1), axis=1)
    vecFromFirstParallel = np.outer(scalarProduct, lineVecNorm)
    vecToLine = vecFromFirst - vecFromFirstParallel
    distToLine = np.sqrt(np.sum(vecToLine ** 2, axis=1))
    idxOfBestPoint = np.argmax(distToLine)

    n_clusters = idxOfBestPoint+1
    model = KMeans(n_clusters=n_clusters).fit(X)
    labels = model.labels_
    # indices of preferible words in each cluster
    ordered_words = model.cluster_centers_.argsort()[:, ::-1]

    texts_per_cluster = np.zeros(n_clusters)
    for i_cluster in range(n_clusters):
        for label in labels:
            if label==i_cluster:
                texts_per_cluster[i_cluster] +=1

    print("Top words per cluster:")
    for i_cluster in range(n_clusters):
        print("Cluster:", i_cluster, "texts:", int(texts_per_cluster[i_cluster])),
        for term in ordered_words[i_cluster, :10]:
            print("\t"+words[term])

    print("\n")
    print("Prediction")

    txt = get_from_file()
    print(txt)

    Y = vectorizer.transform([str(txt)])
    predicted_cluster = model.predict(Y)[0]
    texts_per_cluster[predicted_cluster]+=1

    print("Cluster:", predicted_cluster, "texts:", int(texts_per_cluster[predicted_cluster])),
    for term in ordered_words[predicted_cluster, :100]:
        if words[term] not in txt:
            print("\t"+words[term])
