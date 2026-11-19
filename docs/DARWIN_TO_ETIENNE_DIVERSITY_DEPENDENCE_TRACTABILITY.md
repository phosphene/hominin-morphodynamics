# Deep Genealogy of Diversity Dependence: From Darwin's Wedges to Modern Data Realizations

**Coordinate:** `docs/DARWIN_TO_ETIENNE_DIVERSITY_DEPENDENCE_TRACTABILITY.md`  
**Namespace:** `morphodynamics.canonics`  
**Authors:** Ed Phil (@edphos), Marsyas (@Marsyas6), Flow (@feelingflowingbot)  
**Status:** Theoretical Genealogy, Mathematical Formalization, & Data Calibration  
**Date:** 2026-11-18  
**Repo:** `phosphene/hominin-morphodynamics`  

---

## 1. Executive Summary & Epistemic Trajectory

"Diversity dependence" did not begin as an equation; it began as an intuition about space, energetic limits, and the packing of forms in nature. 

Tracing this idea from Charles Darwin (1859) through Robert MacArthur (1967), Jack Sepkoski (1978), and Rampal Etienne (2012) answers three fundamental questions:
1. **When and how did diversity dependence become mathematically tractable?**
2. **What are its irreducible physical and mathematical components?**
3. **What amount and structure of data constitutes a "matching realization" where the parameters can actually be identified?**

---

## 2. Chronological Genealogy of Tractability

```text
1859: DARWIN'S METAPHORICAL GROUND (Origin of Species, Ch. 3 & 4)
      Concept: "Ten thousand sharp wedges packed close together" & "Places in the economy of nature".
      Status: Intractable qualitative intuition. Zero mathematical equations.
                        │
                        ▼
1934: MICROCOSMIC EXPERIMENTAL PROOF (G.F. Gause, The Struggle for Existence)
      Concept: Competitive Exclusion Principle. Two species cannot occupy the same niche.
      Mathematics: Lotka-Volterra competition equations: dn₁/dt = r₁n₁(1 - (n₁ + α₁₂n₂)/K₁).
      Components: Individual population counts n₁, n₂; carrying capacities K₁, K₂; interaction coefficients α.
      Matching Realization: Closed glass test tubes (Paramecium), daily censuses, constant food input.
                        │
                        ▼
1967: MACARTHUR & WILSON'S ISLAND BIOGEOGRAPHY (The Theory of Island Biogeography)
      Concept: Equilibrium species richness S* on closed oceanic islands.
      Mathematics: dS/dt = I(S) - E(S), where I(S) = I₀(1 - S/P) and E(S) = (E₀/A) · S.
      Components: Measured island area A, distance to mainland d, mainland pool P, standing species count S.
      Matching Realization: Bounded archipelago censuses (Krakatoa recolonization, Simberloff mangrove defaunation).
                        │
                        ▼
1978–1984: THE SEPKOSKI KINETIC MODEL (Paleobiology)
      Concept: Logistic macroevolutionary equilibrium of global taxonomic orders over the Phanerozoic.
      Mathematics: dD/dt = r D (1 - D / K).
      Components: Standing taxonomic diversity D (families/genera), intrinsic diversification r, global capacity K.
      Matching Realization: Sepkoski Marine Compendium (>3,500 families, >30,000 genera, global marine shelf record).
                        │
                        ▼
2008–2012: CONTINUOUS-TIME PHYLOGENETIC MASTER EQUATIONS (Rabosky 2008, Etienne 2012)
      Concept: Diversity-dependent cladogenesis with unobserved extinct lineages: P(n, t).
      Mathematics: Transition matrix ODE: dp_n/dt = λ_{n-1} p_{n-1} + μ_{n+1} p_{n+1} - (λ_n + μ_n) p_n.
                   λ(n) = max(0, λ₀(1 - n / K)).
      Components: Complete branching times {t₁...t_S}, baseline birth λ₀, death μ₀, carrying capacity K.
      Matching Realization: 100% complete molecular phylogenies of bounded radiations (Darwin's finches: 15/15 species).
                        │
                        ▼
2015: THE DAISIE ISLAND BIOTA ASSEMBLY (Valente, Phillimore, & Etienne 2015)
      Concept: Community-wide balance of colonization, anagenesis, cladogenesis, and area-limited extinction.
      Components: Island age T (4.0 Ma), mainland pool M (1,000), immigration γ, anagenesis λ_a, cladogenesis λ_c, extinction μ, K.
      Matching Realization: Full extant terrestrial avifauna of an entire volcanic hotspot archipelago (25 species, 8 clades).
```

