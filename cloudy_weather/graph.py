adj_list_ = [[0, 1], [2, 3], [4, 3]]


def get_graph_info(adj_list):
    def get_nodes():
        nodes_ = []
        for edge_ in adj_list:
            for node_ in edge_:
                if node_ not in nodes_:
                    nodes_.append(node_)

        return nodes_

    def has_parallel_edge():
        for i in range(len(adj_list) - 1):
            edge_ = adj_list[i]
            next_edge_ = adj_list[i + 1]
            if edge_ == next_edge_ or edge_ == next_edge_[::-1]:
                return True
        return False

    nodes = get_nodes()
    degree = 0
    max_degree = 0
    number_of_loops = 0
    for node in nodes:
        for edge in adj_list:
            if node in edge:
                degree += 1
            if [node, node] == edge:
                number_of_loops += 1
        if degree > max_degree:
            max_degree = degree

        degree = 0

    has_parallel = has_parallel_edge()

    return max_degree, number_of_loops, has_parallel


print(get_graph_info(adj_list_))
