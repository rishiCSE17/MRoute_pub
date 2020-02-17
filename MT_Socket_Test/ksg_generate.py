import networkx as nx
import matplotlib.pyplot as plt

def show_sp(topo, src, dst, plot=True):
    spath = nx.shortest_path(topo, src, dst)

    if plot:
        pos = nx.spring_layout(topo)
        nx.draw_networkx(topo, pos, node_color='w')
        nx.draw_networkx_nodes(topo,
                               pos,
                               nodelist=spath,
                               node_shape='d',
                               node_color='g',
                               axis=None
                               )
        plt.axis('off')
        plt.show()
    return spath

def show_topo(topo):
    nx.draw_networkx(topo,
                     pos=nx.draw_spring(topo),
                     node_color='w')
    plt.axis('off')
    return plt


def gen_topo(rt_dict):
    topo = nx.Graph()
    edge_list = []
    all_lan_list = []  # retun value, all lan networks for k-sp calculation

    for key in rt_dict:
        '''
            rt_dict is a dictionary keyed by the router's process id
            the value is a list of last window size updates
            [-1] picks the last update
            [alan] and [awan] are concatinated to form the full neighbour list
            pair of process ID with its neighbours are added to topology edge list
        '''
        for entry in rt_dict[key][-1]['alan'] + rt_dict[key][-1]['awan']:
            edge_list.append((rt_dict[key][-1]['proc'], entry))

        all_lan_list += rt_dict[key][-1]['alan']

    topo.add_edges_from(edge_list)
    return topo, all_lan_list


def gen_all_sp(topo, all_lan_list):
    all_sp = []

    for src in range(len(all_lan_list)):
        for dst in range(src + 1, len(all_lan_list)):
            all_sp.append({'src': all_lan_list[src],
                           'dst': all_lan_list[dst],
                           'ksp': show_sp(topo,
                                          src=all_lan_list[src],
                                          dst=all_lan_list[dst],
                                          plot=False)})
    return all_sp

'''
rt1 = {'proc': 6001,
       'alan': ['192.168.1.0',
                '192.168.2.0'],
       'awan': ['10.1.0.0',
                '10.3.0.0']
       }

rt2 = {'proc': 6002,
       'alan': ['192.168.3.0',
                '192.168.4.0'],
       'awan': ['10.1.0.0',
                '10.2.0.0']
       }

rt3 = {'proc': 6003,
       'alan': ['192.168.5.0',
                '192.168.6.0'],
       'awan': ['10.2.0.0',
                '10.3.0.0']
       }

rt_dict = {6001: [rt1],
           6002: [rt2],
           6003: [rt3]}
'''


# print(rt_dict)
def main_ksp_generate(rt_dict):
    topo, all_lan_list = gen_topo(rt_dict)
    show_topo(topo)
    return gen_all_sp(topo, all_lan_list)

    #for i in out:
    #    print(i)
    # src=input('Enter source Node : ')
    # dst=input('Enter destination Node : ')

    # print(show_sp(topo,src, dst, plot=False))

    # nx.draw_networkx(topo, pos=nx.spring_layout(topo))
    # plt.axis('off')
    # plt.show()
