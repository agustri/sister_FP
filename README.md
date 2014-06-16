FP sister : Clustering terdistribusi dengan k-means dan dispy
=============================================================

List File:

1. `kmeans_dispy.py` : clustering dengan yang terdistribusi dispy
2. `kmeans_nodispy.py` : clustering tak terdistribusi

Cara Running `kmeans_dispy.py` :

1. Isi node ip worker pada list `woker_ip` di baris `worker_ip = ['192.168.56.101']`
2. Setting input file csv dataset pada `dataset = load_csv("../data/kddcup.newtestdata_10_percent_unlabeled.csv")`
3. Setting output hasil clustering pada `fname = "../data/cluster-{}.txt".format(i)`
3. Setting jumlah dataset yang dikirim ke worker tiap sekali submit pada `submit_size = 2000`

