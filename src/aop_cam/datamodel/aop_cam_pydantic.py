from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.12.0"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'aop_cam',
     'default_range': 'string',
     'description': 'Adverse Outcome Pathways represented as causal activity '
                    'models, following the GO-CAM paradigm: an AOP is a model (a '
                    'named causal graph), each Key Event is a node defined by '
                    'associations to ontology terms in context, each Key Event '
                    'Relationship is a typed causal association drawn from the '
                    'Relation Ontology, and evidence attaches to individual '
                    'assertions rather than to whole records. The schema mirrors '
                    'the GO-CAM pattern (Association hierarchy, per-assertion '
                    'evidence, model lifecycle) without importing its gene-product '
                    'machinery: a Key Event is not a molecular Activity, and the '
                    'AOP extensions GO-CAM lacks - direction of change as node '
                    'state, levels of biological organization up to population, '
                    'and compositional outcome grounding with optional '
                    'precomposed-term mappings - are first-class here. Instances '
                    'can be loaded from AOP-Wiki exports; aopwiki_id slots keep '
                    'the crosswalk.',
     'id': 'https://w3id.org/EHS-Data-Standards/aop-cam',
     'imports': ['linkml:types'],
     'license': 'BSD-3',
     'name': 'aop_cam',
     'prefixes': {'AOPWIKI': {'prefix_prefix': 'AOPWIKI',
                              'prefix_reference': 'https://aopwiki.org/'},
                  'AOPWIKIBA': {'prefix_prefix': 'AOPWIKIBA',
                                'prefix_reference': 'https://aopwiki.org/vocabularies/biological-actions/'},
                  'CHEBI': {'prefix_prefix': 'CHEBI',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/CHEBI_'},
                  'CL': {'prefix_prefix': 'CL',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/CL_'},
                  'DOI': {'prefix_prefix': 'DOI',
                          'prefix_reference': 'http://doi.org/'},
                  'ECO': {'prefix_prefix': 'ECO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/ECO_'},
                  'FMA': {'prefix_prefix': 'FMA',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/FMA_'},
                  'GO': {'prefix_prefix': 'GO',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/GO_'},
                  'HP': {'prefix_prefix': 'HP',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/HP_'},
                  'IDO': {'prefix_prefix': 'IDO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/IDO_'},
                  'MESH': {'prefix_prefix': 'MESH',
                           'prefix_reference': 'http://id.nlm.nih.gov/mesh/'},
                  'MI': {'prefix_prefix': 'MI',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/MI_'},
                  'MONDO': {'prefix_prefix': 'MONDO',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/MONDO_'},
                  'MP': {'prefix_prefix': 'MP',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/MP_'},
                  'NBO': {'prefix_prefix': 'NBO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/NBO_'},
                  'NCBITaxon': {'prefix_prefix': 'NCBITaxon',
                                'prefix_reference': 'http://purl.obolibrary.org/obo/NCBITaxon_'},
                  'PATO': {'prefix_prefix': 'PATO',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/PATO_'},
                  'PCO': {'prefix_prefix': 'PCO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/PCO_'},
                  'PMID': {'prefix_prefix': 'PMID',
                           'prefix_reference': 'http://identifiers.org/pubmed/'},
                  'PR': {'prefix_prefix': 'PR',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/PR_'},
                  'RBO': {'prefix_prefix': 'RBO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/RBO_'},
                  'RO': {'prefix_prefix': 'RO',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/RO_'},
                  'UBERON': {'prefix_prefix': 'UBERON',
                             'prefix_reference': 'http://purl.obolibrary.org/obo/UBERON_'},
                  'UPHENO': {'prefix_prefix': 'UPHENO',
                             'prefix_reference': 'http://purl.obolibrary.org/obo/UPHENO_'},
                  'VT': {'prefix_prefix': 'VT',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/VT_'},
                  'aop_cam': {'prefix_prefix': 'aop_cam',
                              'prefix_reference': 'https://w3id.org/EHS-Data-Standards/aop-cam/'},
                  'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'}},
     'source_file': 'src/aop_cam/schema/aop_cam.yaml',
     'title': 'AOP Causal Activity Models'} )

class ModelStateEnum(str, Enum):
    """
    Where the model is in its development life cycle (GO-CAM semantics).
    """
    development = "development"
    """
    Still being worked on; not guaranteed accurate or complete.
    """
    production = "production"
    """
    Declared ready for public consumption.
    """
    review = "review"
    """
    Marked for curator review.
    """
    archived = "archived"
    """
    Retained for reference; no longer maintained.
    """


class EventTypeEnum(str, Enum):
    """
    The curator-asserted role of a key event node in the pathway.
    """
    molecular_initiating_event = "molecular_initiating_event"
    """
    The initial perturbation; no incoming causal associations.
    """
    key_event = "key_event"
    """
    An intermediate measurable change.
    """
    adverse_outcome = "adverse_outcome"
    """
    The apical endpoint; no outgoing causal associations.
    """


class LevelOfBiologicalOrganizationEnum(str, Enum):
    """
    Levels of biological organization, following AOP-Wiki usage.
    """
    molecular = "molecular"
    cellular = "cellular"
    tissue = "tissue"
    organ = "organ"
    individual = "individual"
    population = "population"


class CausalPredicateEnum(str, Enum):
    """
    The causal relation between two key events, drawn from the "causally upstream or within" branch of the Relation Ontology. Permissible values and meanings follow the GO-CAM schema's CausalPredicateEnum.
    """
    causally_upstream_of_positive_effect = "causally upstream of, positive effect"
    causally_upstream_of_negative_effect = "causally upstream of, negative effect"
    causally_upstream_of = "causally upstream of"
    immediately_causally_upstream_of = "immediately causally upstream of"
    causally_upstream_of_or_within = "causally upstream of or within"
    regulates = "regulates"
    negatively_regulates = "negatively regulates"
    positively_regulates = "positively regulates"


class ConfidenceLevelEnum(str, Enum):
    """
    Curated confidence levels, following AOP-Wiki usage.
    """
    high = "high"
    moderate = "moderate"
    low = "low"
    not_specified = "not_specified"



class ModelCollection(ConfiguredBaseModel):
    """
    Root container for a set of AOP causal activity models, e.g. one release of models converted from an AOP-Wiki snapshot, or a curated network slice.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'tree_root': True})

    models: Optional[list[AopModel]] = Field(default=None, description="""The models in this collection.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ModelCollection']} })
    snapshot_date: Optional[date] = Field(default=None, description="""Date of the AOP-Wiki snapshot these models were derived from, when applicable. Nightly dumps are overwritten daily, so cite a quarterly dump date wherever possible.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ModelCollection']} })


class AopModel(ConfiguredBaseModel):
    """
    One Adverse Outcome Pathway as a causal activity model: a named graph of Key Event nodes connected by typed causal associations. Initial nodes (no incoming causal association) are molecular initiating events; terminal nodes (no outgoing causal association) are adverse outcomes. The event_type on each node states the curator's intent; the graph position is checkable against it.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'rules': [{'postconditions': {'slot_conditions': {'key_events': {'name': 'key_events',
                                                                          'required': True}}},
                    'preconditions': {'slot_conditions': {'status': {'equals_string': 'production',
                                                                     'name': 'status'}}},
                    'title': 'Production models must have key events'}]})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'TermObject']} })
    title: str = Field(default=..., description="""Human-readable title of the model.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode'], 'slot_uri': 'dcterms:title'} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'EvidenceItem']} })
    aopwiki_id: Optional[str] = Field(default=None, description="""AOP-Wiki identifier for this AOP (e.g. \"Aop:425\").""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode']} })
    status: Optional[ModelStateEnum] = Field(default=None, description="""Lifecycle status of the model.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel']} })
    oecd_status: Optional[str] = Field(default=None, description="""OECD endorsement status, carried over from AOP-Wiki.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel']} })
    taxa: Optional[list[TaxonTermObject]] = Field(default=None, description="""Taxa this model is asserted to apply to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel']} })
    key_events: Optional[list[KeyEventNode]] = Field(default=None, description="""All Key Event nodes in this model.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel']} })
    stressors: Optional[list[StressorTermObject]] = Field(default=None, description="""Chemical or physical stressors known to trigger this pathway, as ontology term references where possible.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel']} })
    comments: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })


class KeyEventNode(ConfiguredBaseModel):
    """
    One Key Event as a node in a causal activity model. The node itself is only an identifier and a label; its meaning comes from its associations - one or more entity+quality components (the biological process affected and/or the object acted on, with the direction of change) plus the cellular and anatomical context - each assignment carrying its own evidence. An adverse outcome is a terminal KeyEventNode: its composition defines it, and outcome_mappings optionally decorate it with precomposed phenotype or disease terms where any exist.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'TermObject']} })
    title: str = Field(default=..., description="""Human-readable name of the key event.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode']} })
    aopwiki_id: Optional[str] = Field(default=None, description="""AOP-Wiki identifier for this key event (e.g. \"Event:1656\").""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode']} })
    event_type: Optional[EventTypeEnum] = Field(default=None, description="""The curator-asserted role of this node in the pathway. Must be consistent with graph position: a molecular_initiating_event has no incoming causal associations, an adverse_outcome has no outgoing ones.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KeyEventNode']} })
    level_of_biological_organization: Optional[LevelOfBiologicalOrganizationEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['KeyEventNode']} })
    components: Optional[list[KeyEventComponent]] = Field(default=None, description="""The entity+quality decompositions of this key event. Mirrors AOP-Wiki's biological-event triples (action, process, object): most key events have exactly one; some carry several complementary decompositions of the same change, so the pairing of direction with process and object is preserved per component.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KeyEventNode']} })
    occurs_in_cell_type: Optional[CellTypeAssociation] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['KeyEventNode']} })
    occurs_in_anatomy: Optional[GrossAnatomyAssociation] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['KeyEventNode']} })
    causal_associations: Optional[list[CausalAssociation]] = Field(default=None, description="""The causal associations that flow out of this node. A node with none is terminal in the model; a node no other node points at is initial.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KeyEventNode']} })
    outcome_mappings: Optional[list[str]] = Field(default=None, description="""For adverse outcome nodes: precomposed terms equivalent or close to this outcome's compositional definition, where any exist (HPO phenotype, MONDO disease, or uPheno class). A decoration for discovery, not the definition; candidates can be generated by matching the node's entity+quality composition against uPheno's pattern space.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KeyEventNode']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })

    @field_validator('outcome_mappings')
    def pattern_outcome_mappings(cls, v):
        pattern=re.compile(r"^(HP:\d{7}|MONDO:\d{7}|UPHENO:\d+)$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid outcome_mappings format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid outcome_mappings format: {v}"
            raise ValueError(err_msg)
        return v


class KeyEventComponent(ConfiguredBaseModel):
    """
    One entity+quality decomposition of a key event: the biological process perturbed and/or the object acted on (the entity), paired with the direction of change (the quality). Mirrors one AOP-Wiki biological-event triple (action + process + object). Each leg is an Association carrying its own evidence receipt; the component holds them together so a key event with several decompositions keeps each direction attached to the process and object it belongs with.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam'})

    process: Optional[ProcessAssociation] = Field(default=None, description="""The biological process this component perturbs.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KeyEventComponent']} })
    object: Optional[ObjectAssociation] = Field(default=None, description="""The biological object (molecule, cell, structure) acted on.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KeyEventComponent']} })
    direction: Optional[DirectionAssociation] = Field(default=None, description="""The direction of change, as a PATO quality.""", json_schema_extra = { "linkml_meta": {'domain_of': ['KeyEventComponent']} })


class Association(ConfiguredBaseModel):
    """
    An individual assertion in a model, carrying its own evidence and provenance. Every term assignment and every causal edge is an Association subtype, so support attaches to the claim itself rather than to the record that contains it.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam'})

    type: Literal["Association"] = Field(default="Association", description="""Auto-populated association type discriminator.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['Association']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })


class TermAssociation(Association):
    """
    An association between a node and an ontology term. Abstract; use the typed subclasses so each dimension constrains its vocabulary.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam'})

    term: Optional[TermObject] = Field(default=None, description="""The ontology term this association assigns.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermAssociation', 'EvidenceItem']} })
    type: Literal["TermAssociation"] = Field(default="TermAssociation", description="""Auto-populated association type discriminator.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['Association']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })


class ProcessAssociation(TermAssociation):
    """
    Associates a key event with the biological process it perturbs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'slot_usage': {'term': {'name': 'term', 'range': 'ProcessTermObject'}}})

    term: Optional[ProcessTermObject] = Field(default=None, description="""The ontology term this association assigns.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermAssociation', 'EvidenceItem']} })
    type: Literal["ProcessAssociation"] = Field(default="ProcessAssociation", description="""Auto-populated association type discriminator.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['Association']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })


class ObjectAssociation(TermAssociation):
    """
    Associates a key event with the biological object acted on (a protein, chemical, cell component, or other entity).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'slot_usage': {'term': {'name': 'term', 'range': 'ObjectTermObject'}}})

    term: Optional[ObjectTermObject] = Field(default=None, description="""The ontology term this association assigns.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermAssociation', 'EvidenceItem']} })
    type: Literal["ObjectAssociation"] = Field(default="ObjectAssociation", description="""Auto-populated association type discriminator.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['Association']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })


