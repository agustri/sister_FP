import dispy
import numpy
from scipy.cluster.vq import kmeans

### OWN CODE ###
def distance(a, b):
    from math import sqrt
    sum = 0.0
    for i in (a-b):
        sum += (i*i)
    return sqrt(sum)

def compute(centroids, dataset, start_id):
    import numpy
    cluster_data = []
    for i in range(len(centroids)):
        cluster_data.append([])
        cluster_data[i] = []

    data_id = start_id
    for data in dataset:
        cluster_id = 0
        min_dist = float('inf')
        for i in range(len(centroids)):
            dist = distance(data, centroids[i])
            if dist < min_dist:
                min_dist = dist
                cluster_id = i
        cluster_data[cluster_id].append(data_id)
        data_id += 1
    print "dataset terproses =", data_id - start_id,
    return cluster_data

def load_csv(file):
    temp1 = []
    with open(file) as f:
        reader = f.readlines()
        size = len(reader)
        for row in xrange(size):
            temp = []
            t = reader[row].split('\r')
            d = t[0].split(',')
            for i in xrange(len(d)):
                c = float(d[i])
                temp.append(c)
            temp1.append(temp)
    dataset = numpy.array(temp1)
    print "jumlah dataset", len(dataset)
    return dataset
### OWN CODE ###

if __name__ == '__main__':
    cluster_count = 4
    dataset = load_csv("../data/kddcup.newtestdata_10_percent_unlabeled.csv")
    datasize = len(dataset)
    centroids,_ = kmeans(dataset, cluster_count)

    # setup worker yang akan mengeksekusi fungsi compute yang bergantung pada fungsi distance
    worker_ip = ['192.168.56.101']
    cluster = dispy.JobCluster(compute, nodes=worker_ip, depends=[distance])
    jobs = []
    # jumlah dataset yang dikirim ke worker sekali submit
    submit_size = 2000
    start_id = 0
    job_count = 0
    while start_id < datasize:
        end_id = start_id + submit_size
        if end_id > datasize:
            end_id = datasize
        # mengirim parameter ke fungsi 'compute'
        job = cluster.submit(centroids, dataset[start_id : end_id], start_id) 
        # id dataset
        job.id = job_count
        jobs.append(job)
        start_id = end_id
        job_count += 1

    result = []
    for i in range(cluster_count):
        result.append([])
        result[i] = []

    for job in jobs:
        # menunggu job worker selesai
        job() 
        print('job %s selesai, stdout -> %s' % (job.id, job.stdout))
        for i in range(cluster_count):
            result[i] = result[i] + job.result[i]
    for i in range(cluster_count):
        fname = "../data/cluster-{}.txt".format(i)
        print "Menulis hasil cluster", i, "ke", fname
        with open(fname, 'w') as f:
            f.write(str(result[i]))
