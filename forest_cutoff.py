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

#pls don't use these two
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

def bf_count_forests(el, add_edges, del_edges):
	count = 0
	el = set(el).difference(set(add_edges + del_edges))
	print len(el)
	for elp in tqdm(powerset(el)):
		if check_is_forest(list(elp) + add_edges):
			count = count + 1
	return count

def get_forest_prob_bf(edge, el):
	print len(el)
	pos = count_forests(fix_edge_add(edge, el))
	neg = count_forests(fix_edge_del(edge, el))
	return float(pos)/float(pos + neg)

#print count_forests(gen_grid(4))

#print get_forest_prob_bf(("0-0", "0-1"), gen_grid(4))

def make_transitive_closure(graph, n):
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
	total_verts = set([])
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
			total_verts = total_verts.union(test)
	#print output
	#print total_verts
	for i in range(0, n):
		if str(i) not in total_verts:
			output.append(frozenset([str(i)]))
	#		print i
	return frozenset(output)

def check_fixed(edge, fixed_edges):
	(a, b) = edge
	if (a, b) in fixed_edges:
		return True
	if (b, a) in fixed_edges:
		return True
	return False

def dp_grid_cnt(n, add_edges, remove_edges):
	state = {}
	edges = []
	fixed_edges = remove_edges + add_edges
	must_add_base = []
	for j in range(0, n-1):
		candidate = (name_node(0, j), name_node(0, j+1))
		if not check_fixed(candidate, fixed_edges):
			edges.append((str(j), str(j+1)))
		if check_fixed(candidate, add_edges):
			must_add_base.append((str(j), str(j+1)))
		print edges
		print must_add_base
	for el in powerset(edges):
		graph = bld_graph(list(el) + list(must_add_base))
		graph = make_transitive_closure(graph, n)
		state[graph] = 1
		#state.append(graph)
	print state
	for i in (range(1, n)):
		edges = []
		manip_add_edges = []
		for j in range(0, n):
			#do edge filtering here
			if not check_fixed((name_node(i-1, j), name_node(i, j)), fixed_edges):
				edges.append(("base-" + str(j), str(j)))
			if check_fixed((name_node(i-1, j), name_node(i, j)), add_edges):
				manip_add_edges.append(("base-" + str(j), str(j)))
			
			if (j < n-1) and not check_fixed((name_node(i, j), name_node(i, j+1)), fixed_edges):
				edges.append((str(j), str(j+1)))
			if (j < n-1) and check_fixed((name_node(i, j), name_node(i, j+1)), add_edges):
				manip_add_edges.append((str(j), str(j+1)))
		next_state = {}
		print "foo" + str(edges)
		print "bar" + str(manip_add_edges)
		for graph in (state.keys()):
			graph_edges = []
			for component in graph:
				foo = list(component)
				for z in range(0, len(foo)-1):
					graph_edges.append(("base-" + str(foo[z]), "base-" + str(foo[z+1])))
			print "CURRENT GRAPH"
			print graph
			print graph_edges
			counter = 0
			for el in powerset(edges):
				el = list(el) + manip_add_edges
				if check_is_forest(el + graph_edges):
					#compatible
					print "el = " + str(el)
					counter = counter + 1
					cur_index = make_transitive_closure(bld_graph(el + graph_edges), n)
					if cur_index in next_state.keys():
						next_state[cur_index] = next_state[cur_index] + state[graph]
					else:
						next_state[cur_index] = state[graph]
			print counter
		state = next_state
		print "PRINTING STATE"
		for (k, v) in state.iteritems():
			print (k, v)

	count = 0
	for graph in state:
		count = count + state[graph]
	return count

print dp_grid_cnt(3, [("0-0", "0-1")], [("1-1", "1-2")])
print "ASFDSDFS"
print bf_count_forests(gen_grid(3), [("0-0", "0-1")], [("1-1", "1-2")])




