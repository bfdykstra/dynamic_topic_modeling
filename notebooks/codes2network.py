
def csv2network(infilename):
    """Convert a list of observations with attributes (valued 0 or 1)
    in columns to a network format. Each column becomes a node,
    with the column header as its name; each observation becomes
    a fully connected network among nodes for which that attribute is a 1.
    """
    import csv
    import itertools

    with open(infilename, 'rU') as infile:
        inreader = csv.reader(infile)
        cutoff = 5

        attrnames = inreader.next()[cutoff:]  # column headers -> attribute names

        # make a list of all edges
        # (note: we generate 2 entries for each edge, in either order)
        edgedict = {edge: [0,0] for edge in \
                    itertools.permutations(range(len(attrnames)), 2)}

        totalcounts = []
      
        for counter, obs in enumerate(inreader):
            
            if len(obs) > 0: 
                if totalcounts == []:
                    totalcounts = [1 if x == '1' else 0 for x in obs[cutoff:]]
                else:
                    totalcounts = [x + 1 if y == '1' else x for x, y in zip(totalcounts, obs[cutoff:])]
                
                # get list of attributes for which this observation has a 1
                attributelist = [i for i, j in enumerate(obs[cutoff:]) if j == '1']
                # generate all possible pairs, unordered -> these are edges
                obs_network = list(itertools.combinations(attributelist, 2))
                # increment edge counters for these edges
                for edge in obs_network:
                    edgedict[edge][1] += 1                
                    edgedict[edge][0] = obs[5]
        
        #print edgedict
        nrobs = counter + 1
        print "Processed %d articles" % nrobs
        nrobs = float(nrobs)
        #print " total counts: ", totalcounts
        attrfractions = [x/nrobs for x in totalcounts]
        # Combine paired edge counters & divide by total, to get percentage
        edgedict2 = {}
        for edge in itertools.combinations(range(len(attrnames)), 2):
            edgedict2[edge] = [ edgedict[edge][0], 100 * (edgedict[edge][1] + edgedict[(edge[1], edge[0])][1]) / float(nrobs) ]

        # edgedict2 = {edge: 100 * (edgedict[edge][1] + edgedict[(edge[1], edge[0])]) / float(nrobs) \
        #              for edge in itertools.combinations(range(len(attrnames)), 2)}
        # Remove imaginary edges before returning 
        return attrnames, attrfractions, \
               {edge: val for edge, val in edgedict2.iteritems() if val[1] > 0}


