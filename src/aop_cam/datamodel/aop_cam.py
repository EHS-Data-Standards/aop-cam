# Auto generated from aop_cam.yaml by pythongen.py version: 0.0.1
# Schema: aop_cam
#
# id: https://w3id.org/EHS-Data-Standards/aop-cam
# description: Adverse Outcome Pathways represented as causal activity models, following the GO-CAM paradigm: an AOP is a model (a named causal graph), each Key Event is a node defined by associations to ontology terms in context, each Key Event Relationship is a typed causal association drawn from the Relation Ontology, and evidence attaches to individual assertions rather than to whole records. The schema mirrors the GO-CAM pattern (Association hierarchy, per-assertion evidence, model lifecycle) without importing its gene-product machinery: a Key Event is not a molecular Activity, and the AOP extensions GO-CAM lacks - direction of change as node state, levels of biological organization up to population, and compositional outcome grounding with optional precomposed-term mappings - are first-class here. Instances can be loaded from AOP-Wiki exports; aopwiki_id slots keep the crosswalk.
# license: BSD-3

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Date, Datetime, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE, XSDDate, XSDDateTime

metamodel_version = "1.12.0"
version = None

# Namespaces
AOPWIKI = CurieNamespace('AOPWIKI', 'https://aopwiki.org/')
CHEBI = CurieNamespace('CHEBI', 'http://purl.obolibrary.org/obo/CHEBI_')
CL = CurieNamespace('CL', 'http://purl.obolibrary.org/obo/CL_')
DOI = CurieNamespace('DOI', 'http://doi.org/')
ECO = CurieNamespace('ECO', 'http://purl.obolibrary.org/obo/ECO_')
GO = CurieNamespace('GO', 'http://purl.obolibrary.org/obo/GO_')
HP = CurieNamespace('HP', 'http://purl.obolibrary.org/obo/HP_')
MESH = CurieNamespace('MESH', 'http://id.nlm.nih.gov/mesh/')
MONDO = CurieNamespace('MONDO', 'http://purl.obolibrary.org/obo/MONDO_')
NCBITAXON = CurieNamespace('NCBITaxon', 'http://purl.obolibrary.org/obo/NCBITaxon_')
PATO = CurieNamespace('PATO', 'http://purl.obolibrary.org/obo/PATO_')
PMID = CurieNamespace('PMID', 'http://identifiers.org/pubmed/')
PR = CurieNamespace('PR', 'http://purl.obolibrary.org/obo/PR_')
RO = CurieNamespace('RO', 'http://purl.obolibrary.org/obo/RO_')
UBERON = CurieNamespace('UBERON', 'http://purl.obolibrary.org/obo/UBERON_')
UPHENO = CurieNamespace('UPHENO', 'http://purl.obolibrary.org/obo/UPHENO_')
AOP_CAM = CurieNamespace('aop_cam', 'https://w3id.org/EHS-Data-Standards/aop-cam/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = AOP_CAM


# Types

# Class references
class AopModelId(URIorCURIE):
    pass


class KeyEventNodeId(URIorCURIE):
    pass


class TermObjectId(URIorCURIE):
    pass


class ProcessTermObjectId(TermObjectId):
    pass


class ObjectTermObjectId(TermObjectId):
    pass


class DirectionTermObjectId(TermObjectId):
    pass


class CellTypeTermObjectId(TermObjectId):
    pass


class AnatomyTermObjectId(TermObjectId):
    pass


class TaxonTermObjectId(TermObjectId):
    pass


class StressorTermObjectId(TermObjectId):
    pass


@dataclass(repr=False)
class ModelCollection(YAMLRoot):
    """
    Root container for a set of AOP causal activity models, e.g. one release of models converted from an AOP-Wiki
    snapshot, or a curated network slice.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["ModelCollection"]
    class_class_curie: ClassVar[str] = "aop_cam:ModelCollection"
    class_name: ClassVar[str] = "ModelCollection"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.ModelCollection

    models: Optional[Union[dict[Union[str, AopModelId], Union[dict, "AopModel"]], list[Union[dict, "AopModel"]]]] = empty_dict()
    snapshot_date: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="models", slot_type=AopModel, key_name="id", keyed=True)

        if self.snapshot_date is not None and not isinstance(self.snapshot_date, XSDDate):
            self.snapshot_date = XSDDate(self.snapshot_date)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AopModel(YAMLRoot):
    """
    One Adverse Outcome Pathway as a causal activity model: a named graph of Key Event nodes connected by typed causal
    associations. Initial nodes (no incoming causal association) are molecular initiating events; terminal nodes (no
    outgoing causal association) are adverse outcomes. The event_type on each node states the curator's intent; the
    graph position is checkable against it.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["AopModel"]
    class_class_curie: ClassVar[str] = "aop_cam:AopModel"
    class_name: ClassVar[str] = "AopModel"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.AopModel

    id: Union[str, AopModelId] = None
    title: str = None
    description: Optional[str] = None
    aopwiki_id: Optional[str] = None
    status: Optional[Union[str, "ModelStateEnum"]] = None
    oecd_status: Optional[str] = None
    taxa: Optional[Union[dict[Union[str, TaxonTermObjectId], Union[dict, "TaxonTermObject"]], list[Union[dict, "TaxonTermObject"]]]] = empty_dict()
    key_events: Optional[Union[dict[Union[str, KeyEventNodeId], Union[dict, "KeyEventNode"]], list[Union[dict, "KeyEventNode"]]]] = empty_dict()
    stressors: Optional[Union[dict[Union[str, StressorTermObjectId], Union[dict, "StressorTermObject"]], list[Union[dict, "StressorTermObject"]]]] = empty_dict()
    comments: Optional[Union[str, list[str]]] = empty_list()
    provenances: Optional[Union[Union[dict, "ProvenanceInfo"], list[Union[dict, "ProvenanceInfo"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AopModelId):
            self.id = AopModelId(self.id)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.aopwiki_id is not None and not isinstance(self.aopwiki_id, str):
            self.aopwiki_id = str(self.aopwiki_id)

        if self.status is not None and not isinstance(self.status, ModelStateEnum):
            self.status = ModelStateEnum(self.status)

        if self.oecd_status is not None and not isinstance(self.oecd_status, str):
            self.oecd_status = str(self.oecd_status)

        self._normalize_inlined_as_list(slot_name="taxa", slot_type=TaxonTermObject, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="key_events", slot_type=KeyEventNode, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="stressors", slot_type=StressorTermObject, key_name="id", keyed=True)

        if not isinstance(self.comments, list):
            self.comments = [self.comments] if self.comments is not None else []
        self.comments = [v if isinstance(v, str) else str(v) for v in self.comments]

        if not isinstance(self.provenances, list):
            self.provenances = [self.provenances] if self.provenances is not None else []
        self.provenances = [v if isinstance(v, ProvenanceInfo) else ProvenanceInfo(**as_dict(v)) for v in self.provenances]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class KeyEventNode(YAMLRoot):
    """
    One Key Event as a node in a causal activity model. The node itself is only an identifier and a label; its meaning
    comes from its associations - the biological process affected, the object acted on, the direction of change, and
    the cellular and anatomical context - each of which can carry its own evidence. An adverse outcome is a terminal
    KeyEventNode: its composition defines it, and outcome_mappings optionally decorate it with precomposed phenotype
    or disease terms where any exist.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["KeyEventNode"]
    class_class_curie: ClassVar[str] = "aop_cam:KeyEventNode"
    class_name: ClassVar[str] = "KeyEventNode"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.KeyEventNode

    id: Union[str, KeyEventNodeId] = None
    title: str = None
    aopwiki_id: Optional[str] = None
    event_type: Optional[Union[str, "EventTypeEnum"]] = None
    level_of_biological_organization: Optional[Union[str, "LevelOfBiologicalOrganizationEnum"]] = None
    process: Optional[Union[dict, "ProcessAssociation"]] = None
    object: Optional[Union[dict, "ObjectAssociation"]] = None
    direction: Optional[Union[dict, "DirectionAssociation"]] = None
    occurs_in_cell_type: Optional[Union[dict, "CellTypeAssociation"]] = None
    occurs_in_anatomy: Optional[Union[dict, "GrossAnatomyAssociation"]] = None
    causal_associations: Optional[Union[Union[dict, "CausalAssociation"], list[Union[dict, "CausalAssociation"]]]] = empty_list()
    outcome_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    provenances: Optional[Union[Union[dict, "ProvenanceInfo"], list[Union[dict, "ProvenanceInfo"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, KeyEventNodeId):
            self.id = KeyEventNodeId(self.id)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self.aopwiki_id is not None and not isinstance(self.aopwiki_id, str):
            self.aopwiki_id = str(self.aopwiki_id)

        if self.event_type is not None and not isinstance(self.event_type, EventTypeEnum):
            self.event_type = EventTypeEnum(self.event_type)

        if self.level_of_biological_organization is not None and not isinstance(self.level_of_biological_organization, LevelOfBiologicalOrganizationEnum):
            self.level_of_biological_organization = LevelOfBiologicalOrganizationEnum(self.level_of_biological_organization)

        if self.process is not None and not isinstance(self.process, ProcessAssociation):
            self.process = ProcessAssociation(**as_dict(self.process))

        if self.object is not None and not isinstance(self.object, ObjectAssociation):
            self.object = ObjectAssociation(**as_dict(self.object))

        if self.direction is not None and not isinstance(self.direction, DirectionAssociation):
            self.direction = DirectionAssociation(**as_dict(self.direction))

        if self.occurs_in_cell_type is not None and not isinstance(self.occurs_in_cell_type, CellTypeAssociation):
            self.occurs_in_cell_type = CellTypeAssociation(**as_dict(self.occurs_in_cell_type))

        if self.occurs_in_anatomy is not None and not isinstance(self.occurs_in_anatomy, GrossAnatomyAssociation):
            self.occurs_in_anatomy = GrossAnatomyAssociation(**as_dict(self.occurs_in_anatomy))

        self._normalize_inlined_as_list(slot_name="causal_associations", slot_type=CausalAssociation, key_name="predicate", keyed=False)

        if not isinstance(self.outcome_mappings, list):
            self.outcome_mappings = [self.outcome_mappings] if self.outcome_mappings is not None else []
        self.outcome_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.outcome_mappings]

        if not isinstance(self.provenances, list):
            self.provenances = [self.provenances] if self.provenances is not None else []
        self.provenances = [v if isinstance(v, ProvenanceInfo) else ProvenanceInfo(**as_dict(v)) for v in self.provenances]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Association(YAMLRoot):
    """
    An individual assertion in a model, carrying its own evidence and provenance. Every term assignment and every
    causal edge is an Association subtype, so support attaches to the claim itself rather than to the record that
    contains it.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["Association"]
    class_class_curie: ClassVar[str] = "aop_cam:Association"
    class_name: ClassVar[str] = "Association"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.Association

    type: Optional[str] = None
    evidence: Optional[Union[Union[dict, "EvidenceItem"], list[Union[dict, "EvidenceItem"]]]] = empty_list()
    provenances: Optional[Union[Union[dict, "ProvenanceInfo"], list[Union[dict, "ProvenanceInfo"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        self.type = str(self.class_name)

        if not isinstance(self.evidence, list):
            self.evidence = [self.evidence] if self.evidence is not None else []
        self.evidence = [v if isinstance(v, EvidenceItem) else EvidenceItem(**as_dict(v)) for v in self.evidence]

        if not isinstance(self.provenances, list):
            self.provenances = [self.provenances] if self.provenances is not None else []
        self.provenances = [v if isinstance(v, ProvenanceInfo) else ProvenanceInfo(**as_dict(v)) for v in self.provenances]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class TermAssociation(Association):
    """
    An association between a node and an ontology term. Abstract; use the typed subclasses so each dimension
    constrains its vocabulary.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["TermAssociation"]
    class_class_curie: ClassVar[str] = "aop_cam:TermAssociation"
    class_name: ClassVar[str] = "TermAssociation"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.TermAssociation

    term: Optional[Union[dict, "TermObject"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.term is not None and not isinstance(self.term, TermObject):
            self.term = TermObject(**as_dict(self.term))

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class ProcessAssociation(TermAssociation):
    """
    Associates a key event with the biological process it perturbs.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["ProcessAssociation"]
    class_class_curie: ClassVar[str] = "aop_cam:ProcessAssociation"
    class_name: ClassVar[str] = "ProcessAssociation"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.ProcessAssociation

    term: Optional[Union[dict, "ProcessTermObject"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.term is not None and not isinstance(self.term, ProcessTermObject):
            self.term = ProcessTermObject(**as_dict(self.term))

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class ObjectAssociation(TermAssociation):
    """
    Associates a key event with the biological object acted on (a protein, chemical, cell component, or other entity).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["ObjectAssociation"]
    class_class_curie: ClassVar[str] = "aop_cam:ObjectAssociation"
    class_name: ClassVar[str] = "ObjectAssociation"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.ObjectAssociation

    term: Optional[Union[dict, "ObjectTermObject"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.term is not None and not isinstance(self.term, ObjectTermObject):
            self.term = ObjectTermObject(**as_dict(self.term))

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class DirectionAssociation(TermAssociation):
    """
    Associates a key event with the direction of change, as a PATO quality (e.g. increased amount, decreased
    functionality). Together with the process or object this forms the entity+quality decomposition of the event.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["DirectionAssociation"]
    class_class_curie: ClassVar[str] = "aop_cam:DirectionAssociation"
    class_name: ClassVar[str] = "DirectionAssociation"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.DirectionAssociation

    term: Optional[Union[dict, "DirectionTermObject"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.term is not None and not isinstance(self.term, DirectionTermObject):
            self.term = DirectionTermObject(**as_dict(self.term))

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class CellTypeAssociation(TermAssociation):
    """
    The cell type in which the key event occurs.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["CellTypeAssociation"]
    class_class_curie: ClassVar[str] = "aop_cam:CellTypeAssociation"
    class_name: ClassVar[str] = "CellTypeAssociation"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.CellTypeAssociation

    term: Optional[Union[dict, "CellTypeTermObject"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.term is not None and not isinstance(self.term, CellTypeTermObject):
            self.term = CellTypeTermObject(**as_dict(self.term))

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class GrossAnatomyAssociation(TermAssociation):
    """
    The anatomical location in which the key event occurs.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["GrossAnatomyAssociation"]
    class_class_curie: ClassVar[str] = "aop_cam:GrossAnatomyAssociation"
    class_name: ClassVar[str] = "GrossAnatomyAssociation"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.GrossAnatomyAssociation

    term: Optional[Union[dict, "AnatomyTermObject"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.term is not None and not isinstance(self.term, AnatomyTermObject):
            self.term = AnatomyTermObject(**as_dict(self.term))

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class CausalAssociation(Association):
    """
    A typed causal edge between two key event nodes: the AOP framework's Key Event Relationship, with the relation
    drawn from the causal branch of the Relation Ontology. AOP-Wiki adjacency maps onto the predicate: adjacent KERs
    are immediately causally upstream of; non-adjacent KERs are causally upstream of; use the positive/negative effect
    or regulates forms where the direction of influence is curated.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["CausalAssociation"]
    class_class_curie: ClassVar[str] = "aop_cam:CausalAssociation"
    class_name: ClassVar[str] = "CausalAssociation"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.CausalAssociation

    predicate: Union[str, "CausalPredicateEnum"] = None
    downstream_event: Union[str, KeyEventNodeId] = None
    aopwiki_ker_id: Optional[str] = None
    evidence_level: Optional[Union[str, "ConfidenceLevelEnum"]] = None
    quantitative_understanding: Optional[Union[str, "ConfidenceLevelEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, CausalPredicateEnum):
            self.predicate = CausalPredicateEnum(self.predicate)

        if self._is_empty(self.downstream_event):
            self.MissingRequiredField("downstream_event")
        if not isinstance(self.downstream_event, KeyEventNodeId):
            self.downstream_event = KeyEventNodeId(self.downstream_event)

        if self.aopwiki_ker_id is not None and not isinstance(self.aopwiki_ker_id, str):
            self.aopwiki_ker_id = str(self.aopwiki_ker_id)

        if self.evidence_level is not None and not isinstance(self.evidence_level, ConfidenceLevelEnum):
            self.evidence_level = ConfidenceLevelEnum(self.evidence_level)

        if self.quantitative_understanding is not None and not isinstance(self.quantitative_understanding, ConfidenceLevelEnum):
            self.quantitative_understanding = ConfidenceLevelEnum(self.quantitative_understanding)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class EvidenceItem(YAMLRoot):
    """
    One piece of evidence supporting an assertion: an ECO evidence type, a publication, and optionally the supporting
    records themselves - for example the identifier of a SOMA assay whose measurements inform the assertion. This is
    the joint between the knowledge layer (this schema) and the experimental evidence layer (SOMA): an assay's
    informs_on_key_event link materializes here as evidence on the node's association.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["EvidenceItem"]
    class_class_curie: ClassVar[str] = "aop_cam:EvidenceItem"
    class_name: ClassVar[str] = "EvidenceItem"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.EvidenceItem

    term: Optional[Union[str, URIorCURIE]] = None
    reference: Optional[Union[str, URIorCURIE]] = None
    supporting_objects: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    description: Optional[str] = None
    provenances: Optional[Union[Union[dict, "ProvenanceInfo"], list[Union[dict, "ProvenanceInfo"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.term is not None and not isinstance(self.term, URIorCURIE):
            self.term = URIorCURIE(self.term)

        if self.reference is not None and not isinstance(self.reference, URIorCURIE):
            self.reference = URIorCURIE(self.reference)

        if not isinstance(self.supporting_objects, list):
            self.supporting_objects = [self.supporting_objects] if self.supporting_objects is not None else []
        self.supporting_objects = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.supporting_objects]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.provenances, list):
            self.provenances = [self.provenances] if self.provenances is not None else []
        self.provenances = [v if isinstance(v, ProvenanceInfo) else ProvenanceInfo(**as_dict(v)) for v in self.provenances]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProvenanceInfo(YAMLRoot):
    """
    Who made or changed an assertion, and when.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["ProvenanceInfo"]
    class_class_curie: ClassVar[str] = "aop_cam:ProvenanceInfo"
    class_name: ClassVar[str] = "ProvenanceInfo"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.ProvenanceInfo

    contributor: Optional[str] = None
    created: Optional[Union[str, XSDDateTime]] = None
    modified: Optional[Union[str, XSDDateTime]] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.contributor is not None and not isinstance(self.contributor, str):
            self.contributor = str(self.contributor)

        if self.created is not None and not isinstance(self.created, XSDDateTime):
            self.created = XSDDateTime(self.created)

        if self.modified is not None and not isinstance(self.modified, XSDDateTime):
            self.modified = XSDDateTime(self.modified)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TermObject(YAMLRoot):
    """
    A pointer to an ontology term: an identifier plus its label. Typed subclasses constrain which vocabulary each slot
    draws from.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["TermObject"]
    class_class_curie: ClassVar[str] = "aop_cam:TermObject"
    class_name: ClassVar[str] = "TermObject"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.TermObject

    id: Union[str, TermObjectId] = None
    label: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TermObjectId):
            self.id = TermObjectId(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProcessTermObject(TermObject):
    """
    A biological process term (GO preferred; MESH accepted for AOP-Wiki conversion).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["ProcessTermObject"]
    class_class_curie: ClassVar[str] = "aop_cam:ProcessTermObject"
    class_name: ClassVar[str] = "ProcessTermObject"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.ProcessTermObject

    id: Union[str, ProcessTermObjectId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcessTermObjectId):
            self.id = ProcessTermObjectId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ObjectTermObject(TermObject):
    """
    A biological object term (protein, chemical, or other entity).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["ObjectTermObject"]
    class_class_curie: ClassVar[str] = "aop_cam:ObjectTermObject"
    class_name: ClassVar[str] = "ObjectTermObject"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.ObjectTermObject

    id: Union[str, ObjectTermObjectId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ObjectTermObjectId):
            self.id = ObjectTermObjectId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DirectionTermObject(TermObject):
    """
    A PATO quality term for the direction of change.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["DirectionTermObject"]
    class_class_curie: ClassVar[str] = "aop_cam:DirectionTermObject"
    class_name: ClassVar[str] = "DirectionTermObject"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.DirectionTermObject

    id: Union[str, DirectionTermObjectId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DirectionTermObjectId):
            self.id = DirectionTermObjectId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CellTypeTermObject(TermObject):
    """
    A Cell Ontology term.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["CellTypeTermObject"]
    class_class_curie: ClassVar[str] = "aop_cam:CellTypeTermObject"
    class_name: ClassVar[str] = "CellTypeTermObject"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.CellTypeTermObject

    id: Union[str, CellTypeTermObjectId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CellTypeTermObjectId):
            self.id = CellTypeTermObjectId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AnatomyTermObject(TermObject):
    """
    An UBERON anatomy term.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["AnatomyTermObject"]
    class_class_curie: ClassVar[str] = "aop_cam:AnatomyTermObject"
    class_name: ClassVar[str] = "AnatomyTermObject"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.AnatomyTermObject

    id: Union[str, AnatomyTermObjectId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnatomyTermObjectId):
            self.id = AnatomyTermObjectId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TaxonTermObject(TermObject):
    """
    An NCBI Taxonomy term.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["TaxonTermObject"]
    class_class_curie: ClassVar[str] = "aop_cam:TaxonTermObject"
    class_name: ClassVar[str] = "TaxonTermObject"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.TaxonTermObject

    id: Union[str, TaxonTermObjectId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TaxonTermObjectId):
            self.id = TaxonTermObjectId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StressorTermObject(TermObject):
    """
    A stressor as an ontology term reference where one exists (CHEBI chemical, or an environmental material);
    free-text stressor names from AOP-Wiki that cannot be grounded keep their label with an AOPWIKI-prefixed id.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AOP_CAM["StressorTermObject"]
    class_class_curie: ClassVar[str] = "aop_cam:StressorTermObject"
    class_name: ClassVar[str] = "StressorTermObject"
    class_model_uri: ClassVar[URIRef] = AOP_CAM.StressorTermObject

    id: Union[str, StressorTermObjectId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StressorTermObjectId):
            self.id = StressorTermObjectId(self.id)

        super().__post_init__(**kwargs)


# Enumerations
class ModelStateEnum(EnumDefinitionImpl):
    """
    Where the model is in its development life cycle (GO-CAM semantics).
    """
    development = PermissibleValue(
        text="development",
        description="Still being worked on; not guaranteed accurate or complete.")
    production = PermissibleValue(
        text="production",
        description="Declared ready for public consumption.")
    review = PermissibleValue(
        text="review",
        description="Marked for curator review.")
    archived = PermissibleValue(
        text="archived",
        description="Retained for reference; no longer maintained.")

    _defn = EnumDefinition(
        name="ModelStateEnum",
        description="Where the model is in its development life cycle (GO-CAM semantics).",
    )

class EventTypeEnum(EnumDefinitionImpl):
    """
    The curator-asserted role of a key event node in the pathway.
    """
    molecular_initiating_event = PermissibleValue(
        text="molecular_initiating_event",
        description="The initial perturbation; no incoming causal associations.")
    key_event = PermissibleValue(
        text="key_event",
        description="An intermediate measurable change.")
    adverse_outcome = PermissibleValue(
        text="adverse_outcome",
        description="The apical endpoint; no outgoing causal associations.")

    _defn = EnumDefinition(
        name="EventTypeEnum",
        description="The curator-asserted role of a key event node in the pathway.",
    )

class LevelOfBiologicalOrganizationEnum(EnumDefinitionImpl):
    """
    Levels of biological organization, following AOP-Wiki usage.
    """
    molecular = PermissibleValue(text="molecular")
    cellular = PermissibleValue(text="cellular")
    tissue = PermissibleValue(text="tissue")
    organ = PermissibleValue(text="organ")
    individual = PermissibleValue(text="individual")
    population = PermissibleValue(text="population")

    _defn = EnumDefinition(
        name="LevelOfBiologicalOrganizationEnum",
        description="Levels of biological organization, following AOP-Wiki usage.",
    )

class CausalPredicateEnum(EnumDefinitionImpl):
    """
    The causal relation between two key events, drawn from the "causally upstream or within" branch of the Relation
    Ontology. Permissible values and meanings follow the GO-CAM schema's CausalPredicateEnum.
    """
    regulates = PermissibleValue(
        text="regulates",
        meaning=RO["0002211"])

    _defn = EnumDefinition(
        name="CausalPredicateEnum",
        description="""The causal relation between two key events, drawn from the \"causally upstream or within\" branch of the Relation Ontology. Permissible values and meanings follow the GO-CAM schema's CausalPredicateEnum.""",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "causally upstream of, positive effect",
            PermissibleValue(
                text="causally upstream of, positive effect",
                meaning=RO["0002304"]))
        setattr(cls, "causally upstream of, negative effect",
            PermissibleValue(
                text="causally upstream of, negative effect",
                meaning=RO["0002305"]))
        setattr(cls, "causally upstream of",
            PermissibleValue(
                text="causally upstream of",
                meaning=RO["0002411"]))
        setattr(cls, "immediately causally upstream of",
            PermissibleValue(
                text="immediately causally upstream of",
                meaning=RO["0002412"]))
        setattr(cls, "causally upstream of or within",
            PermissibleValue(
                text="causally upstream of or within",
                meaning=RO["0002418"]))
        setattr(cls, "negatively regulates",
            PermissibleValue(
                text="negatively regulates",
                meaning=RO["0002212"]))
        setattr(cls, "positively regulates",
            PermissibleValue(
                text="positively regulates",
                meaning=RO["0002213"]))

class ConfidenceLevelEnum(EnumDefinitionImpl):
    """
    Curated confidence levels, following AOP-Wiki usage.
    """
    high = PermissibleValue(text="high")
    moderate = PermissibleValue(text="moderate")
    low = PermissibleValue(text="low")
    not_specified = PermissibleValue(text="not_specified")

    _defn = EnumDefinition(
        name="ConfidenceLevelEnum",
        description="Curated confidence levels, following AOP-Wiki usage.",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=AOP_CAM.id, name="id", curie=AOP_CAM.curie('id'),
                   model_uri=AOP_CAM.id, domain=None, range=URIRef)

slots.label = Slot(uri=AOP_CAM.label, name="label", curie=AOP_CAM.curie('label'),
                   model_uri=AOP_CAM.label, domain=None, range=Optional[str])

slots.term = Slot(uri=AOP_CAM.term, name="term", curie=AOP_CAM.curie('term'),
                   model_uri=AOP_CAM.term, domain=None, range=Optional[Union[dict, TermObject]])

slots.modelCollection__models = Slot(uri=AOP_CAM.models, name="modelCollection__models", curie=AOP_CAM.curie('models'),
                   model_uri=AOP_CAM.modelCollection__models, domain=None, range=Optional[Union[dict[Union[str, AopModelId], Union[dict, AopModel]], list[Union[dict, AopModel]]]])

slots.modelCollection__snapshot_date = Slot(uri=AOP_CAM.snapshot_date, name="modelCollection__snapshot_date", curie=AOP_CAM.curie('snapshot_date'),
                   model_uri=AOP_CAM.modelCollection__snapshot_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.aopModel__id = Slot(uri=AOP_CAM.id, name="aopModel__id", curie=AOP_CAM.curie('id'),
                   model_uri=AOP_CAM.aopModel__id, domain=None, range=URIRef)

slots.aopModel__title = Slot(uri=DCTERMS.title, name="aopModel__title", curie=DCTERMS.curie('title'),
                   model_uri=AOP_CAM.aopModel__title, domain=None, range=str)

slots.aopModel__description = Slot(uri=AOP_CAM.description, name="aopModel__description", curie=AOP_CAM.curie('description'),
                   model_uri=AOP_CAM.aopModel__description, domain=None, range=Optional[str])

slots.aopModel__aopwiki_id = Slot(uri=AOP_CAM.aopwiki_id, name="aopModel__aopwiki_id", curie=AOP_CAM.curie('aopwiki_id'),
                   model_uri=AOP_CAM.aopModel__aopwiki_id, domain=None, range=Optional[str])

slots.aopModel__status = Slot(uri=AOP_CAM.status, name="aopModel__status", curie=AOP_CAM.curie('status'),
                   model_uri=AOP_CAM.aopModel__status, domain=None, range=Optional[Union[str, "ModelStateEnum"]])

slots.aopModel__oecd_status = Slot(uri=AOP_CAM.oecd_status, name="aopModel__oecd_status", curie=AOP_CAM.curie('oecd_status'),
                   model_uri=AOP_CAM.aopModel__oecd_status, domain=None, range=Optional[str])

slots.aopModel__taxa = Slot(uri=AOP_CAM.taxa, name="aopModel__taxa", curie=AOP_CAM.curie('taxa'),
                   model_uri=AOP_CAM.aopModel__taxa, domain=None, range=Optional[Union[dict[Union[str, TaxonTermObjectId], Union[dict, TaxonTermObject]], list[Union[dict, TaxonTermObject]]]])

slots.aopModel__key_events = Slot(uri=AOP_CAM.key_events, name="aopModel__key_events", curie=AOP_CAM.curie('key_events'),
                   model_uri=AOP_CAM.aopModel__key_events, domain=None, range=Optional[Union[dict[Union[str, KeyEventNodeId], Union[dict, KeyEventNode]], list[Union[dict, KeyEventNode]]]])

slots.aopModel__stressors = Slot(uri=AOP_CAM.stressors, name="aopModel__stressors", curie=AOP_CAM.curie('stressors'),
                   model_uri=AOP_CAM.aopModel__stressors, domain=None, range=Optional[Union[dict[Union[str, StressorTermObjectId], Union[dict, StressorTermObject]], list[Union[dict, StressorTermObject]]]])

slots.aopModel__comments = Slot(uri=AOP_CAM.comments, name="aopModel__comments", curie=AOP_CAM.curie('comments'),
                   model_uri=AOP_CAM.aopModel__comments, domain=None, range=Optional[Union[str, list[str]]])

slots.aopModel__provenances = Slot(uri=AOP_CAM.provenances, name="aopModel__provenances", curie=AOP_CAM.curie('provenances'),
                   model_uri=AOP_CAM.aopModel__provenances, domain=None, range=Optional[Union[Union[dict, ProvenanceInfo], list[Union[dict, ProvenanceInfo]]]])

slots.keyEventNode__id = Slot(uri=AOP_CAM.id, name="keyEventNode__id", curie=AOP_CAM.curie('id'),
                   model_uri=AOP_CAM.keyEventNode__id, domain=None, range=URIRef)

slots.keyEventNode__title = Slot(uri=AOP_CAM.title, name="keyEventNode__title", curie=AOP_CAM.curie('title'),
                   model_uri=AOP_CAM.keyEventNode__title, domain=None, range=str)

slots.keyEventNode__aopwiki_id = Slot(uri=AOP_CAM.aopwiki_id, name="keyEventNode__aopwiki_id", curie=AOP_CAM.curie('aopwiki_id'),
                   model_uri=AOP_CAM.keyEventNode__aopwiki_id, domain=None, range=Optional[str])

slots.keyEventNode__event_type = Slot(uri=AOP_CAM.event_type, name="keyEventNode__event_type", curie=AOP_CAM.curie('event_type'),
                   model_uri=AOP_CAM.keyEventNode__event_type, domain=None, range=Optional[Union[str, "EventTypeEnum"]])

slots.keyEventNode__level_of_biological_organization = Slot(uri=AOP_CAM.level_of_biological_organization, name="keyEventNode__level_of_biological_organization", curie=AOP_CAM.curie('level_of_biological_organization'),
                   model_uri=AOP_CAM.keyEventNode__level_of_biological_organization, domain=None, range=Optional[Union[str, "LevelOfBiologicalOrganizationEnum"]])

slots.keyEventNode__process = Slot(uri=AOP_CAM.process, name="keyEventNode__process", curie=AOP_CAM.curie('process'),
                   model_uri=AOP_CAM.keyEventNode__process, domain=None, range=Optional[Union[dict, ProcessAssociation]])

slots.keyEventNode__object = Slot(uri=AOP_CAM.object, name="keyEventNode__object", curie=AOP_CAM.curie('object'),
                   model_uri=AOP_CAM.keyEventNode__object, domain=None, range=Optional[Union[dict, ObjectAssociation]])

slots.keyEventNode__direction = Slot(uri=AOP_CAM.direction, name="keyEventNode__direction", curie=AOP_CAM.curie('direction'),
                   model_uri=AOP_CAM.keyEventNode__direction, domain=None, range=Optional[Union[dict, DirectionAssociation]])

slots.keyEventNode__occurs_in_cell_type = Slot(uri=AOP_CAM.occurs_in_cell_type, name="keyEventNode__occurs_in_cell_type", curie=AOP_CAM.curie('occurs_in_cell_type'),
                   model_uri=AOP_CAM.keyEventNode__occurs_in_cell_type, domain=None, range=Optional[Union[dict, CellTypeAssociation]])

slots.keyEventNode__occurs_in_anatomy = Slot(uri=AOP_CAM.occurs_in_anatomy, name="keyEventNode__occurs_in_anatomy", curie=AOP_CAM.curie('occurs_in_anatomy'),
                   model_uri=AOP_CAM.keyEventNode__occurs_in_anatomy, domain=None, range=Optional[Union[dict, GrossAnatomyAssociation]])

slots.keyEventNode__causal_associations = Slot(uri=AOP_CAM.causal_associations, name="keyEventNode__causal_associations", curie=AOP_CAM.curie('causal_associations'),
                   model_uri=AOP_CAM.keyEventNode__causal_associations, domain=None, range=Optional[Union[Union[dict, CausalAssociation], list[Union[dict, CausalAssociation]]]])

slots.keyEventNode__outcome_mappings = Slot(uri=AOP_CAM.outcome_mappings, name="keyEventNode__outcome_mappings", curie=AOP_CAM.curie('outcome_mappings'),
                   model_uri=AOP_CAM.keyEventNode__outcome_mappings, domain=None, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]],
                   pattern=re.compile(r'^(HP:\d{7}|MONDO:\d{7}|UPHENO:\d+)$'))

slots.keyEventNode__provenances = Slot(uri=AOP_CAM.provenances, name="keyEventNode__provenances", curie=AOP_CAM.curie('provenances'),
                   model_uri=AOP_CAM.keyEventNode__provenances, domain=None, range=Optional[Union[Union[dict, ProvenanceInfo], list[Union[dict, ProvenanceInfo]]]])

slots.association__type = Slot(uri=AOP_CAM.type, name="association__type", curie=AOP_CAM.curie('type'),
                   model_uri=AOP_CAM.association__type, domain=None, range=Optional[str])

slots.association__evidence = Slot(uri=AOP_CAM.evidence, name="association__evidence", curie=AOP_CAM.curie('evidence'),
                   model_uri=AOP_CAM.association__evidence, domain=None, range=Optional[Union[Union[dict, EvidenceItem], list[Union[dict, EvidenceItem]]]])

slots.association__provenances = Slot(uri=AOP_CAM.provenances, name="association__provenances", curie=AOP_CAM.curie('provenances'),
                   model_uri=AOP_CAM.association__provenances, domain=None, range=Optional[Union[Union[dict, ProvenanceInfo], list[Union[dict, ProvenanceInfo]]]])

slots.causalAssociation__predicate = Slot(uri=AOP_CAM.predicate, name="causalAssociation__predicate", curie=AOP_CAM.curie('predicate'),
                   model_uri=AOP_CAM.causalAssociation__predicate, domain=None, range=Union[str, "CausalPredicateEnum"])

slots.causalAssociation__downstream_event = Slot(uri=AOP_CAM.downstream_event, name="causalAssociation__downstream_event", curie=AOP_CAM.curie('downstream_event'),
                   model_uri=AOP_CAM.causalAssociation__downstream_event, domain=None, range=Union[str, KeyEventNodeId])

slots.causalAssociation__aopwiki_ker_id = Slot(uri=AOP_CAM.aopwiki_ker_id, name="causalAssociation__aopwiki_ker_id", curie=AOP_CAM.curie('aopwiki_ker_id'),
                   model_uri=AOP_CAM.causalAssociation__aopwiki_ker_id, domain=None, range=Optional[str])

slots.causalAssociation__evidence_level = Slot(uri=AOP_CAM.evidence_level, name="causalAssociation__evidence_level", curie=AOP_CAM.curie('evidence_level'),
                   model_uri=AOP_CAM.causalAssociation__evidence_level, domain=None, range=Optional[Union[str, "ConfidenceLevelEnum"]])

slots.causalAssociation__quantitative_understanding = Slot(uri=AOP_CAM.quantitative_understanding, name="causalAssociation__quantitative_understanding", curie=AOP_CAM.curie('quantitative_understanding'),
                   model_uri=AOP_CAM.causalAssociation__quantitative_understanding, domain=None, range=Optional[Union[str, "ConfidenceLevelEnum"]])

slots.evidenceItem__term = Slot(uri=AOP_CAM.term, name="evidenceItem__term", curie=AOP_CAM.curie('term'),
                   model_uri=AOP_CAM.evidenceItem__term, domain=None, range=Optional[Union[str, URIorCURIE]],
                   pattern=re.compile(r'^ECO:\d{7}$'))

slots.evidenceItem__reference = Slot(uri=AOP_CAM.reference, name="evidenceItem__reference", curie=AOP_CAM.curie('reference'),
                   model_uri=AOP_CAM.evidenceItem__reference, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.evidenceItem__supporting_objects = Slot(uri=AOP_CAM.supporting_objects, name="evidenceItem__supporting_objects", curie=AOP_CAM.curie('supporting_objects'),
                   model_uri=AOP_CAM.evidenceItem__supporting_objects, domain=None, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.evidenceItem__description = Slot(uri=AOP_CAM.description, name="evidenceItem__description", curie=AOP_CAM.curie('description'),
                   model_uri=AOP_CAM.evidenceItem__description, domain=None, range=Optional[str])

slots.evidenceItem__provenances = Slot(uri=AOP_CAM.provenances, name="evidenceItem__provenances", curie=AOP_CAM.curie('provenances'),
                   model_uri=AOP_CAM.evidenceItem__provenances, domain=None, range=Optional[Union[Union[dict, ProvenanceInfo], list[Union[dict, ProvenanceInfo]]]])

slots.provenanceInfo__contributor = Slot(uri=AOP_CAM.contributor, name="provenanceInfo__contributor", curie=AOP_CAM.curie('contributor'),
                   model_uri=AOP_CAM.provenanceInfo__contributor, domain=None, range=Optional[str])

slots.provenanceInfo__created = Slot(uri=AOP_CAM.created, name="provenanceInfo__created", curie=AOP_CAM.curie('created'),
                   model_uri=AOP_CAM.provenanceInfo__created, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.provenanceInfo__modified = Slot(uri=AOP_CAM.modified, name="provenanceInfo__modified", curie=AOP_CAM.curie('modified'),
                   model_uri=AOP_CAM.provenanceInfo__modified, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.provenanceInfo__source = Slot(uri=AOP_CAM.source, name="provenanceInfo__source", curie=AOP_CAM.curie('source'),
                   model_uri=AOP_CAM.provenanceInfo__source, domain=None, range=Optional[str])

slots.ProcessAssociation_term = Slot(uri=AOP_CAM.term, name="ProcessAssociation_term", curie=AOP_CAM.curie('term'),
                   model_uri=AOP_CAM.ProcessAssociation_term, domain=ProcessAssociation, range=Optional[Union[dict, "ProcessTermObject"]])

slots.ObjectAssociation_term = Slot(uri=AOP_CAM.term, name="ObjectAssociation_term", curie=AOP_CAM.curie('term'),
                   model_uri=AOP_CAM.ObjectAssociation_term, domain=ObjectAssociation, range=Optional[Union[dict, "ObjectTermObject"]])

slots.DirectionAssociation_term = Slot(uri=AOP_CAM.term, name="DirectionAssociation_term", curie=AOP_CAM.curie('term'),
                   model_uri=AOP_CAM.DirectionAssociation_term, domain=DirectionAssociation, range=Optional[Union[dict, "DirectionTermObject"]])

slots.CellTypeAssociation_term = Slot(uri=AOP_CAM.term, name="CellTypeAssociation_term", curie=AOP_CAM.curie('term'),
                   model_uri=AOP_CAM.CellTypeAssociation_term, domain=CellTypeAssociation, range=Optional[Union[dict, "CellTypeTermObject"]])

slots.GrossAnatomyAssociation_term = Slot(uri=AOP_CAM.term, name="GrossAnatomyAssociation_term", curie=AOP_CAM.curie('term'),
                   model_uri=AOP_CAM.GrossAnatomyAssociation_term, domain=GrossAnatomyAssociation, range=Optional[Union[dict, "AnatomyTermObject"]])

slots.DirectionTermObject_id = Slot(uri=AOP_CAM.id, name="DirectionTermObject_id", curie=AOP_CAM.curie('id'),
                   model_uri=AOP_CAM.DirectionTermObject_id, domain=DirectionTermObject, range=Union[str, DirectionTermObjectId],
                   pattern=re.compile(r'^PATO:\d{7}$'))

slots.CellTypeTermObject_id = Slot(uri=AOP_CAM.id, name="CellTypeTermObject_id", curie=AOP_CAM.curie('id'),
                   model_uri=AOP_CAM.CellTypeTermObject_id, domain=CellTypeTermObject, range=Union[str, CellTypeTermObjectId],
                   pattern=re.compile(r'^CL:\d{7}$'))

slots.AnatomyTermObject_id = Slot(uri=AOP_CAM.id, name="AnatomyTermObject_id", curie=AOP_CAM.curie('id'),
                   model_uri=AOP_CAM.AnatomyTermObject_id, domain=AnatomyTermObject, range=Union[str, AnatomyTermObjectId],
                   pattern=re.compile(r'^UBERON:\d{7}$'))

slots.TaxonTermObject_id = Slot(uri=AOP_CAM.id, name="TaxonTermObject_id", curie=AOP_CAM.curie('id'),
                   model_uri=AOP_CAM.TaxonTermObject_id, domain=TaxonTermObject, range=Union[str, TaxonTermObjectId],
                   pattern=re.compile(r'^NCBITaxon:\d+$'))
