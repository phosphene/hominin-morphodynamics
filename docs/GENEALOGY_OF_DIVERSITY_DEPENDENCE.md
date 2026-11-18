# The Genealogy of "Diversity Dependence": From Island Demography to Paleontological Storytelling

**Coordinate:** `docs/GENEALOGY_OF_DIVERSITY_DEPENDENCE.md`  
**Namespace:** `morphodynamics.canonics`  
**Authors:** Ed Phil (@edphos), Marsyas (@Marsyas6), Flow (@feelingflowingbot)  
**Status:** Theoretical Genealogy & Epistemic Audit  
**Date:** 2026-11-18  
**Repo:** `phosphene/hominin-morphodynamics`  

---

## 1. Executive Summary

"Diversity dependence" is currently treated in evolutionary anthropology as an established, off-the-shelf macroevolutionary law—an empirical mechanism that can be loaded into Bayesian MCMC software (PyRate) and fitted to hominin fossil occurrence sheets.

This document traces the historical, conceptual, and mathematical genealogy of the term. It demonstrates that:
1. **The concept underwent four distinct conceptual shifts**, mutating from a physical, spatial equilibrium model of bounded islands into an unbounded, abstract narrative bucket applied to continental bone fragments.
2. **The mathematics shifted from bounded carrying capacities to unbounded exponential hazards**, obscuring non-identifiability.
3. **The empirical content evaporated along the way**: what began as countable birds landing on visible basalt was transformed into ungrounded narrative labels applied to uninformative fossil timestamps.

---

## 2. The Four Stages of the Genealogy

```text
STAGE 1: Ecological Demography on Islands (MacArthur & Wilson 1963, 1967)
         Physical island area A < ∞, immigration rate λ_imm, extinction rate μ_ext.
         Equilibrium species number S* where immigration balances extinction.
         Competition is spatial/energetic packing of living organisms on closed land.
                              │
                              ▼
STAGE 2: Paleontological Equilibrium & Logistic Clades (Raup, Gould, Sepkoski 1970s–1980s)
         Extension from ecological time (years) to geological time (hundreds of millions of years).
         Global Phanerozoic marine curve: dD/dt = r D (1 - D / K).
         Sepkoski's three evolutionary faunas; adaptive grids (Walker & Valentine 1984).
         Diversity dependence becomes an abstract macro-taxonomic property of phyla.
                              │
                              ▼
STAGE 3: Molecular Phylogenetics & Lineage-Through-Time Slowdowns (Rabosky 2008, Etienne 2012)
         Observation that molecular phylogenies show branching rate slowdowns toward the present.
         Mathematical formalization: Continuous-time master equations P(n, t).
         Linear diversity-dependent cladogenesis: λ(n) = max(0, λ₀(1 - n / K)).
         Tractable in bounded insular radiations (Darwin's finches; Valente et al. 2015).
         Extreme mathematical restraint: K is interpreted as allopatric island fragmentation, NOT direct combat.
                              │
                              ▼
STAGE 4: Exponential Bayesian Hazard on Fossil Occurrences (Silvestro 2014, Van Holstein & Foley 2024)
         Elimination of the hard ceiling K; replaced with exponential hazard: λ(D) = λ₀ exp(G_l · D).
         Applied to continental hominin fossils (17 species, 385 occurrences across 6 Myr).
         Likelihood surface is completely flat (p ≥ 0.25).
         Narrative Reification: G_l < 0 = "competition throttles speciation"; G_l > 0 = "competition drives speciation".
         "Competition" becomes an unmeasured, unfalsifiable explanatory ghost.
```

---

## 3. Deep Dive into the Intellectual Epochs

### Stage 1: The MacArthur-Wilson Equilibrium (1963, 1967)
- **Primary Source:** Robert H. MacArthur & Edward O. Wilson, *The Theory of Island Biogeography* (1967).
- **Domain:** Closed oceanic islands of measured surface area $A$ located at distance $d$ from a continental source pool $P$.
- **Mechanism:** Immigration rate $\lambda$ drops as island richness $S$ approaches source pool $P$ (fewer novel migrants). Extinction rate $\mu$ increases with $S$ because fixed island area $A$ forces smaller average population sizes per species ($N_i \approx A / S$), increasing vulnerability to demographic stochasticity.
- **Role of Competition:** Competition is **direct, local, and physical**. Individuals of competing species occupy the same finite hectare of vegetation or soil.
- **Empirical Status:** Grounded, measurable, and falsified/verified by defaunation experiments (Simberloff & Wilson 1969).

### Stage 2: The MBL Paleontological Turn & Sepkoski's Kinetic Model (1970s–1980s)
- **Primary Sources:** Raup, Gould, Schopf, & Simberloff (1973); Sepkoski (1978, 1984); Walker & Valentine (1984).
- **The Shift:** The Marine Biodiversity Laboratory (MBL) group attempted to see if global marine biodiversity through the Phanerozoic could be modeled as an equilibrium system analogous to MacArthur-Wilson.
- **The Kinetic Equation:** Sepkoski wrote down a coupled logistic differential equation for global taxonomic orders:
  $$\frac{dD}{dt} = r D \left(1 - \frac{D}{K}\right)$$
- **The Epistemic Mutation:** Notice what happened to $K$:
  - In MacArthur-Wilson, $K$ was an island's acreage and primary productivity.
  - In Sepkoski, $K$ became an abstract "global marine ecospace capacity" for thousands of genera over 500 million years.
