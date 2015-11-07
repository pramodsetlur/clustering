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

DIMENSIONS = 0
POINTS_COUNT = 0
K_CLUSTERS = 0

def extract_eucledien_point(each_line):
    temp_line = each_line.strip().split(',')
    del temp_line[-1]
    temp_line = [float(i) for i in temp_line]
    return temp_line

def setup(input_file):
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

if __name__ == '__main__':

    if 3 != len(sys.argv):
        print "USAGE: python pramod_setlur_hclust.py [INPUT_FILE] [K_CLUSTERS]"
    else:
        input_file = sys.argv[1]

        K_CLUSTERS = int(sys.argv[2])
        input_point_list = setup(input_file)
        #print input_point_list

