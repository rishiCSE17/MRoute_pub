'''
this code is developed under SONNET project


dependency:
    1.https://visualstudio.microsoft.com/downloads/

'''

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
from networkx.readwrite import json_graph
from UI import simple_ui
import json

edge_list = []
'''
ip_list = ['10.1.2.1',
           '10.1.2.2',
           '10.1.2.3',
           '10.1.2.4',
           '10.1.2.5',
           '10.1.2.6']
'''

ip_list=[]
map_dict = {}  # number to IP Addresses
inv_map = {}  # IP Addresses to number
tag_dict_p={} # Create the tag dict
tag_dict_c={} # Create the tag dict

def init():
    global map_dict
    global inv_map
    global tag_dict_p
    global tag_dict_c

    for ip in range(len(ip_list)):
        map_dict[ip] = ip_list[ip]


    for k, v in map_dict.items():
        inv_map[v] = k

    tag_dict_p = inv_map.copy()  # Create the tag dict
    for k in tag_dict_p:
        tag_dict_p[k] = 0

    tag_dict_c = inv_map.copy()  # Create the tag dict
    for k in tag_dict_c:
        tag_dict_c[k] = 0

def reset_tag_dict():
    for k in tag_dict_p:
        tag_dict_p[k] = 0
    for k in tag_dict_c:
        tag_dict_c[k] = 0

def update_tag(node):
    global tag_dict
    tag_dict[node] += 1
    return tag_dict[node]


def grow_tree(adj_matrix, current_node, parents_list, source_node):
    global edge_list
    global tag_dict_p
    global tag_dict_c

    if current_node != source_node:
        call_param = []
        for child in get_neighbour(adj_matrix, inv_map[current_node]):

            c = map_dict[child]

            flag = 0  # to ensure if the neighber is child

            if c not in parents_list:  # if neighbour is not visited
                flag += 1

                t_p = current_node + '_' +str(tag_dict_p[current_node])
                t_c = c + '_' +str(tag_dict_c[c])
                tag_dict_c[c] += 1

                edge_list.append((t_p, t_c))

                parents_list.append(current_node)
                s = set(parents_list)
                parents_list = list(s)

                call_param.append((adj_matrix, map_dict[child], parents_list, source_node))

        if (flag > 0):
            tag_dict_p[current_node] += 1

        for p in call_param:
            grow_tree(p[0], p[1], p[2], p[3])

    else:
        tag_dict_p[current_node] += 1

def get_neighbour(matrix, node_index):
    neighbours_list = matrix[node_index].tolist()[0]
    queue = []
    for i in range(len(neighbours_list)):
        if neighbours_list[i] != 0:
            queue.append(i)
    return queue


class Node(object):
    global all_nodes

    def __init__(self, **kwargs):
        self._id = kwargs['id'] if 'id' in kwargs else id(self)
        self._parent = kwargs['parent'] if 'parent' in kwargs else None
        self._info = kwargs['info'] if 'info' in kwargs else {'label': ''}
        self._children = kwargs['children'] if 'children' in kwargs else []
        self._anc = kwargs['anc'] if 'anc' in kwargs else []

    def node_id(self, i=None):
        if i: self._id = i
        return self._id

    def parent(self, p=None):
        if p: self._parent = p
        return self._parent

    def info(self, i=None):
        if i: self._info = i
        return self._info

    def children(self, node=None):
        if node: self._children.append(node)
        return self._children

    def anc(self, node=None):
        if node: self._anc.append(node)
        return self._anc

    def insert(self, new_node, d):
        new_node.data(d)
        self.children(new_node)
        new_node.anc(self)
        new_node.parent(self)

    def __str__(self):
        line = '***'
        new_line = '\n'
        init = f'Node id is: {self.node_id()}, ' if self.node_id() else 'Node does not have any id, '
        parent = f'parent node id is : {self.parent().node_id()}, ' if self.parent() else 'no parent '
        children = f'the children are: {self.children()} ' if self.children() else 'no children, '
        return new_line + line + init + parent + children + line

# recursively traverse the tree and remove '_num' part
def recur_dict(s):
    d=s
    for k,v in d.items():
        if isinstance(v,dict):
            recur_dict(v)
        if isinstance(v,list):
            for elem in v:
                recur_dict(elem)
        else:
            d[k]=v.split('_')[0] #taking only the IP Address
    returne d


def show_it(li,dst):
    g = nx.DiGraph()
    g.add_edges_from(li)
    g_json=recur_dict(json_graph.tree_data(G=g,root=dst+'_0')) # dropping all _
    ret = json.dumps(g_json, indent=4).replace('id','name') #replacing id with name for d3
    return ret


    #print('============== JSON ====================\n',ret)

    #nx.draw_networkx(g, nx.spring_layout(g))
    #pos = graphviz_layout(g, prog='dot')
    #nx.draw(g, pos, with_labels=True, arrows=False)
    #plt.axis('off')
    #plt.show()

def main(adj_mat, iplist):
    global edge_list
    print('Initialising global data structures...')
    init()
    json_list=[]

    ip_list=iplist
    m=adj_mat

    m1 = np.matrix('0 1 1 0; '
                   '1 0 1 1; '
                   '1 1 0 1;'
                   ' 0 1 1 0')

    m3 = np.matrix('0 1 1 0 0 0; '
                   '1 0 1 1 0 0; '
                   '1 1 0 1 1 0; '
                   '0 1 1 0 1 1; '
                   '0 0 1 1 0 1; '
                   '0 0 1 0 1 0')

    m2 = np.matrix('0 1 1 0 0 1; '
                   '1 0 0 0 0 1; '
                   '1 0 0 1 1 0;'
                   '0 0 1 0 1 1; '
                   '0 0 1 1 0 1; '
                   '1 1 0 1 0 0')

    edge_list_1 = []
    #src = input(r'Enter source ip : ')
    #st = input(r'Enter destination ip : ')

    for src in range(len(ip_list)):
        for dst in range(src+1,len(ip_list)):
            edge_list=[]
            reset_tag_dict()
            print(f'generating tree : {ip_list[src]}-->{ip_list[dst]}')
            grow_tree(m, ip_list[dst], [], ip_list[src])
            json_list.append({'src': ip_list[src],
                              'dst': ip_list[dst],
                              'tree':show_it(edge_list, ip_list[dst])}
                             )
            print('\t JSON Skeleton Generated....')

    #grow_tree(m2, dst, [], src)

    #print('============= Edge List ================ \n',
    #    edge_list)

    #print('============= Number of nodes =============\n',
    #    len(edge_list))

    #show_it(edge_list,dst)


    simple_ui.main(json_list)

#main(adj_mat=None, iplist=)

#if __name__ == '__main()__': main()