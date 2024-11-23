from dataclasses import dataclass
from typing import List, Self

from networkx.drawing.nx_agraph import graphviz_layout
import networkx as nx
from pydantic import BaseModel, model_validator


class Position(BaseModel):
    x: float
    y: float


class Node(BaseModel):
    id: str
    position: Position = Position(x=0, y=0)


class Edge(BaseModel):
    source: str
    target: str
    sourceHandle: str


class Flowchart(BaseModel):
    nodes: List[Node]
    Edges: List[Edge]

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        graph = nx.DiGraph()

        for node in self.nodes:
            graph.add_node(node.id)

        for edge in self.edges:
            graph.add_edge(edge.source, edge.target)

        pos = graphviz_layout(graph, prog="dot")

        if __debug__:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8, 8))
            nx.draw(graph, pos, with_labels=True, node_size=700, node_color="lightgreen", font_size=12,
                    font_weight="bold")
            plt.show()
        for node_id, node_position in pos.items():
            for node in self.nodes:
                if node.id == node_id:
                    node.position.x, node.position.y = node_position
        return self


def get_positions(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    pos = graphviz_layout(G, prog="dot")
    if __debug__:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 8))
        nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightgreen", font_size=12,
                font_weight="bold")
        plt.show()
    return pos


def main():
    nodes = [3, 1, 2, 4, 5, 6]
    edges = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (5, 6)]
    get_positions(nodes, edges)

    # G = nx.DiGraph()
    # G.add_edges_from(edges)
    # print_hierarchy(G, 1)


if __name__ == "__main__":
    main()
