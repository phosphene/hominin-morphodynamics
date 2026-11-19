# Explanation, Descriptive Capacity, and Epistemic Circumspection in Morphodynamics

**Coordinate:** `docs/EXPLANATION_DESCRIPTIVE_CAPACITY_AND_CIRCUMSPECTION.md`  
**Namespace:** `morphodynamics.epistemics`  
**Authors:** Ed Phil (@edphos), Marsyas (@Marsyas6), Flow (@feelingflowingbot)  
**Status:** Foundational Methodological & Epistemic Specification  
**Date:** 2026-11-18  
**Repo:** `phosphene/hominin-morphodynamics`  

---

## 1. Executive Summary & The Epistemic Problem

A persistent obstacle in evolutionary biology is the dogmatic reduction of scientific "explanation" to a single mid-century template: either Hempel's **Deductive-Nomological (Covering Law)** model or narrow **Causal-Mechanical** reductionism. Under these rigid views, a study is only considered "explanatory" if it claims to have identified a universal law or a direct microscopic causal engine.

This dogmatism creates a false dilemma:
1. Either researchers invent an ungrounded causal narrative (e.g., reifying a descriptive statistical parameter $G_l$ into a grand saga of "interspecific competition driving range expansion and technological innovation"),
2. Or their work is dismissed as "merely descriptive."

This document establishes the foundational methodological stance of the `hominin-morphodynamics` project:
- **A formal mathematical model expands our descriptive capacity**, providing coordinate systems, bounding envelopes, and empirical variance metrics.
- **Descriptive capacity does not automatically license causal closure.**
- In the history and philosophy of science, there is a rich pluralism of explanatory forms—unificationist, structural, contrastive, and historical—under which disciplined mathematical description constitutes genuine, foundational explanation.
- **Circumspection is positive science:** identifying what a given empirical data regime *cannot* prove protects the integrity of the empirical baseline.

---

## 2. Pluralism in the Philosophy of Scientific Explanation

### A. The Unificationist Tradition (Whewell 1840, Friedman 1974, Kitcher 1981)
- **Core Principle:** An explanation does not require tracing every microscopic push-and-pull interaction. Instead, to explain a domain is to find the minimal set of generative argument patterns that subsumes and unifies the largest possible range of disparate empirical observations.
- **Darwin’s Method:** Charles Darwin could not provide a causal-mechanical trace of how beaks or limbs formed; he lacked genetics, developmental biology, and molecular mechanics. What Darwin provided was **consilience of inductions** (William Whewell): showing that a single branching genealogical schema unifies embryological homologies, vestigial organs, oceanic biogeography, and geological succession.
- **Application to Morphodynamics:** Defining the continuous geometric coordinate system of cranial and dental morphospace is unificationist: it organizes hundreds of isolated anatomical fragments into a coherent geometric manifold without needing fictional competitive micro-causes.

### B. The Structural and Mathematical Tradition (D’Arcy Thompson 1917, Batterman 2002, Lange 2013)
- **Core Principle:** Many of the most powerful scientific explanations are **structural, topological, or asymptotic**, not causal-mechanical. They explain why a phenomenon occurs by demonstrating that it is an invariant consequence of geometry, scale, or conservation laws.
- **Biological Precedent:** D’Arcy Wentworth Thompson’s *On Growth and Form* (1917) did not explain skull shapes or nautilus spirals through natural selection or behavioral combat; he explained them through physical and mathematical constraints on surface tension, shear, and coordinate transformations.
- **Application to Morphodynamics:** Mapping the volume and boundary envelope of a morphospace identifies the **structural constraints of viable mammalian anatomy**. Structural geometry explains why certain morphologies are physically, mechanically, or allometrically unviable, doing real explanatory work without narrative decoration.

### C. The Contrastive and Pragmatic Tradition (van Fraassen 1980, Garfinkel 1981, Lipton)
- **Core Principle:** Every scientific explanation is an answer to an **erotetic question** with an explicit contrast class:
  $$\text{"Why } P \text{ rather than } Q\text{?"}$$
- **Avoiding Vague Questions:** Asking broadly *"Why did hominins speciate?"* invites ungrounded storytelling.
- **Application to Morphodynamics:** Framing the question contrastively—*"Why does cranial capacity expand along the Homo trajectory while post-canine tooth area expands along the Paranthropus trajectory?"*—shifts the focus to observable functional, developmental, and dietary divergence vectors ($\delta^{13}\text{C}$ tooth enamel geochemistry, masticatory bite forces, neurocranial allometry), moving past abstract global birth-death rates.

### D. The Narrative and Historical Tradition (Gould 1989, Griesemer 1996)
- **Core Principle:** In deep-time historical sciences, explanation is inherently **configurational and contingent**. One cannot deduce the Pliocene hominins from universal laws plus boundary conditions.
- **Application to Morphodynamics:** Historical explanation is the rigorous reconstruction of an ordered sequence of contingent morphological states, where each preserved anatomical state sets the physical constraints for subsequent developmental modification.

