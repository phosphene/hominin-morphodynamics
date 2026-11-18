# Naming Principles and Architectural Design

*Synthesized from "Elements of Clojure" by Zachary Tellman, integrated with Phosphene Logic/IO separation and morphological inference architecture.*

Software engineering is primarily the act of naming and the discipline of managing indirection. A name establishes the primary boundary of **indirection**—the formal separation between *what* an entity is and *how* it is implemented.

In macroevolutionary inference, morphological analysis, and numerical simulation, clear naming principles are essential to prevent leaky implementation details from corrupting biological senses.

---

## 1. The Tripartite Semantic Framework (Frege)

Every name operates across three distinct semantic dimensions:

1. **Sign:** The textual token or symbol representation (e.g., `specimen-id`, `morpho-disparity`, `solve-master-equation`).
2. **Referent:** The concrete runtime value, data structure, or physical implementation (e.g., a NumPy float64 array, a Polars DataFrame, a SciPy sparse transition matrix, a PyRate horizon dictionary).
3. **Sense:** The fundamental, invariant property or conceptual meaning ascribed to the name (e.g., the biological property of being *taxonomically identifiable*, of being an *anagenetic lineage step*, of being an *eigen-solution*).

### The Invariance Rule
A name’s **sense** is timeless and invariant. While the **referent** (the underlying implementation or numerical routine) changes across revisions and refactorings, the **sense** must remain constant. When implementation mechanics leak into the sense (e.g., naming a variable `specimen-dict` or `likelihood-float64`), the abstraction becomes complected, brittle, and subject to breaking changes under numerical optimization.

---

## 2. Two Pillars of a Good Name

### Narrowness
A narrow name exposes its exact biological or mathematical sense while cleanly excluding states and entities it cannot legitimately represent.

* **Under-specified (Too Broad):** Generic identifiers like `data`, `matrix`, `res`, `calc`, `x`, `model`, or `temp` obscure their sense, invite semantic drift, and erode mathematical contracts.
* **Over-specified (Leaky):** Identifiers like `numpy-array-points`, `pyrate-parsed-json`, or `sparse-scipy-csr` hardcode transient implementation structures into the symbol, forcing cascading renames when data containers or solver libraries change.
* **Balanced & Narrow:** Identifiers like `paleodeme-coords`, `profile-likelihood`, `transition-matrix`, or `branch-lengths` specify the exact operational sense without binding the call site to transient internal representations.

### Consistency
A name achieves consistency when it reinforces established conventions across the surrounding module, the biological domain, and the software ecosystem.

* **Expectation Alignment:** Using a well-known sign (e.g., `phylogeny` for a raw distance matrix, or `carrying-capacity` for an unconstrained diversification rate parameter) forces the reader to doubt their intuitive mental model.
* **Contextual Isolation:** Identical signs (e.g., `rate`, `dr`, `dispersion`) may legitimately hold different senses across independent domains (e.g., insular speciation rates vs. taphonomic loss rates), provided those senses are strictly partitioned by namespaces or module boundaries.

---

## 3. Data Naming Defaults (Clojure & Functional Scientific Code)

In functional and dynamic environments without verbose explicit type declarations, names carry the weight of meaning:

| Category | Recommended Sign | Context |
| :--- | :--- | :--- |
| **Arbitrary Value** | `x` | Used only when universal operations (`=`, `hash`, `str`) are performed. |
| **Sequences / Vectors** | `xs`, `specimens`, `clades` | Adding an `s` suffix to denote an immutable sequence or collection. |
| **Maps / Records** | `m`, `horizon` | For arbitrary maps or single record maps. |
| **Pure Functions / Operators** | `f`, `kernel` | For higher-order functions and mathematical kernels. |
| **Named Tuples / Pairs** | `a+b` (e.g., `fossil+matrix`, `island+clade`) | Vector or tuple pairing of distinct domains. |
| **Mapped Relations** | `key->value` (e.g., `taxon->demes`, `horizon->profile`) | Clear relational transformations or lookup maps. |

---

## 4. Naming Functions: The Logic / IO Boundary

Functions are categorized by how they interact with data scope and boundary crossing:

### Pure Functional Transformations (Internal Scope)
Functions that operate strictly within an internal data scope to accrete, project, or reshape immutable data must **avoid action verbs**.

* **Standard:** `profile-likelihood`, `transition-matrix`, `eigen-spectrum`, `tip-dr`, `->base64`, `normalized-coordinates`.
* **Antipattern:** `calculate-profile-likelihood`, `compute-transition-matrix`, `get-eigen-spectrum`.
* **Rationale:** Verbs imply external action, temporal sequence, or physical state change. A pure mathematical transformation is fully denoted by the value or result it yields.

