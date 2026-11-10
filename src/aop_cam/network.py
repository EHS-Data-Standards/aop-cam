"""Merge AOP models into a network and traverse it.

GO-CAM models merge on shared ontology identifiers; AOP models converted
from AOP-Wiki merge on shared key events (the aopwiki_id crosswalk). This
module builds that merged view - e.g. the four respiratory AOPs (148, 411,
424, 425) merge into the network of the SOMA paper's Figure 2 - and offers
the traversal checks the schema promises: initial nodes should be the
asserted molecular initiating events, terminal nodes the adverse outcomes,
and every node should lie on a path from an MIE.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from aop_cam.datamodel.aop_cam import ModelCollection


@dataclass
class MergedNode:
    key: str  # merge key: aopwiki_id when present, else the node id
    title: str
    event_types: set[str] = field(default_factory=set)
    models: set[str] = field(default_factory=set)


@dataclass
class MergedEdge:
    upstream: str
    downstream: str
    predicate: str
    aopwiki_ker_id: str | None
    models: set[str] = field(default_factory=set)


@dataclass
class MergedNetwork:
    nodes: dict[str, MergedNode] = field(default_factory=dict)
    edges: dict[tuple, MergedEdge] = field(default_factory=dict)

    def initial_nodes(self) -> set[str]:
        """Nodes with no incoming edge (should be the MIEs)."""
        targets = {e.downstream for e in self.edges.values()}
        return set(self.nodes) - targets

    def terminal_nodes(self) -> set[str]:
        """Nodes with no outgoing edge (should be the adverse outcomes)."""
        sources = {e.upstream for e in self.edges.values()}
        return set(self.nodes) - sources

    def reachable_from(self, starts: set[str]) -> set[str]:
        out: dict[str, set[str]] = {}
        for e in self.edges.values():
            out.setdefault(e.upstream, set()).add(e.downstream)
        seen = set(starts)
        frontier = list(starts)
        while frontier:
            for nxt in out.get(frontier.pop(), ()):  # depth-first; order moot
                if nxt not in seen:
                    seen.add(nxt)
                    frontier.append(nxt)
        return seen


def merge(collection: ModelCollection) -> MergedNetwork:
    """Merge every model in the collection on shared key events."""
    network = MergedNetwork()
    for model in collection.models:
        model_key = str(model.aopwiki_id or model.id)
        node_key = {}  # model-local node id -> merge key
        for ke in model.key_events:
            key = str(ke.aopwiki_id or ke.id)
            node_key[str(ke.id)] = key
            node = network.nodes.setdefault(key, MergedNode(key=key, title=ke.title))
            if ke.event_type is not None:
                node.event_types.add(str(ke.event_type))
            node.models.add(model_key)
        for ke in model.key_events:
            for ca in ke.causal_associations:
                up = node_key[str(ke.id)]
                down = node_key[str(ca.downstream_event)]
                ekey = (up, down, str(ca.predicate))
                edge = network.edges.setdefault(
                    ekey,
                    MergedEdge(
                        upstream=up,
                        downstream=down,
                        predicate=str(ca.predicate),
                        aopwiki_ker_id=str(ca.aopwiki_ker_id)
                        if ca.aopwiki_ker_id
                        else None,
                    ),
                )
                edge.models.add(model_key)
    return network


def event_type_position_errors(collection: ModelCollection) -> list[str]:
    """Check each model's asserted event types against graph position:
    an MIE must have no incoming causal association within its model, an
    adverse outcome no outgoing one. Returns human-readable violations."""
    errors = []
    for model in collection.models:
        targets = {
            str(ca.downstream_event)
            for ke in model.key_events
            for ca in ke.causal_associations
        }
        for ke in model.key_events:
            etype = str(ke.event_type) if ke.event_type else None
            if etype == "molecular_initiating_event" and str(ke.id) in targets:
                errors.append(
                    f"{model.id}: MIE {ke.id} has an incoming causal association"
                )
            if etype == "adverse_outcome" and ke.causal_associations:
                errors.append(
                    f"{model.id}: adverse outcome {ke.id} has outgoing "
                    "causal associations"
                )
    return errors
