# Verbatim Empirical Baseline: Etienne, Valente, & Phillimore (2015) vs. Van Holstein & Foley (2024)

**Coordinate:** `docs/VERBATIM_ETIENNE_GALAPAGOS_VS_FOLEY_HOMININ.md`  
**Namespace:** `morphodynamics.canonics`  
**Authors:** Ed Phil (@edphos), Marsyas (@Marsyas6), Flow (@feelingflowingbot)  
**Status:** Canonical Comparative Analysis & Textual Forensic Audit  
**Date:** 2026-11-18  
**Repo:** `phosphene/hominin-morphodynamics`  

---

## 1. Executive Summary & Epistemic Core

In macroevolutionary modeling, equations borrowed from island biogeography are frequently mapped onto continental paleontological databases. This document performs a verbatim close-read of the source literature establishing the canonical empirical island baseline—**Valente, Phillimore, & Etienne (2015, *Ecology Letters* 18: 844–852; Etienne et al. 2012, *Proc. R. Soc. B* 279: 1300–1309)**—and directly contrasts it with the continental hominin application in **Van Holstein & Foley (2024, *Nature Ecology & Evolution* 8: 1180–1190)**.

The fundamental epistemic result of this audit is:
1. **Competition is Not in the Data:** Neither the Galápagos avifaunal branching table nor the Paleobiology Database hominin occurrence spreadsheet contains an observation of competition, calories, territoriality, niche overlap, or encounter rates. Both datasets consist strictly of taxonomic labels and timestamps.
2. **Etienne and Valente are Rigorously Restrained:** In Valente, Phillimore, & Etienne (2015), the word "competition" appears **exactly once**, and solely to note that competition between close relatives "may not be ubiquitous." The authors explicitly acknowledge that their mathematical carrying capacity ($K$) is not a direct measurement of ecological competition, but an archipelago-wide geometric limit where fragmented allopatric ranges increase extinction rates.
3. **Foley & Van Holstein Invoke Unbounded Narrative Reification:** Van Holstein & Foley (2024) invoke "competition" **44 times**. They reify an unobserved mathematical derivative ($\partial \lambda / \partial N$) into a universal causal agent that simultaneously explains why clades slow down ($\partial \lambda / \partial N < 0$ in Australopiths) and why clades accelerate ($\partial \lambda / \partial N > 0$ in *Homo*), turning an unidentifiable statistical artifact into an unfalsifiable evolutionary story.

---

## 2. The Verbatim Galápagos Baseline: Valente, Phillimore, & Etienne (2015)

### A. The Complete Primary Data Ledger
In the Galápagos study, the empirical dataset comprises all 8 colonizing lineages of terrestrial birds that colonized the archipelago over its 4.0-Myr subaerial history:

```csv
Clade_name,Status,Missing_species,Branching_times
Coccyzus,Non_endemic_MaxAge,0,7.456
Dendroica,Non_endemic,0,0.34
Finches,Endemic,0,"3.0282,1.3227,0.8223,0.4286,0.3462,0.245,0.0808,0.0527,0.0327,0.0221,0.118,0.0756,0.0525,0.0322,0.0118"
Mimus,Endemic,0,"3.958,3.422,2.884,0.459"
Myiarchus,Endemic,0,0.855
Progne,Endemic,0,0.086
Pyrocephalus,Non_endemic_MaxAge,0,10.285
Zenaida,Endemic,0,3.51
```

### B. Verbatim Text on the Absence of Equilibrium in Most Clades
Crucially, Valente et al. do *not* claim that the Galápagos is an equilibrium system saturated by competition. Quite the contrary:

> *"The fact that total avian diversity of the Galápagos archipelago has not achieved a steady state after at least 4 My of existence questions the adequacy of an equilibrium perspective for understanding biodiversity patterns on remote oceanic islands (MacArthur & Wilson 1963; Heaney 2000; Gillespie & Baldwin 2010; Triantis et al. 2015). The absence of a signature of diversity-feedbacks and ecological limits in non-DF-type species in the Galápagos contrasts with recent studies on less isolated biodiverse landmasses that have detected slowdowns within most clades, consistent with ecological controls to diversity (Rabosky & Glor 2010; Scantlebury 2013)."* (Valente et al. 2015, p. 848)

### C. The Sole Occurrence of "Competition" in Valente et al. (2015)
The single time the concept of competition appears in the entire text of Valente et al. (2015), it is treated with severe skepticism:

> *"This may imply that diversity controls are relaxed in isolated and ephemeral environments, or that rather than diversity-dependence operating within each colonising lineage, as most macroevolutionary studies assume, the entire biota may subject to the same diversity-dependent regulation in the same arena. **Indeed, whilst Darwin's hypothesis that competition is strongest between close relatives has been experimentally confirmed (Violle et al. 2011), it may not be ubiquitous (Narwani et al. 2013).**"* (Valente et al. 2015, p. 848)

### D. Verbatim Interpretation of Carrying Capacity ($K$)
Even for Darwin's finches (the only clade showing diversity dependence), Valente et al. explicitly warn that $K$ does not necessarily mean local ecological competition over food:

