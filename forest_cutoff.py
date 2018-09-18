import itertools
from tqdm import tqdm
def name_node(i, j):
	return str(i) + "-" + str(j)
def gen_grid(n):
	el = []
	for i in range (0, n):
		for j in range(0, n):
			if (i < n - 1):
				el.append((name_node(i, j), name_node(i+1, j)))
			if (j < n-1):
				el.append((name_node(i, j), name_node(i, j+1)))
	return el

def bld_graph(el):
	graph = {}
	for (a, b) in el:
		if a in graph.keys():
			graph[a].append(b)
		else:
			graph[a] = [b]
		if b in graph.keys():
			graph[b].append(a)
		else:
			graph[b] = [a]
	return graph

def check_is_forest(el):
	graph = bld_graph(el)
	vs = set(graph.keys())
	visited = set([])
	working = set([])
	while len(vs) != 0:
		if len(working) == 0:
			#print "pop new component"
			working = set([vs.pop()])
			visited = set([])
		head = working.pop()
		visited.add(head)
		nbs = set(graph[head])
		if len(visited.intersection(nbs)) > 1:
			return False
		working = working.union(nbs.difference(visited))
		vs = vs.difference(visited)
	return True

def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

def fix_edge_add(fix_e, el):
	(a, b) = fix_e
	output = []
	for (x, y) in el:
		xp = x
		yp = y
		if (x == b):
			xp = a
		if (y == b):
			yp = a
		if (xp == yp):
			continue
		output.append((xp, yp))
	return output

def fix_edge_del(fix_e, el):
	#copies the list
	(a, b) = fix_e
	output = []
	for (x, y) in el:
		if ((x == a) and (y == b)) or ((x == b) and (y == a)):
			continue
		output.append((x, y))
	return output

def count_forests(el):
	count = 0
	print len(el)
	for elp in tqdm(powerset(el)):
		if check_is_forest(elp):
			count = count + 1
	return count

def get_forest_prob_bf(edge, el):
	print len(el)
	pos = count_forests(fix_edge_add(edge, el))
	neg = count_forests(fix_edge_del(edge, el))
	return float(pos)/float(pos + neg)

#print count_forests(gen_grid(4))

#print get_forest_prob_bf(("0-0", "0-1"), gen_grid(4))

def make_transitive_closure(graph):
	mod = True
	for v in graph.keys():
		graph[v] = set(graph[v])
	while mod:
		mod = False
		for v in graph.keys():
			for nb in graph[v]:
				if not (graph[v].issuperset(graph[nb])):
					graph[v] = graph[v].union(graph[nb])
					mod = True
	output = []
	#print "foo"
	#print graph
	for v in graph.keys():
		test = []
		for vert in graph[v]:
			#print vert
			if vert[0:4] == "base":
				#print "asdfa"
				continue
			test.append(vert)
		test = frozenset(test)
		if not (test in output) and len(test) != 0:
			output.append(test)
	#print output
	return frozenset(output)


def dp_grid_cnt(n):
	state = {}
	edges = []
	for j in range(0, n-1):
		edges.append((str(j), str(j+1)))
	for el in powerset(edges):
		graph = bld_graph(el)
		graph = make_transitive_closure(graph)
		state[graph] = 1
		#state.append(graph)
	for i in tqdm(range(1, n)):
		edges = []
		for j in range(0, n):
			#do edge filtering here
			edges.append(("base-" + str(j), str(j)))
			if (j < n-1):
				edges.append((str(j), str(j+1)))
		next_state = {}
		for graph in tqdm(state.keys()):
			graph_edges = []
			for component in graph:
				foo = list(component)
				for z in range(0, len(foo)-1):
					graph_edges.append(("base-" + str(foo[z]), "base-" + str(foo[z+1])))
			for el in powerset(edges):
				el = list(el)
				if check_is_forest(el + graph_edges):
					#compatible
					cur_index = make_transitive_closure(bld_graph(el + graph_edges))
					if cur_index in next_state.keys():
						next_state[cur_index] = next_state[cur_index] + state[graph]
					else:
						next_state[cur_index] = state[graph]
		state = next_state

	count = 0
	for graph in state:
		count = count + state[graph]
	return count

print dp_grid_cnt(6)