def network2gv(nodenames, nodefractions, edgedict):
    """Convert a list of nodenames and edges with counts to graphviz format."""
    from graphviz import Graph
    import sys
    import csv

    absweights = False
    cutoff = 14.28 # 16.66
    relcutoff = 4.95

    topicnames = {}
    with open('/Users/maurits/TRIPvars.csv', 'rU') as nodefile:
        for row in csv.reader(nodefile):
            topicnames[row[0]] = row[1]

    ldalist = ['topic0', 'topic1', 'topic2', 'topic3', 'topic4', 'topic5',
               'topic6', 'topic7', 'topic8', 'topic9', 'topic10', 'topic11',
               'topic12', 'topic13', 'topic14', 'topic15', 'topic16',
               'topic17', 'topic18', 'topic19']
    metalist = ['anywoman', 'policyprescriptionX', 'multiauthors', 'firstwoman',
                'AJPS', 'APSR', 'BJPS', 'EJIR', 'IO', 'IS', 'ISQ', 'JCR', 'pub1980s', 'pub1990s', 'pub2000s',
                'pub2010s', 'citations_upto3', 'citations_4to7', 'citations_8to12', 'citations_13to20',
                'citations_21to30', 'citations_31to50', 'citations_51plus']
    theorylist = ['seriouslyrealismX', 'seriouslyliberalismX', 'seriouslymarxismX',
                  'seriouslyconstructivismX', 'seriouslynonparadigmaticX',
                  'seriouslyatheoreticnoneX', 'synthesisrealismX', 'synthesisliberalismX',
                  'synthesismarxismX', 'synthesisconstructivismX',
                  'synthesisnonparadigmaticX', 'synthesisnosynthesisX', 'ideationalX',
                  'materialX', 'epistemologyX', 'realist', 'liberal', 'nonparadigm',
                  'atheoretic', 'constructivist', 'marxist',]
    methodlist = ['level1X', 'level2X', 'level3X',
                  'levelnoneX', 'quantitativeX', 'qualitativeX', 'formalmodelingX',
                  'counterfactualX', 'analyticnonformalX', 'descriptiveX',
                  'policyanalysisX', 'experimentalX', ]
    timelist = ['time1X', 'time2X', 'time3X', 'time4X', 'time5X', 'time6X',
                'time7X', 'time8X', 'time9X', 'timenoneX', 'contemporaryX']
    subjectlist = ['unitedstatesX', 'canadawesteuropeX', 'latinamericaX',
                   'subsaharanafricaX', 'fsueasterneuropeX', 'middleeastnorthafricaX',
                   'eastasiaX', 'southasiaX', 'southeastasiaX', 'oceaniaX', 'globalX',
                   'noneX', 'antarticaX', 'alliancesX', 'balanceofpowerX',
                   'bargainingdeterrencestrategyX', 'developmentX', 'diplomacyX',
                   'domesticpoliticsX', 'economicinterdependenceX', 'ethnicityreligionX',
                   'environmentX', 'foreignaidX', 'foreignpolicyX', 'genderX', 'intllawX',
                   'igoX', 'itnlregimesX', 'interstatecrisisX', 'interstatewarX',
                   'intrastateconflictX', 'migrationX', 'humanitarianX', 'monetarypolicyX',
                   'northsouthrelationsX', 'publichealthX', 'publicopinionX', 'regimetypeX',
                   'regionalintegrationX', 'sanctionsX', 'irdisciplineX', 'terrorismX',
                   'tradeX', 'ngoX', 'weaponsystemsX', 'wmdproliferationX', 'otherX']
    colors = ['cyan', 'chartreuse', 'red', 'gold', 'bisque', 'magenta']
    shapes = ['box', 'box', 'diamond', 'hexagon', 'hexagon', 'oval']
    nodelists = [ldalist, subjectlist, metalist, theorylist, methodlist, timelist]
    nodespecs = [(x, col, shp) for nodes, col, shp in zip(nodelists, colors, shapes) for x in nodes]
    excludelist = ['topic4', 'topic8', 'topic15', 'seriouslyatheoreticnoneX',
                   'materialX', 'synthesisnosynthesisX', 'citations_51plus', 'pub1990s',
                   'firstwoman', 'pub2000s', 'noneX', 'nonparadigm', 'multiauthors', 'otherX']

    # Get edge info
    edgevals = [x[1] for x in edgedict.iteritems()]
    print "Edge values (percentages of %d edges total): mean - %5.2f, maximum: %5.2f," % \
          (len(edgevals), sum(edgevals)/float(len(edgevals)), max(edgevals))
    if absweights:
        print "Nr above %d percent - %d" % \
              (cutoff, len([1 for x in edgedict.iteritems() if x[1] > cutoff]))
    else:
        print "Nr above more than %d times independence - %d" % \
              (relcutoff, len([1 for x in edgedict.iteritems() \
                               if x[1] / 100 > relcutoff * nodefractions[x[0][0]] * nodefractions[x[0][1]]]))

    sys.stdout.flush()  # Make sure this gets printed as the system is calculating the graph

    netwk = Graph('TRIPgraph', format='png')
    netwk.graph_attr.update({'bgcolor': 'transparent'})

    nodes = []
    for edge, value in edgedict.iteritems():
        node1 = nodenames[edge[0]]
        frac1 = nodefractions[edge[0]]
        node2 = nodenames[edge[1]]
        frac2 = nodefractions[edge[1]]
        if ((absweights and (value > cutoff)) or
                (not absweights and (value / 100 > relcutoff * frac1 * frac2))) and \
                (node1 not in excludelist and node2 not in excludelist) and (node1 != node2):
            nodes.append(edge[0])
            nodes.append(edge[1])
    nodenrs = set(nodes)
    nodelist = [nodenames[i] for i in nodenrs]

    # Create nodes, with color & shape
    for item, col, nodeshape in nodespecs:
        if item in nodelist:
            itemname = item if item not in topicnames else topicnames[item]
            netwk.node(itemname, style='filled', fillcolor=col, shape=nodeshape)

    # netwk_topic = Graph('cluster_topic')
    # netwk_topic.node_attr.update(style='filled', color=topiccolor, shape='box')
    # for item in topiclist:
    #     netwk_topic.node(item)
    # netwk.subgraph(netwk_topic)

    # Create edges
    for edge, value in edgedict.iteritems():
        # Add edges with values, if they pass threshold
        # Make colour depend different if within grouping
        node1 = nodenames[edge[0]]
        frac1 = nodefractions[edge[0]]
        name1 = node1 if node1 not in topicnames else topicnames[node1]
        node2 = nodenames[edge[1]]
        frac2 = nodefractions[edge[1]]
        name2 = node2 if node2 not in topicnames else topicnames[node2]

        # if node1 in topiclist and node2 in topiclist:
        #     edgecolor = topiccolor
        # elif node1 in timelist and node2 in timelist:
        #     edgecolor = timecolor
        # elif node1 in methodlist and node2 in methodlist:
        #     edgecolor = methodcolor
        # elif node1 in authorlist or node2 in authorlist:
        #     edgecolor = authorcolor
        # elif node1 in ldalist and node2 in ldalist:
        #     edgecolor = ldacolor
        # else:
        edgecolor = 'black'
        if ((absweights and (value > cutoff)) or
                (not absweights and (value / 100 > relcutoff * frac1 * frac2))) and \
                (node1 not in excludelist and node2 not in excludelist) and \
                name1 != name2:
            if absweights:
                if value <= 20:
                    binvalue = 2
                elif value <= 25:
                    binvalue = 3
                elif value <= 40:
                    binvalue = 4
                else:
                    binvalue = 6
                edgelabel = str(value)[:4]
            else:
                strength = (value / 100) / (frac1 * frac2)
                if strength <= 5.6: # was 7
                    binvalue = 1
                elif strength <= 6.6: # was 10
                    binvalue = 2
                elif strength <= 7.6: # was 15
                    binvalue = 3
                else:
                    binvalue = 4
                edgelabel = str(strength)[:4]
            netwk.edge(name1, name2, label=edgelabel,
                       color=edgecolor, weight=str(binvalue)) # ,
                       # penwidth=str(int(value/cutoff) + 1))
    netwk.view()
    return netwk


