@author_edphos @author_flow @okr_morphodynamics_demonstration
Feature: Simulation and Recovery of Diversity-Dependent Avifaunal Radiation
  As an evolutionary paleobiologist or quantitative morphodynamicist
  I require forward continuous-time simulations of insular adaptive radiations under known ecological limits
  So that the Etienne master equation's parameter recovery, boundary invariants, and carrying capacity profiles are verified against known ground truth

  Background:
    Given the empirical Darwin finches radiation parameters from Valente et al. 2015
      | parameter           | value  | unit           | description                             |
      | crown_age           | 3.0282 | Myr            | Time before present of crown divergence |
      | lambda_0            | 1.50   | Myr^-1         | Baseline speciation rate                |
      | mu_0                | 0.20   | Myr^-1         | Background extinction rate              |
      | carrying_capacity_K | 20.0   | species        | Equilibrium carrying capacity limit     |
      | standing_richness_S | 15     | species        | Observed extant species count           |

  Scenario: Forward Stochastic Simulation Replicates Realized Finches Richness and Cladogenesis
    Given a continuous-time Gillespie birth-death simulator initialized with 2 crown lineages
    When the simulation executes forward for 3.0282 Myr under the canonical diversity-dependence function
    Then the surviving clade must reach an extant richness S between 12 and 22 species
    And the temporal distribution of branching events must reflect early cladogenetic burst
    And the reconstructed tree must satisfy the exact topological invariant of S minus 1 branching nodes

  Scenario: Inverse Master Equation Recovers Known Carrying Capacity from Synthetic Clade
    Given a simulated phylogenetic tree generated under true carrying capacity K = 20.0
    When the Etienne master equation computes the profile log-likelihood across a candidate grid of K from 16 to 100
    Then candidate K values violating physical standing richness must evaluate to negative infinity
    And the maximum likelihood estimate hat_K must fall within an acceptable recovery band of the true parameter K = 20.0
    And the unconstrained diversification model at K = 100 must be penalized relative to the peak carrying capacity

  Scenario: Simulation-Based Calibration Distinguishes True Capacity from Unbounded Expansion
    Given an ensemble of forward-simulated trees under true bounded capacity K = 20.0
    And an ensemble of forward-simulated trees under unbounded diversification
    When both ensembles are inverted through the carrying capacity profiler
    Then the bounded simulations must exhibit an interior likelihood maximum near true capacity
    And the unbounded simulations must show monotonically non-decreasing likelihood toward large K
