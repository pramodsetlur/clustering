'''
ALGORITHM
__________
There are various data structures in this algorithm:
    DIMENSIONS - an integer indicating the number of dimensions present for each point in the eucledien space
    POINTS_COUNT - an integer representing the number of points present in the input file
    input_point_list = [[1.0,2.3,4,2,1.3],[2.3,13.2,1.4,2.4],[]...] - a list containing all the input points
    heap = [[distance,[(cluster1),(cluster2)]], [distance,[(cluster1),(cluster2)]], ...] - distance is an float value between cluster1 and cluster2
    not_considered_list = [(cluster1), (cluster2), ...] - This is a list indicating the clusters that have not been encountered yet. Suppose points 'a' and 'b' are merged to form cluster 'ab' then, individual points 'a' and 'b' are removed from this list and 'ab' is added.
    all_clusters_dict = 150 -> [[point1], [point2], ... , [point150]]
                        149 -> [[point1,point2], point3, point4, ... , point149]
                        148 ->
                        147 ->
                        146 ->
                        ...
                        ...
                        3 -> [[point1..point50],[point51..point100],[point101...point150]]
                        2 -> [[point1..point75], [point76..point150]]
                        1 -> [[point1, point2, .. point150]]

                        Suppose there are 150 points.
                        Key is the number of clusters, value is the list of clusters.
                        value is a list - with all the clusters again represented as an individual list

SETUP:
    read_input_list() : input_point_list

    for every combination of points in the input_point_list
        Compute pairwise distance
        add [distance, [(point1), (point2)]] to the heap

    initiatialize_not_considered_list() : not_considered_list //This will now look like - [(point1), (point2), ..., (pointN)]
    cluster_iteration_number = POINTS_COUNT

HIERARCHICAL CLUSTERING
    while cluster_iteration_number >= 1:
        min_distance_cluster = heappop()
        cluster1 = min_distance_cluster[1][0]
        cluster2 = min_distance_cluster[1][1]

        if both cluster1 and cluster2 are in not_considered_list:
            remove cluster1 and cluster2 from n_c_l
            new_cluster = cluster1 + cluster2
            n_c_l.prepend(new_cluster)
            compute pairwise distance with new_cluster and the rest of the elements in n_c_l
            copy n_c_l to all_cluster_dict[cluster_iteration_number]
            cluster_iteration_number --

PRECISION AND RECALL
    Say for  k = 3
    Find all possible pairs in cluster1, cluster2 and cluster3.
    Compute all the possible pairs in the gold standard
    Compare the pairs produced by this algorithm vs the pairs of gold standard and compute the precision and recall
'''
import sys
import math
import heapq

DIMENSIONS = 0
POINTS_COUNT = 0
K_CLUSTERS = 0

def extract_eucledien_point(each_line):
    temp_line = each_line.strip().split(',')
    del temp_line[-1]
    temp_line = [float(i) for i in temp_line]
    return temp_line

def read_input_file(input_file):
    input_point_list = []
    with open(input_file) as file:
        for each_line in file:
            eucledian_point = extract_eucledien_point(each_line)
            input_point_list.append(eucledian_point)
    file.close()
    global DIMENSIONS
    DIMENSIONS = len(input_point_list[1])

    global POINTS_COUNT
    POINTS_COUNT = len(input_point_list)

    #print DIMENSIONS
    #print POINTS_COUNT

    return input_point_list


def compute_centroid(cluster, input_point_list):
    cluster_size = len(cluster)
    cluster_euclidean_points = []
    centroid = []

    for i in range(0, DIMENSIONS):
        centroid.append(0.0)

    for i in range(0, cluster_size):
        point = cluster[i]
        euclean_points = input_point_list[point]
        cluster_euclidean_points.append(euclean_points)

    for i in range(0, DIMENSIONS):
        for j in range(0, cluster_size):
            centroid[i] += cluster_euclidean_points[j][i]
        centroid[i] /= cluster_size

    return centroid