def network2snap(nodenames, edgedict):
    """Convert a list of nodenames and edges with counts to snap format."""
    import snap

    netwk = snap.TNEANet.New()

    # Create nodes
    netwk.AddStrAttrN('name')  # nodes have a name
    for i, name in enumerate(nodenames):
        # Add nodes with names
        netwk.AddNode(i)
        netwk.AddStrAttrDatN(i, name, 'name')

    # Create edges; add edges first, then attributes
    netwk.AddFltAttrE('val')   # edges have a value
    edgedata = edgedict.iteritems()
    for edge, value in edgedata:
        edgeid = edge[0] * 100 + edge[1]
        netwk.AddEdge(edge[0], edge[1], edgeid)
    for edge, value in edgedata:
        edgeid = edge[0] * 100 + edge[1]
        netwk.AddStrAttrDatE(edgeid, value, 'val')
    return netwk


# This function is not yet implemented
def assigncolors(attribnames):
    """Generate a hash table for the attribute name -> colour mapping.

    Assign the same colours to related attributes. Hard-coded.
    """
    import snap
    colortable = snap.TIntStrH()
    colortable.AddDat(1, 'blue')


def attribs2network(infilename, outfilestem):
    """Convert csv file of attributes to network file, and display."""
    import snap

    attribnames, edgedict = csv2network(infilename)
    # attrib2colorH = assigncolors(attribnames)
    network = network2snap(attribnames, edgedict)
    FOut = snap.TFout(outfilestem + '.graph')
    network.Save(FOut)
    FOut.Flush()
    snap.SaveEdgeList(network, outfilestem + '.csv',
                      'Save as tab-separated list of edges')
    snap.SaveGViz(network, outfilestem + '.dot', 'graph from attribute list', True)
    
    
def network2nodes(outfile_path, yr_dict, keep_strengths = False):
    
    """
    Params:
    
    String data: File path to the Trip database
    
    String outfile_path: File path to the file that you want to write to. Will be read by D3 force graphs
    
    Dictionary yr_dict: A dictionary with yrs as keys, edge information as keys. This information includes 
    what node(s) it attaches too, and the strength of that attachment
    
    Bool keep_strengths: boolean flag on whether to keep the strength of a connection as part of the data
    
    Initial structure of just_connects
    {
        "2000": {0: [......], 1: [.....]},
        "2001": {0: [......], 1: [.....]}
    }
    
    We then strip the index keys (0, 1, 2, ... etc.) from the inner dictionaries so that the final structure
    is as follows:
    {
        "2000": [[.....],[.....]],
        "2001": [[.....],[.....]]
    }
    
    For each year as a key, there is a list of nodes, denoted by the index of the list. At each index there is
    a sublist with indices of the nodes that that node is connected to. For example, if we wanted to see what
    node 50 was connected to in 2015, we would type connects['2015'][50]. This returns a sublist of other 
    indices that node 50 is connected too.
    """
    connects = {}

    for key in yr_dict.iterkeys():
        connects[key] = {}
        for connection in yr_dict[key]:
            if connection[0] in connects[key]:
                if keep_strengths:
                    #append tuple including strength
                    connects[key][connection[0]].append((connection[1], connection[2]))
                else:
                    connects[key][connection[0]].append(connection[1])
            else:
                if keep_strengths:
                    connects[key][connection[0]] = [(connection[1], connection[2])]
                else:
                    connects[key][connection[0]] = [connection[1]]

    
    #strip the numeric index key out so that we are left with only years and their values
    for key in connects.iterkeys():
        connects[key] = connects[key].values()
    
    #Check the indexes in each list and make sure they don't point to an index that is out of range
    for key,val in connects.iteritems():
        for node in xrange(len(val)):
            if keep_strengths:
                filtered_list = [connection for connection in val[node] if connection[0] < len(val)]
            else:
                filtered_list = [connection for connection in val[node] if connection < len(val)]
            val[node] = filtered_list
            
    #save file as a json
    with open(outfile_path, 'w') as outfile:
        json.dump(connects, outfile)
        
    return connects