---

## 3. Dovetailing Descriptive Capacity and Explanatory Circumspection

A mathematical model can dramatically enhance descriptive capacity without warranting causal overreach:

```text
┌────────────────────────────────────────────────────────┐
│             FORMAL MATHEMATICAL MODEL                  │
│  (State-space master equations, morphometric manifolds) │
└───────────────────────────┬────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│   DESCRIPTIVE CAPACITY    │ │  EXPLANATORY CIRCUMSPECTION│
│ - Geometric coordinates   │ │ - Preserves underdetermination
│ - Variance-covariance Σ  │ │ - Identifies non-identifiable
│ - Empirical rate vectors  │ │   parameter mixtures      │
│ - Bounding envelopes      │ │ - Distinguishes pattern   │
│                           │ │   from causal mechanism   │
└───────────────────────────┘ └───────────────────────────┘
```

### The Methodological Precedent: Sarah Blaffer Hrdy
A classic example of disciplined scientific advance is Sarah Blaffer Hrdy's work on maternal investment and alloparenting (*Mother Nature*, *Mothers and Others*):
- **She did not have to prove a totalizing thesis** that human sociality is "founded" on cooperative breeding, which would merely substitute one foundation myth for another.
- **She described a real empirical factor:** Through granular field observation of langurs and comparative human foraging groups, she documented allomaternal care, maternal trade-offs, and physiological plasticity.
- **She broke the clean deduction of her priors:** The Bateman-Trivers paradigm had deduced from first principles that males compete while females are passive, uniform investors. Describing alloparental care broke that tidy, ungrounded causal deduction.

Progress consisted of describing a factor and dethroning an oversimplified prior, without erecting a new metaphysical dogma.

---

## 4. The Mathematical Limits of Morphological Partitioning

Consider the total empirical variance-covariance matrix $\mathbf{\Sigma}_{\text{total}}$ of a set of hominin skull and tooth measurements preserved in fossil deposits:

$$\mathbf{\Sigma}_{\text{total}} = \mathbf{\Sigma}_{\text{allometry}} + \mathbf{\Sigma}_{\text{within-deme}} + \mathbf{\Sigma}_{\text{dimorphism}} + \mathbf{\Sigma}_{\text{drift}} + \mathbf{\Sigma}_{\text{taphonomy}}$$

Circumspection requires acknowledging what data is required to statistically partition this mixture:

1. **To isolate allometry and ontogeny ($\mathbf{\Sigma}_{\text{allometry}}$):**  
   Requires a complete developmental growth series (infants through adults of known developmental age). Isolated adult fossil fragments confound ontogenetic scaling with taxonomic difference.
2. **To isolate within-deme variation ($\mathbf{\Sigma}_{\text{within-deme}}$):**  
   Requires repeated contemporaneous samples from a single local population (e.g., Dmanisi $N=5$, a rare exception; across most Pliocene members, $N=1$ or $N=2$).
3. **To isolate sexual dimorphism ($\mathbf{\Sigma}_{\text{dimorphism}}$):**  
   Requires large, sex-controlled population cohorts, not isolated unassociated jaws.

### The Boundary of Proof
- **What is empirically determined:** The bounding envelope, total variance $\mathbf{\Sigma}_{\text{total}}$, and temporal distribution of cranial and dental dimensions preserved in the rock record.
- **What is mathematically underdetermined:** The exact causal partitioning of that variance between developmental plasticity, local allometry, sexual dimorphism, and macroevolutionary cladogenesis.

Models that claim to partition these components from sparse, unassociated fragments are fitting assumptions to non-identifiable mixtures.

---

## 5. Biological Plausibility vs. Empirical Proof

Because all terrestrial vertebrates share deep developmental, physiological, and genetic machinery, it is reasonable to presume that hominins experienced allometry, populational variance, and environmental constraints. Biological continuity across life forms is a sound prior.

However, **continuity does not license causal inference without data**:
- **Empirical proof requires data at both tiers simultaneously:**
  1. *At the individual level:* Ontogenetic series and physiological plasticity.
  2. *At the group level:* Complete demographic censuses, spatial boundaries, and genealogical splits.
- Where data exists at both tiers (laboratory microcosms, living bird populations, fully censused volcanic archipelagos like the Galápagos), model parameters are constrained by evidence.
- Where data exists at neither tier (17 scattered hominin fossil horizons across an open continent), the underlying biological processes were certainly operating, but the data cannot resolve them.

---

## 6. Conclusion: Circumspection as Positive Science

Epistemic circumspection is not skepticism or cynicism; it is the positive definition of empirical boundaries:
1. It separates the descriptive mathematical instrument from ungrounded causal storytelling.
2. It embraces structural, unificationist, and contrastive explanations where causal-mechanical tracing is impossible.
3. It preserves the integrity of empirical fossil measurements, ensuring that future researchers can build upon durable data rather than discarding superseded narrative models.