def compute_eucledian_distance(clusterA, clusterB, input_point_list):
    sum = 0
    if 1 == len(clusterA):
        centroidA = input_point_list[clusterA[0]]
    else:
        centroidA = compute_centroid(clusterA, input_point_list)

    if 1 == len(clusterB):
        centroidB = input_point_list[clusterB[0]]
    else:
        centroidB = compute_centroid(clusterB, input_point_list)

    #print "ClusterA:",clusterA, "CentroidA: ",centroidA
    #print "ClusterB:",clusterB, "CentroidB: ",centroidB, "\n"

    for i in range(DIMENSIONS):
        xi = centroidA[i]
        yi = centroidB[i]
        sum += (xi - yi) * (xi - yi)
    distance = math.sqrt(sum)

    return distance

def compute_pair_distance_add_to_heap(i, list, input_point_list, heap):
    j = i + 1
    clusterA = list[i]
    for k in range(j, len(list)):
        clusterB = list[k]
        distance = compute_eucledian_distance(clusterA, clusterB, input_point_list)
        #print distance
        heap_item = [distance, [clusterA, clusterB]]
        #print heap_item
        heapq.heappush(heap, heap_item)

    return heap


def initialize_not_considered_list(not_considered_list):
    #Create a list of [(0),(1),...,POINT_COUNT]
    for i in range(POINTS_COUNT):
        not_considered_list.append([i])

    return not_considered_list

def setup(heap, input_point_list):
    not_considered_list = []
    not_considered_list = initialize_not_considered_list(not_considered_list)

    #Compute pairwise distance between points of all combination of 2
    for i in range(POINTS_COUNT - 1):
        heap = compute_pair_distance_add_to_heap(i, not_considered_list, input_point_list, heap)

    return not_considered_list, heap

def check_heap(heap):
    sort = []
    while heap:
        sort.append(heapq.heappop(heap))
    for i in sort:
        print i

def copy_ncl_all_clusters(cluster_iteration, not_considered_list, all_clusters_dict):
    all_clusters_dict[cluster_iteration] = list(not_considered_list)
    #print cluster_iteration,": ", all_clusters_dict[cluster_iteration], "\n"
    return all_clusters_dict

def merge_clusters(clusterA, clusterB):
    return list(set(clusterA) | set(clusterB))

def hierarchial_clustering(heap, input_point_list):
    all_clusters_dict = {}
    not_considered_list, heap = setup(heap, input_point_list)
    #check_heap(heap)

    cluster_iteration = POINTS_COUNT
    all_clusters_dict = copy_ncl_all_clusters(cluster_iteration, not_considered_list, all_clusters_dict)

    while cluster_iteration > 1:
        min_distance_cluster = heapq.heappop(heap)
        distance = min_distance_cluster[0]
        cluster_information = min_distance_cluster[1]
        clusterA = cluster_information[0]
        clusterB = cluster_information[1]

        if clusterA in not_considered_list and clusterB in not_considered_list:
            not_considered_list.remove(clusterA)
            not_considered_list.remove(clusterB)
            merged_cluster = merge_clusters(clusterA, clusterB)
            not_considered_list.insert(0, merged_cluster)

            heap = compute_pair_distance_add_to_heap(0, not_considered_list, input_point_list, heap)
            cluster_iteration -= 1
            all_clusters_dict = copy_ncl_all_clusters(cluster_iteration, not_considered_list, all_clusters_dict)


    return all_clusters_dict

if __name__ == '__main__':

    if 3 != len(sys.argv):
        print "USAGE: python pramod_setlur_hclust.py [INPUT_FILE] [K_CLUSTERS]"
    else:
        input_file = sys.argv[1]

        K_CLUSTERS = int(sys.argv[2])
        input_point_list = read_input_file(input_file)
        #print input_point_list
        heap = []
        all_clusters_dict = hierarchial_clustering(heap, input_point_list)
        