---

## 3. The Epochs in Detail: Components & Data Realizations

### Epoch 1: Darwin (1859) — The Wedges and the Economy of Nature
In Chapters 3 ("Struggle for Existence") and 4 ("Natural Selection") of *On the Origin of Species*, Darwin introduced the physical intuition:
> *"The face of Nature may be compared to a yielding surface, with ten thousand sharp wedges packed close together and driven inwards by incessant blows, sometimes one wedge being struck, and then another with greater force."* (Origin, 1859, p. 67)
> 
> *"The more diversified the descendants from any one species become in structure, constitution, and habits, by so much will they be better enabled to seize on many and widely diversified places in the economy of nature, and so be enabled to increase in numbers."* (Origin, 1859, p. 112)

- **The Conceptual Invariant:** Space is finite; "places in the economy of nature" (niches) are packed; one wedge can only drive in by displacing another.
- **Why It Was Intractable:** Darwin had no formalization for rate of entry versus rate of displacement, no probability distribution for branching intervals, and no quantitative metric for niche volume.

---

### Epoch 2: MacArthur & Wilson (1963, 1967) — First Mathematical Tractability
Robert MacArthur and E.O. Wilson turned Darwin's verbal wedges into dynamical rates of immigration and extinction on islands.

#### The Core Equations:
$$\frac{dS}{dt} = \lambda_{\text{imm}}(S) - \mu_{\text{ext}}(S)$$

$$\lambda_{\text{imm}}(S) = I_0 \left(1 - \frac{S}{P}\right), \quad \mu_{\text{ext}}(S) = \left(\frac{E_0}{A}\right) S$$

At equilibrium ($\frac{dS}{dt} = 0$):
$$S^* = \frac{I_0 P}{I_0 + \frac{E_0 P}{A}}$$

#### Irreducible Components:
1. $A$: Bounded geographic area with clear ocean borders.
2. $d$: Distance isolating the system from mainland source pool $P$.
3. $S$: Total standing species richness on the island.
4. $I_0, E_0$: Baseline immigration and extinction coefficients.

#### Matching Data Realization:
- **Spatial Boundary:** Physical oceanic islands where the coastline is known.
- **Census Completeness:** Total species inventories (e.g., all vascular plants or nesting birds).
- **Time Horizon:** Monitored recolonization following complete defaunation (e.g., Krakatoa 1883–1933; Simberloff & Wilson 1969 mangrove island fumigation).

---

### Epoch 3: Sepkoski (1978, 1984) — Macroevolutionary Paleontological Kinetics
Jack Sepkoski brought MacArthur-Wilson into deep time, attempting to explain the global Phanerozoic marine curve.

#### The Core Equation:
$$\frac{dD}{dt} = r D \left(1 - \frac{D}{K}\right)$$

For multi-clade evolutionary faunas (Cambrian, Paleozoic, Modern):
$$\frac{dD_i}{dt} = r_i D_i \left(1 - \frac{\sum_j \alpha_{ij} D_j}{K_i}\right)$$

#### Irreducible Components:
1. $D(t)$: Global standing taxonomic diversity count at discrete geological stages.
2. $r$: Intrinsic per-taxon diversification rate.
3. $K$: Global marine carrying capacity.
4. $\alpha_{ij}$: Inter-faunal competitive interaction coefficients.

#### Matching Data Realization:
- **Scale:** Entire global marine fossil record (>3,500 families, >30,000 genera).
- **Stratigraphic Coverage:** Global, densely stacked shelf sediment beds spanning 540 million years.
- **Empirical Purchase:** Thousands of data points per time slice; diversity levels large enough that demographic noise averages out into smooth logistic trajectories.

---

