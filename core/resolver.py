import re
from core.meta import load_meta
from core.versions import resolve_version

# Build Graph

def build_graph(package_tuple, graph, visited):
   name, version = package_tuple
   if package_tuple in visited:
       return
   visited.add(package_tuple)
   meta = load_meta(name, version)
   if not meta:
       raise Exception(f"Package '{name}' not found.")
   
   resolved_deps = []

   for dep in meta.get("dependencies", []):
       dep_name, op, ver = parse_dependency(dep)
       resolved_version = resolve_version(dep_name, op, ver)
       
       if not resolved_version:
           raise Exception(f"Cannot resolve {dep}")
       resolved_deps.append((dep_name, resolved_version))


   graph[package_tuple] = resolved_deps
   for dep in resolved_deps:
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

def parse_dependency(dep_str):
    match = re.match(r"^([a-zA-Z0-9_\-]+)(?:([<>=!]=?)(.+))?$", dep_str)

    if not match:
        raise Exception(f"Invalid Package: {dep_str}")
    
    name = match.group(1)
    op = match.group(2)
    ver = match.group(3)
    print(name, op, ver)

    return name, op, ver