- **The Warning:** Even then, Stephen Jay Gould cautioned that taxonomic counts in fossil databases reflect sedimentary rock volume and sampling bias rather than pure biological carrying capacities.

### Stage 3: Molecular Phylogenetics & Etienne's Master Equation (2008–2015)
- **Primary Sources:** Rabosky & Lovette (2008); Etienne et al. (2012, *Proc. R. Soc. B*); Valente, Phillimore, & Etienne (2015, *Ecology Letters*).
- **The Empirical Driver:** The rise of molecular phylogenies revealed that Lineage-Through-Time (LTT) plots for many clades exhibit an apparent slowdown in branching rate as they approach the present.
- **The Competing Hypotheses:**
  1. *Ecological limits:* Niche space is filling up, depressing cladogenesis ($\lambda(n) = \lambda_0(1 - n/K)$).
  2. *Protracted speciation:* Speciation takes time ($1\text{–}2\text{ Myr}$); nascent lineages have not yet split into recognized biological species (Etienne & Rosindell 2012).
  3. *Incomplete sampling / artifact:* Missing cryptic species or lineage-extinction pull-of-the-present.
- **The Galápagos Verification:** When Valente, Phillimore, & Etienne (2015) built the DAISIE framework to test this on the Galápagos avifauna:
  - **7 out of 8 clades showed NO diversity dependence.**
  - Only Darwin's finches supported a finite $K$.
  - **Valente & Etienne explicitly warned against calling $K$ "competition"**: they interpreted $K$ as an archipelago-wide geometric limit where fragmented allopatric ranges increase extinction rates. The word "competition" appeared **once** in their paper, solely to express skepticism.

### Stage 4: Bayesian Fossil Inversion & The Foley Reification (2014–2024)
- **Primary Sources:** Silvestro et al. (2014, *Syst. Biol.*); Van Holstein & Foley (2024, *Nature Ecology & Evolution*).
- **The Mathematical Mutation:**
  In PyRate, Silvestro abandoned Etienne's hard ceiling $K$ because hard cutoffs cause MCMC samplers to reject proposals whenever simulated diversity crosses $K$. He replaced it with an unbounded exponential hazard:
  $$\lambda(D) = \lambda_0 \exp(G_l \cdot D)$$
- **The Application to Hominins:**
  Van Holstein & Foley applied this exponential hazard to 17 hominin taxa represented by 385 fossil occurrences across 6 million years of African geology.
- **The Breakdown of Identifiability:**
  Because the hominin fossil record contains an average of only 1 to 3 preserved morphospecies per million-year horizon, the likelihood surface over $G_l$ is completely flat ($\Delta \ln L \le 0.35, p \ge 0.25$). 
  The 95% credible intervals for *Homo* span zero in every model ($[-1.80, +6.24]$).
- **The Reification of the Unmeasured:**
  Instead of reporting non-identifiability, the authors invoked the word "competition" **44 times**. When the MCMC output a positive mean slope ($G_l > 0$), they invented an ad-hoc evolutionary narrative claiming that competition "drives range expansion and technological innovation."

---

## 4. The Conceptual Erosion: What Disappeared Along the Way

| Feature | Stage 1: MacArthur-Wilson (1967) | Stage 3: Etienne / Galápagos (2012–2015) | Stage 4: Foley / Hominins (2024) |
|---|---|---|---|
| **Physical Space** | Closed volcanic rock ($A < \infty$) with ocean barriers | Closed archipelago ($A = 8,000\text{ km}^2$) with ocean barriers | Open, unbounded continental landmass (Africa + Eurasia) |
| **Origin ($t=0$)** | Physical emergence of basalt ($t=0, N=0$) | Hotspot dating ($4.0\text{ Ma}, N=0$) | No origin; continuous with catarrhine primates for $55+\text{ Ma}$ |
| **Observation** | Countable living bird populations | Complete extant molecular genealogies | Fragmentary bones scattered across $6\text{ Myr}$ |
| **Waiting Times ($\Delta t$)** | Direct dispersal/survival intervals | True biological gene coalescence | Meters of sediment between lucky lacustrine beds |
| **Carrying Capacity ($K$)** | Energetic food ceiling per hectare | Geometric fragmentation / allopatric extinction limit | Unbounded, unmeasured abstraction |
| **Word "Competition"** | Used for observed seed/forage overlap | **Used 1 time** (doubting ubiquity) | **Used 44 times** (reified causal narrative) |
| **Falsifiability** | High (direct defaunation tests) | High (profile likelihood has sharp peak) | **Zero (profile likelihood dead flat, $p \ge 0.25$)** |

---

## 5. Conclusion

The genealogy of "diversity dependence" is a textbook case of **methodological drift**:
1. It began as a physical model of islands, where space and organisms are directly observable.
2. It was abstracted into paleontological kinetic equations where $K$ lost its physical boundaries.
3. In modern phylogenetics, rigorous practitioners like Etienne and Valente applied it with extreme mathematical restraint, explicitly rejecting naive competitive storytelling.
4. Finally, in continental paleoanthropology, it was decoupled from data entirely: loaded into Bayesian MCMC software to fit uninformative fossil timestamps, while an unobserved, multi-directional concept of "competition" was invoked to explain whatever sign the prior-dominated sampler returned.
