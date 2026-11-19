@author_edphos @author_flow @okr_morphodynamics_demonstration
Feature: Comparative Morphodynamics and Taphonomic Grounding
  As an evolutionary paleobiologist or quantitative morphodynamicist
  I require living behavioral proofs comparing insular carrying capacity models with sparse continental fossil data
  So that claims of diversity dependence are proven physically and statistically, while localized paleodemes provide a grounded exploratory lens

  Background:
    Given the canonical Galapagos terrestrial avifauna dataset from Valente et al. 2015
    And the Plio-Pleistocene hominin specimen occurrence database from Van Holstein & Foley 2024

  Scenario: Bounded Insular Radiation Demonstrates Identifiable Carrying Capacity
    When the Etienne continuous-time master equation evaluates Darwin's finches across carrying capacity K
    Then the log-likelihood profile must exhibit sharp penalization as K approaches the standing species count S
    And carrying capacity K must be statistically identifiable with likelihood-ratio p-value < 0.05
    And the physical invariant K >= S must be strictly enforced with log-likelihood of negative infinity when violated

  Scenario: Sparse Continental Hominin Data Yields Non-Identifiable Diversity Dependence
    When the Etienne master equation is applied to canonical Plio-Pleistocene Homo branching times across carrying capacity K
    Then the maximum log-likelihood variation across carrying capacity K from 8 to 500 must be less than 0.60 units
    And the profile likelihood must not reject the unconstrained null with p-value >= 0.25
    And the empirical MCMC credible intervals for speciation slope Gl must span zero across all published taxonomic schemes

  Scenario: Specimen Ingestion Identifies Stratigraphic Grime and Enforces Provenance
    When the raw hominin occurrence database is audited for physical chronological invariants
    Then exactly 5 published records must be flagged with inverted physical ages across site or stratigraphic horizons
    And more than 50% of the occurrences must be flagged as lacking bed-level stratigraphic resolution
    And the raw specimen records must be rectified without in-place mutation of Layer 0 provenance

  Scenario: Localized Spatio-Temporal Paleodemes Provide a Grounded Exploratory Lens
    Given the hominin occurrences have been audited and rectified
    When the rectified hominin occurrences are projected into localized paleodemes by sedimentary basin and ecological grade
    Then at least 50 distinct spatio-temporal paleodemes must be formed across the 0.5 Myr time slices
    And the paleodemes must partition specimens into regional basins including Turkana, Afar, Olduvai-Laetoli, and South African Karst
    And the resulting demographic clusters must serve as a plausible, non-dogmatic exploratory framework for underdetermined fossil data
