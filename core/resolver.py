from core.meta import load_meta


# Build Graph

def build_graph(package, graph, visited):
   if package in visited:
       return
   visited.add(package)
   meta = load_meta(package)
   if not meta:
       raise Exception(f"Package '{package}' not found.")
   deps = meta.get("dependencies", [])
   graph[package] = deps
   for dep in deps:
       build_graph(dep, graph, visited)


# Topological Sort
def topo_sort(graph):
    visited = set()
    temp = set()
    order = []
    def dfs(node):
        if node in temp:
            raise Exception("Circular dependency detected!")
        if node in visited:
            return
        temp.add(node)
        for dep in graph.get(node,[]):
            dfs(dep)
        temp.remove(node)
        visited.add(node)
        order.append(node)
    for node in graph:
        dfs(node)
    return order