4
Bayesian Networks – Tools, Modelling, and Inference 
PART A – What is a Bayesian Network?

A Bayesian Network (BN) is a probabilistic graphical model that represents a set
of random variables and their conditional dependencies via a Directed Acyclic
Graph (DAG).
 
Key components:
  1. Nodes   : random variables (e.g., Disease, Symptom, Test)
  2. Edges   : conditional dependencies  A → B means "A influences B."
  3. CPTs    : Conditional Probability Tables for each node
                P(Node | Parents)
 
Core formula – Bayes' Theorem:
    P(A | B) = P(B | A) × P(A) / P(B)
 
BNs allow us to:
  • Encode domain knowledge + uncertainty
  • Perform inference: P(hypothesis | evidence)
  • Update beliefs as new evidence arrives
 
PART B – Popular BN Tools
Tool          | Language | Best For

pgmpy         | Python   | Building & inferring BNs (used here)
pomegranate   | Python   | Fast BNs, HMMs, GMMs
bnlearn       | R        | Structure learning from data
Netica        | GUI      | Commercial BN tool with GUI
GeNIe (SMILE) | C++/GUI  | Academic BN editor
Hugin         | Java/GUI | Enterprise decision support
PyMC          | Python   | Bayesian modelling + MCMC
Stan          | C++      | Probabilistic programming
 
PART C – Implementation: Medical Diagnosis BN
Domain: "Does this patient have the Flu?"
 
Network structure:
    Season ──┐
             ▼
    Flu ────▶ Fever ──▶ (no child, leaf)
    Flu ────▶ Cough ──▶ (no child, leaf)
    Flu ────▶ Fatigue ─▶ (no child, leaf)
 
Variables:
  • Season  : Winter / Other
  • Flu     : Yes / No  (depends on Season)
  • Fever   : Yes / No  (depends on Flu)
  • Cough   : Yes / No  (depends on Flu)
  • Fatigue : Yes / No  (depends on Flu)
 
We then answer clinical queries like:
  "If a patient has Fever AND Cough, what is P(Flu=Yes)?"

3
Describing Knowledge Graphs
A Knowledge Graph (KG) is a programmatic way of organizing information as a network of real-world objects (called Nodes or Entities) linked together by meaningful properties (called Edges or Relationships).

Unlike traditional databases that store data in isolated row-and-column tables, a Knowledge Graph turns abstract facts into interconnected data points. The fundamental layout of a knowledge graph relies on a three-part structural unit called a Semantic Triple:

Subject -> Predicate -> Object

Subject (Node 1): Tuscany
Predicate (Edge): PRODUCES_DRINK
Object (Node 2): Chianti Classico

By linking millions of these triples together, systems like Google Search or Alexa can easily deduce contextual, real-world connections.

Exploring Tools to Build Knowledge Graphs
Depending on the scale and language of your engineering environment, multiple specialized tools exist to construct, query, and store graphs:

1. Python Libraries (For Development & Analysis)
NetworkX: A native Python package used for building, manipulating, and studying the structural properties of complex networks. It is ideal for prototyping graph logic (similar to the manual code built above).

RDFLib: A Python library specifically built for working with semantic web standard formats like RDF, OWL, and JSON-LD.

2. Graph Databases (For Production & Storage)
Neo4j: The world's most popular native graph database engine. It uses a highly readable, human-centric query language called Cypher (which acts like SQL but optimized for network structures).

Amazon Neptune / Graph Databases via Cloud: Fully managed graph database engines optimized for storing billions of relationships and executing fast queries across complex networks.

3. Ontological Schema Modeler
Protégé: An open-source desktop application designed by Stanford University. It gives developers a visual interface to define the vocabulary, categories, and structural rules (the Ontology) of a system before translating it into raw code database elements.