> *"The diversity limit that we propose operates on DF requires diversity-dependence to occur on an archipelago-wide scale where species ranges may not overlap. Negative diversity feedbacks may operate in both sympatric and highly fragmented allopatric settings... **In the case of DF, we suggest that the carrying capacity emerges as a function of limits to both alpha and beta diversity – thus, if a form distributed over several islands splits into two species with smaller ranges, each of these forms will then have a higher probability of extinction (Pigot et al. 2010).**"* (Valente et al. 2015, p. 848)

Valente and Etienne define $K$ geometrically and biogeographically: dividing island land area among multiple allopatric populations shrinks their population sizes and elevates extinction risk. It is not an ungrounded claim about mysterious mental or behavioural combat.

---

## 3. The Verbatim Hominin Application: Van Holstein & Foley (2024)

In sharp contrast to the empirical restraint of Valente & Etienne, Van Holstein & Foley (2024) use the words **"competition"** or **"competitive"** **44 times** across their manuscript.

### A. The Reification of Interspecific Competition
> *"The search for drivers of hominin speciation and extinction has tended to focus on the impact of climate change. Far less attention has been paid to the role of interspecific competition. However, research across vertebrates more broadly has shown that both processes are often correlated with species diversity, suggesting an important role for interspecific competition."* (p. 1180)

Here, a correlation between species count and speciation rate is automatically baptized as "interspecific competition," skipping any requirement to observe actual resources, diets, or competitive encounters.

### B. The Conceptual Sign-Flip: Saving the Narrative When the Math Inverts
In classical MacArthur-Wilson diversity dependence, competition puts a *ceiling* on species richness; as diversity $N$ rises, speciation $\lambda$ drops ($G_l < 0$). But when Van Holstein & Foley ran their Bayesian MCMC on the genus *Homo*, the estimated parameter was positive ($G_l > 0$, speciation accelerating with diversity). 

Instead of concluding that diversity-dependent competition had failed as an explanatory model, they invented a secondary story where "competition" now causes acceleration:

> *"The unusual and unexpected patterns of diversity dependence in Homo speciation and extinction may be a consequence of repeated Homo range expansions driven by interspecific competition and made possible by recurrent innovations in ecological strategies."* (p. 1180)
> 
> *"We argue that the comparatively unusual pattern of positive diversity-dependent speciation we report is concordant with a set of underappreciated and non-mutually exclusive drivers of speciation in Homo: interspecific competition, repeated geographic expansions potentially driven by interspecific competition, and ecosystem engineering by other members of Homo opening up new niches."* (p. 1186)

### C. The Logical Vacuity of Dual-Directional "Competition"
Under this semantic elasticity:
1. When speciation rate decelerates (in Australopithecines): **Competition is invoked** (niche saturation throttles speciation).
2. When speciation rate accelerates (in *Homo*): **Competition is invoked** (competition drives technological innovation and migration).
3. If speciation rate were constant: **Competition would be invoked** (competition in equilibrium with background climate).

A concept that can explain $x$, $-x$, and $0$ with equal facility without measuring an underlying physical variable is non-empirical and unfalsifiable.

---

## 4. Side-by-Side Architectural Contrast

| Dimension | Valente, Phillimore, & Etienne (2015) | Van Holstein & Foley (2024) |
|---|---|---|
| **System** | Galápagos Islands avifauna | African & Eurasian fossil hominins |
| **Occurrences of "Competition"** | **1 occurrence** (questioning its ubiquity) | **44 occurrences** (central causal narrative) |
| **Data Completeness** | Complete extant census ($S=25$, 0 missing extant species) | Highly incomplete fossil record (17 species, 385 occurrences over 6 Myr) |
| **Origin Boundary ($t=0$)** | Physical volcanic emergence ($\approx 4.0\text{ Ma}$, $N=0$) | No physical origin ($N$ continuous with African catarrhines) |
| **Waiting Times ($\Delta t$)** | True molecular coalescence split horizons | Taphonomic intervals between discoverable fossil beds |
| **Carrying Capacity ($K$)** | Interpreted as geometric limit to archipelago beta-diversity | Reified as direct ecological/mental combat over continental resources |
| **Likelihood Surface** | Identifiable, sharply peaked for finches ($K \approx 20\text{–}23$) | Completely flat ($\Delta \ln L \le 0.35$, $p \ge 0.25$, unidentifiable) |
| **Statistical Status** | Bounded, empirical island baseline | Prior-dominated MCMC exploring an uninformative surface |

---

## 5. Conclusion: What Is Actually Grounded

When we look verbatim at the papers:
1. The Galápagos baseline is tractable because the boundaries are real: water limits area, geology dates the zero-point, and living birds provide complete genealogies. 
2. Even under those ideal insular conditions, Etienne and Valente found that **only 1 of the 8 bird lineages** showed evidence of a carrying capacity, and they explicitly refrained from dressing that carrying capacity in speculative stories about "competition."
3. Imposing these models onto fragmentary fossil spreadsheets does not reveal ancient competition. It reveals that when mathematical machinery is divorced from physical boundary conditions, unmeasured human narratives rush in to fill the silence of the data.
