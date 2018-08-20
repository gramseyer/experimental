

def get_root(tree):
	minimum = None
	for i in tree:
		if (minimum == None):
			minimum = i
		else:
			if i < minimum:
				minimum = i
	return minimum

def get_nbs(index, forest_edges):
	nbs = []
	for (u, v) in forest_edges:
		if index == u:
			nbs.append(v)
		if index == v:
			nbs.append(u)
	return nbs

def get_isolated_verts(forest_edges, graph_edges):
	#this assumes g doesn't have isolated verts bc that's dumb
	forest_span = set([])
	graph_span = set([])
	for (u, v) in forest_edges:
		forest_span.add(u)
		forest_span.add(v)
	for (u, v) in graph_edges:
		graph_span.add(u)
		graph_span.add(v)
	return graph_span - forest_span

def tree_index_dicts(forest_edges, graph_edges):
	trees = []
	for (u, v) in forest_edges:
		l = None
		r = None
		for t in trees:
			if u in t:
				l = t
			if v in t:
				r = t
		if l == None and r == None:
			trees.append(set([u, v]))
		elif l == None:
			r.add(u)
		elif r == None:
			l.add(v)
		else:
			trees.remove(l)
			trees.remove(r)
			trees.append(l.union(r))
	for isolated_vert in get_isolated_verts(forest_edges, graph_edges):
		trees.append(set([isolated_vert]))

	#print trees
	processed = {}
	roots = []
	for t in trees:
		root = get_root(t)
		roots.append(root)
		working_set = [root]
		while not (working_set == []):
			current = working_set.pop(0)
			nbs = get_nbs(current, forest_edges)
			processed[current] = []
			for nb in nbs:
				if nb in processed.keys():
					#parent
					continue
				processed[current].append(nb)
				working_set.append(nb)
	#print roots
	output = {}
	#print processed
	for (k, v) in processed.iteritems():
		output[k] = {}
		for child in v:
			output[k][child] = child

	#print "output_start is " + str(output)
	working = list(output.keys())
	#print working
	while not len(working) == 0:
		current = working.pop(0)
		#print current
		cur_map = output[current]
		descendants = cur_map.keys()
		flag = False
		for descendant in descendants:
			desc_map = output[descendant]
			for grand_desc in desc_map.keys():
				if not (grand_desc in descendants):
					cur_map[grand_desc] = cur_map[descendant]
					flag = True
		if flag:
			nbs = get_nbs(current, forest_edges)
			for nb in nbs:
				working.append(nb)
			working.append(current)
	#print "output end is " + str(output)
	return (roots, output)
	# return (list of roots, map from u to (map from v to first child on path from u to v)

def is_non_forest_edge(edge, forest_edges):
	(u, v) = edge
	if (u, v) in forest_edges:
		return True
	if (v, u) in forest_edges:
		return True
	return False

def get_non_forest_edges(forest_edges, graph_edges):
	out = []
	for e in graph_edges:
		if is_non_forest_edge(e, forest_edges):
			out.append(e)
	return out

def forest_to_cn(forest_edges, graph_edges):
	output_cn = []
	(roots, tree_root_maps) = tree_index_dicts(forest_edges, graph_edges)
	for (u, v) in graph_edges:
		#print "edge is " + str((u, v))
		u_r = None
		v_r = None
		for root in roots:
			if u in tree_root_maps[root].keys() or u == root:
				u_r = root
			if v in tree_root_maps[root].keys() or v == root:
				v_r = root
		#print (u_r, v_r)
		if u_r < v_r:
			output_cn.append((v, u))
			continue
		if v_r < u_r:
			output_cn.append((u, v))
			continue
		if v in tree_root_maps[u].keys():
			#v is descendant of u from root
			x = tree_root_maps[u][v]
			if x <= v:
				output_cn.append((u, v))
			else:
				output_cn.append((v, u))
			continue
		if u in tree_root_maps[v].keys():
			#converse
			x = tree_root_maps[v][u]
			if x <= u:
				output_cn.append((v, u))
			else:
				output_cn.append((u, v))
			continue
		#print "common ancestor"
		lca = u_r # == v_r
		u_a = lca
		v_a = lca
		while True:
			u_a = tree_root_maps[lca][u]
			v_a = tree_root_maps[lca][v]
			if u_a == v_a:
				lca = u_a
			else:
				break
		if u_a > v_a:
			output_cn.append((u, v))
		else:
			output_cn.append((v, u))
	return output_cn

simple_f = [(1, 3), (2, 4), (1, 2)]
simple_g = [(1,2), (2, 3), (1, 3), (3, 4), (2, 4)]

#f_edges = [(1, 2), (2, 3), (2, 4), (5, 6), (6, 7), (1, 7)]
#g_edges = f_edges + [(3, 4), (4, 5)]

#print tree_index_dicts(f_edges, g_edges)
print forest_to_cn(simple_f, simple_g)