### Operational Procedures (Boundary Crossing / Side Effects)
Functions that cross scope boundaries (disk I/O, database interaction, network calls, filesystem mutations, external CLI invocations) **must use explicit operational verbs**.

* **Inbound (Pull):** Verbs describe the data type acquired across the boundary (e.g., `fetch-specimens`, `read-fossil-horizons`, `pull-tree-nexus`).
* **Outbound (Push):** Verbs describe the effect produced in the external environment (e.g., `export-surface-plot!`, `write-demes!`, `save-checkpoint!`).

---

## 5. Organization of Synthetic Semantics (Scientific Context)

In scientific research, synthetic terminology is mandatory to avoid the ambiguity, metaphorical baggage, and drift of natural language. Tellman’s principle states that absolute consistency requires maintaining a 1:1 relationship between signs and senses.

### Namespacing as Contextual Isolation
Namespaces organize functions and data structures around a singular, unified purpose. The namespace coordinate provides the necessary narrowness, permitting clean, concise identifiers within:

* **Domain Partitioning:** In a platform analyzing both Galápagos avifauna and continental hominins, both involve diversification dynamics. Partitioning into `canonical.galapagos` and `inference.hominin` allows short, narrow signs (`carrying-capacity`, `speciation-rate`) without name collision or prefix bloat.
* **Type Stripping via Namespace:** Within `hominin_morphodynamics.inference.joint_likelihood`, a function is cleanly named `surface`, not `compute-hominin-joint-likelihood-surface`. The namespace carries the structural coordinate.

### Managing the "Cliff"
Synthetic names represent binary propositions: the reader either knows the formalism or does not.

* Confine dense synthetic vocabularies (e.g., `seme`, `pheme`, `delome`, `paleodeme`, `eigen-morphospace`) to the **operational core** and formal contracts of the module.
* Expose natural, analogical names at public ingress boundaries, CLI scripts, and high-level interfaces, allowing researchers to orient themselves before crossing the synthetic cliff.

---

## 6. Architectural Indirection: Model, Interface, Environment

Every computational module decomposes into a tripartite architecture:

1. **Model:** The collection of data structures and pure functions that represent specific facets of the observed environment (e.g., Etienne continuous-time master equations, Markov transition rate matrices).
2. **Interface:** The formal contracts, protocols, and boundaries through which the model and environment interact (e.g., API boundaries, LikelihoodRatioTest results, PyRate schema adapters).
3. **Environment:** The unmanaged external territory (the fossil record, deep-time taphonomy, the operating system, CSV/TSV disk files, human researchers).

### Deductive vs. Inductive Models
* **Deductive Models:** Target mathematical closure and formal invariants (e.g., analytical diversification likelihoods). They are internally self-consistent but break down if external environmental invariants violate their axioms.
* **Inductive Models:** Target satisficing and heuristic adequacy through analogy. Research software systematically migrates from inductive exploration toward deductive rigor.

**Axiom of Assumption:** Every omitted factor is an active assumption. If a diversification model omits taphonomic preservation bias, it assumes the preservation probability is spatially and temporally uniform ($p = 1.0$).

---

## 7. Composition: The Unit of Computation (The Process)

A standalone computational process decomposes cleanly into three decoupled phases:

```
[ PULL: Ingestion / Parse ]  -->  [ TRANSFORM: Pure Core Logic ]  -->  [ PUSH: Egress / Storage ]
   (Operational / Verb)               (Functional / Non-Verb)             (Operational / Verb!)
```

1. **Pull (Operational):** Acquires raw specimen logs or phylogenetic trees from the environment, verifies schema shape, asserts boundary constraints, and handles missing coordinate errors.
2. **Transform (Functional Core):** The pure algorithmic core. Operates on immutable data structures; zero disk access, zero network calls, zero side effects. Fully testable via deterministic unit tests, property checks, and analytical edge cases.
3. **Push (Operational):** Transmits or persists the resulting values to the target environment (e.g., writing Parquet summary tables, generating matplotlib likelihood surfaces, emitting test reports).

---

## 8. The "Skimming" Principle

Rigorous naming and clean three-phase composition enable **lossless skimming**:

1. **Top Layer (What):** High-level function pipelines and orchestrators (`let` blocks, pipeline steps) composed exclusively of narrow, consistent operational names that describe *what* transformation is executing.
2. **Bottom Layer (How):** Internal helper functions within the pure transform module that detail *how* the numerical data is reshaped.

A researcher inspecting a pipeline must be able to verify its entire macroevolutionary intent and invariant structure strictly by reading the top-level orchestration layer, without descending into solver internals.