class DirectionAssociation(TermAssociation):
    """
    Associates a key event with the direction of change, as a PATO quality (e.g. increased amount, decreased functionality). Together with the process or object this forms the entity+quality decomposition of the event.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'slot_usage': {'term': {'name': 'term', 'range': 'DirectionTermObject'}}})

    term: Optional[DirectionTermObject] = Field(default=None, description="""The ontology term this association assigns.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermAssociation', 'EvidenceItem']} })
    type: Literal["DirectionAssociation"] = Field(default="DirectionAssociation", description="""Auto-populated association type discriminator.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['Association']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })


class CellTypeAssociation(TermAssociation):
    """
    The cell type in which the key event occurs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'slot_usage': {'term': {'name': 'term', 'range': 'CellTypeTermObject'}}})

    term: Optional[CellTypeTermObject] = Field(default=None, description="""The ontology term this association assigns.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermAssociation', 'EvidenceItem']} })
    type: Literal["CellTypeAssociation"] = Field(default="CellTypeAssociation", description="""Auto-populated association type discriminator.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['Association']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })


class GrossAnatomyAssociation(TermAssociation):
    """
    The anatomical location in which the key event occurs.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'slot_usage': {'term': {'name': 'term', 'range': 'AnatomyTermObject'}}})

    term: Optional[AnatomyTermObject] = Field(default=None, description="""The ontology term this association assigns.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermAssociation', 'EvidenceItem']} })
    type: Literal["GrossAnatomyAssociation"] = Field(default="GrossAnatomyAssociation", description="""Auto-populated association type discriminator.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['Association']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })


class CausalAssociation(Association):
    """
    A typed causal edge between two key event nodes: the AOP framework's Key Event Relationship, with the relation drawn from the causal branch of the Relation Ontology. AOP-Wiki adjacency maps onto the predicate: adjacent KERs are immediately causally upstream of; non-adjacent KERs are causally upstream of; use the positive/negative effect or regulates forms where the direction of influence is curated.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam'})

    predicate: CausalPredicateEnum = Field(default=..., description="""The RO causal relation for this edge.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CausalAssociation']} })
    downstream_event: str = Field(default=..., description="""The key event node this edge points to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CausalAssociation']} })
    aopwiki_ker_id: Optional[str] = Field(default=None, description="""AOP-Wiki identifier for this relationship (e.g. \"Relationship:2555\").""", json_schema_extra = { "linkml_meta": {'domain_of': ['CausalAssociation']} })
    evidence_level: Optional[ConfidenceLevelEnum] = Field(default=None, description="""Weight of evidence for this relationship, as curated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CausalAssociation']} })
    quantitative_understanding: Optional[ConfidenceLevelEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['CausalAssociation']} })
    type: Literal["CausalAssociation"] = Field(default="CausalAssociation", description="""Auto-populated association type discriminator.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['Association']} })
    evidence: Optional[list[EvidenceItem]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Association']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })


class EvidenceItem(ConfiguredBaseModel):
    """
    One piece of evidence supporting an assertion: an ECO evidence type, a publication, and optionally the supporting records themselves - for example the identifier of a SOMA assay whose measurements inform the assertion. This is the joint between the knowledge layer (this schema) and the experimental evidence layer (SOMA): an assay's informs_on_key_event link materializes here as evidence on the node's association.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam'})

    term: Optional[str] = Field(default=None, description="""The ECO term for the type of evidence.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermAssociation', 'EvidenceItem']} })
    reference: Optional[str] = Field(default=None, description="""The publication the evidence comes from (PMID, DOI, or AOPWIKI page).""", json_schema_extra = { "linkml_meta": {'domain_of': ['EvidenceItem']} })
    supporting_objects: Optional[list[str]] = Field(default=None, description="""Identifiers of supporting records, such as SOMA assay instances or database entities.""", json_schema_extra = { "linkml_meta": {'domain_of': ['EvidenceItem']} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'EvidenceItem']} })
    provenances: Optional[list[ProvenanceInfo]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'Association', 'EvidenceItem']} })

    @field_validator('term')
    def pattern_term(cls, v):
        pattern=re.compile(r"^ECO:\d{7}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid term format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid term format: {v}"
            raise ValueError(err_msg)
        return v


class ProvenanceInfo(ConfiguredBaseModel):
    """
    Who made or changed an assertion, and when.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam'})

    contributor: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceInfo']} })
    created: Optional[datetime ] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceInfo']} })
    modified: Optional[datetime ] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceInfo']} })
    source: Optional[str] = Field(default=None, description="""Where this content came from, e.g. \"AOPWiki\" for converted content or a curation project name for new assertions.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceInfo']} })


class TermObject(ConfiguredBaseModel):
    """
    A pointer to an ontology term: an identifier plus its label. Typed subclasses constrain which vocabulary each slot draws from.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam'})

    id: str = Field(default=..., description="""A unique identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'TermObject']} })
    label: Optional[str] = Field(default=None, description="""The human-readable label of the term, as given by its ontology.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermObject']} })


class ProcessTermObject(TermObject):
    """
    A biological process term. GO preferred; the other sources in AOP-Wiki's biological-process vocabulary (MESH, HP, MP, VT, NBO and kin) are accepted for conversion so the upstream assertion is kept verbatim, with re-grounding to GO left to curation.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'id_prefixes': ['GO',
                         'MESH',
                         'HP',
                         'MP',
                         'VT',
                         'NBO',
                         'MI',
                         'PCO',
                         'RBO',
                         'IDO']})

    id: str = Field(default=..., description="""A unique identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'TermObject']} })
    label: Optional[str] = Field(default=None, description="""The human-readable label of the term, as given by its ontology.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermObject']} })


class ObjectTermObject(TermObject):
    """
    A biological object term (protein, chemical, cell, anatomical structure, or other entity). AOP-Wiki's biological-object vocabulary also draws on CL, UBERON and FMA; those assertions are kept verbatim.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'id_prefixes': ['PR', 'CHEBI', 'GO', 'MESH', 'CL', 'UBERON', 'FMA']})

    id: str = Field(default=..., description="""A unique identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'TermObject']} })
    label: Optional[str] = Field(default=None, description="""The human-readable label of the term, as given by its ontology.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermObject']} })


class DirectionTermObject(TermObject):
    """
    A PATO quality term for the direction of change.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'id_prefixes': ['PATO'],
         'slot_usage': {'id': {'name': 'id', 'pattern': '^PATO:\\d{7}$'}}})

    id: str = Field(default=..., description="""A unique identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'TermObject']} })
    label: Optional[str] = Field(default=None, description="""The human-readable label of the term, as given by its ontology.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermObject']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^PATO:\d{7}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class CellTypeTermObject(TermObject):
    """
    A Cell Ontology term.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'id_prefixes': ['CL'],
         'slot_usage': {'id': {'name': 'id', 'pattern': '^CL:\\d{7}$'}}})

    id: str = Field(default=..., description="""A unique identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'TermObject']} })
    label: Optional[str] = Field(default=None, description="""The human-readable label of the term, as given by its ontology.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermObject']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^CL:\d{7}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class AnatomyTermObject(TermObject):
    """
    An UBERON anatomy term.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'id_prefixes': ['UBERON'],
         'slot_usage': {'id': {'name': 'id', 'pattern': '^UBERON:\\d{7}$'}}})

    id: str = Field(default=..., description="""A unique identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'TermObject']} })
    label: Optional[str] = Field(default=None, description="""The human-readable label of the term, as given by its ontology.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermObject']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^UBERON:\d{7}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class TaxonTermObject(TermObject):
    """
    An NCBI Taxonomy term.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'id_prefixes': ['NCBITaxon'],
         'slot_usage': {'id': {'name': 'id', 'pattern': '^NCBITaxon:\\d+$'}}})

    id: str = Field(default=..., description="""A unique identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'TermObject']} })
    label: Optional[str] = Field(default=None, description="""The human-readable label of the term, as given by its ontology.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermObject']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^NCBITaxon:\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class StressorTermObject(TermObject):
    """
    A stressor as an ontology term reference where one exists (CHEBI chemical, or an environmental material); free-text stressor names from AOP-Wiki that cannot be grounded keep their label with an AOPWIKI-prefixed id.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/EHS-Data-Standards/aop-cam',
         'id_prefixes': ['CHEBI', 'MESH']})

    id: str = Field(default=..., description="""A unique identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['AopModel', 'KeyEventNode', 'TermObject']} })
    label: Optional[str] = Field(default=None, description="""The human-readable label of the term, as given by its ontology.""", json_schema_extra = { "linkml_meta": {'domain_of': ['TermObject']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
ModelCollection.model_rebuild()
AopModel.model_rebuild()
KeyEventNode.model_rebuild()
KeyEventComponent.model_rebuild()
Association.model_rebuild()
TermAssociation.model_rebuild()
ProcessAssociation.model_rebuild()
ObjectAssociation.model_rebuild()
DirectionAssociation.model_rebuild()
CellTypeAssociation.model_rebuild()
GrossAnatomyAssociation.model_rebuild()
CausalAssociation.model_rebuild()
EvidenceItem.model_rebuild()
ProvenanceInfo.model_rebuild()
TermObject.model_rebuild()
ProcessTermObject.model_rebuild()
ObjectTermObject.model_rebuild()
DirectionTermObject.model_rebuild()
CellTypeTermObject.model_rebuild()
AnatomyTermObject.model_rebuild()
TaxonTermObject.model_rebuild()
StressorTermObject.model_rebuild()