### Epoch 4: Etienne (2012) & Valente et al. (2015) — Continuous-Time Markov Master Equations
Prior to Rampal Etienne's work, phylogenetic trees were evaluated using crude summary statistics (like Pybus & Harvey's $\gamma$-statistic) that assumed zero extinction or couldn't handle missing species without bias. Etienne solved the exact continuous-time Markov master equation $P(n, t)$.

#### The Core Master Equation:
$$\frac{d p_n(t)}{dt} = \lambda(n-1) p_{n-1}(t) + \mu(n+1) p_{n+1}(t) - [\lambda(n) + \mu(n)] p_n(t)$$

With linear diversity-dependent speciation:
$$\lambda(n) = \max\left(0, \, \lambda_0 \left(1 - \frac{n}{K}\right)\right), \quad \mu(n) = \mu_0$$

#### The DAISIE Island Community Extension (Valente et al. 2015):
Tracks colonization, anagenesis, cladogenesis, and extinction across multiple lineages sharing an archipelago:
$$\lambda^c(N) = \lambda_0^c \left(1 - \frac{N}{K}\right)$$
$$\gamma(M, N) = \gamma_0 \left(1 - \frac{N}{K}\right)$$

#### Irreducible Components:
1. $T$: Exact geological time horizon (time since volcanic island emergence).
2. $M$: Mainland source pool size.
3. $\{t_1, t_2, \dots, t_S\}$: Exact chronological sequence of internal branching times (coalescence horizons).
4. $\lambda_0$: Baseline cladogenesis rate in empty ecospace.
5. $\mu_0$: Background extinction rate.
6. $K$: Absolute carrying capacity ceiling.

#### Matching Data Realization:
- **Taxonomic Exhaustiveness:** 100% of extant species sampled (all 15 Darwin's finch species, all 4 mockingbirds, all single colonists).
- **Physical Boundaries:** Known volcanic island age ($T = 4.0\text{ Ma}$), measured isolation distance ($1,000\text{ km}$).
- **Precision:** Molecular gene trees providing high-resolution branching intervals down to $10,000$-year precision.
- **Identifiability:** Under this data regime, profile likelihood curves over $K$ exhibit sharp, clear global maxima ($K \approx 15\text{–}23$).

---

## 4. The Category Error: What Happens When Data Regimes Don't Match

The table below contrasts the data structure required for diversity dependence to be identifiable against the hominin reality:

| Dimension | Etienne / Galápagos Matching Realization | Van Holstein & Foley Hominin Reality | Ratio / Disparity |
|---|---|---|---|
| **Sampling Completeness** | $100\%$ ($25/25$ extant birds sequenced) | $< 5\%$ preserved fossil morphospecies | Complete vs. Severely Censored |
| **Branching Precision** | Molecular gene coalescence ($\pm 10^4\text{ yr}$) | Geological member dating ($\pm 10^5\text{–}10^6\text{ yr}$) | $10\times\text{ to }100\times$ temporal smear |
| **Geographic Bounding** | $8,000\text{ km}^2$ closed volcanic basalt | $84,000,000\text{ km}^2$ open continent | $10,000\times$ spatial area difference |
| **Initial Condition ($t=0$)** | Empty rock rising from sea ($N=0$) | Continuous primate occupation for $55+\text{ Ma}$ | Hard boundary vs. arbitrary truncation |
| **Lineages per Horizon** | High density ($15$ finch splits in $3\text{ Myr}$) | Average $1.8$ species per million-year bin | $8\times$ lower lineage density |
| **Likelihood Surface** | Sharp peak at finite $K$ ($\Delta \ln L > 5.0$) | Dead flat line ($\Delta \ln L \le 0.35, p \ge 0.25$) | **Identifiable vs. Non-Identifiable** |

### Conclusion
Diversity dependence is a legitimate mathematical concept, but **it requires a matching data realization**:
1. When applied to complete island archipelagos or massive global marine compendia, its parameters ($K, \lambda_0, \mu_0$) are physically grounded and statistically identifiable.
2. When applied to 17 fragmentary hominin fossil occurrences scattered across millions of square kilometers, the data contains zero mathematical mass to identify carrying capacity. The resulting "measurements" of competition are ungrounded narrative projections onto flat likelihood surfaces.
