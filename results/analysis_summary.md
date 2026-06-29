# Analysis Summary

Complete idea/evaluation pairs: 84 across 12 contexts.
Best mean overall score: literature_comparison (4.00).
Best mean novelty-feasibility product: ungrounded (14.67).
Ungrounded baseline mean overall: 3.92.

## Omnibus Tests

| metric                      | test     |   n_contexts | conditions                                                                                         |   statistic |    p_value |
|:----------------------------|:---------|-------------:|:---------------------------------------------------------------------------------------------------|------------:|-----------:|
| novelty                     | Friedman |           12 | ungrounded,deduction,induction,proposal,outcome_imagination,small_experiment,literature_comparison |     8.60377 | 0.197118   |
| feasibility                 | Friedman |           12 | ungrounded,deduction,induction,proposal,outcome_imagination,small_experiment,literature_comparison |     7.28571 | 0.295231   |
| specificity                 | Friedman |           12 | ungrounded,deduction,induction,proposal,outcome_imagination,small_experiment,literature_comparison |     6.58537 | 0.360898   |
| grounding                   | Friedman |           12 | ungrounded,deduction,induction,proposal,outcome_imagination,small_experiment,literature_comparison |     3.81818 | 0.701265   |
| overall                     | Friedman |           12 | ungrounded,deduction,induction,proposal,outcome_imagination,small_experiment,literature_comparison |     9.31579 | 0.156582   |
| quality_mean                | Friedman |           12 | ungrounded,deduction,induction,proposal,outcome_imagination,small_experiment,literature_comparison |     8.43787 | 0.207746   |
| novelty_feasibility_product | Friedman |           12 | ungrounded,deduction,induction,proposal,outcome_imagination,small_experiment,literature_comparison |     4.77966 | 0.572368   |
| prior_overlap_fraction      | Friedman |           12 | ungrounded,deduction,induction,proposal,outcome_imagination,small_experiment,literature_comparison |    53.2143  | 1.0623e-09 |

## Pairwise Tests vs Ungrounded

| metric                      | condition             | baseline   |   n_contexts |    mean_diff |   median_diff |   paired_cohens_d |   wilcoxon_statistic |     p_value |   holm_p_value |
|:----------------------------|:----------------------|:-----------|-------------:|-------------:|--------------:|------------------:|---------------------:|------------:|---------------:|
| novelty                     | deduction             | ungrounded |           12 | -0.25        |     0         |       -0.4022     |                 24   | 0.375       |     1          |
| novelty                     | induction             | ungrounded |           12 | -0.333333    |     0         |       -0.511766   |                 20   | 0.21875     |     1          |
| novelty                     | proposal              | ungrounded |           12 | -0.166667    |     0         |       -0.23221    |                 29.5 | 0.6875      |     1          |
| novelty                     | outcome_imagination   | ungrounded |           12 | -0.25        |     0         |       -0.4022     |                 24   | 0.375       |     1          |
| novelty                     | small_experiment      | ungrounded |           12 | -0.416667    |     0         |       -0.809174   |                 14   | 0.0625      |     0.375      |
| novelty                     | literature_comparison | ungrounded |           12 |  0           |     0         |        0          |                 39   | 1           |     1          |
| feasibility                 | deduction             | ungrounded |           12 | -0.0833333   |     0         |       -0.288675   |                 33   | 1           |     1          |
| feasibility                 | induction             | ungrounded |           12 |  0.0833333   |     0         |        0.288675   |                 33   | 1           |     1          |
| feasibility                 | proposal              | ungrounded |           12 |  0           |     0         |        0          |                 39   | 1           |     1          |
| feasibility                 | outcome_imagination   | ungrounded |           12 |  0.0833333   |     0         |        0.288675   |                 33   | 1           |     1          |
| feasibility                 | small_experiment      | ungrounded |           12 |  0.0833333   |     0         |        0.288675   |                 33   | 1           |     1          |
| feasibility                 | literature_comparison | ungrounded |           12 | -0.0833333   |     0         |       -0.288675   |                 33   | 1           |     1          |
| specificity                 | deduction             | ungrounded |           12 | -0.25        |     0         |       -0.4022     |                 24   | 0.375       |     1          |
| specificity                 | induction             | ungrounded |           12 | -0.166667    |     0         |       -0.288675   |                 28.5 | 0.625       |     1          |
| specificity                 | proposal              | ungrounded |           12 |  0           |     0         |        0          |                 39   | 1           |     1          |
| specificity                 | outcome_imagination   | ungrounded |           12 | -0.166667    |     0         |       -0.288675   |                 28.5 | 0.625       |     1          |
| specificity                 | small_experiment      | ungrounded |           12 | -0.333333    |     0         |       -0.677003   |                 18   | 0.125       |     0.75       |
| specificity                 | literature_comparison | ungrounded |           12 | -0.166667    |     0         |       -0.428174   |                 27.5 | 0.5         |     1          |
| grounding                   | deduction             | ungrounded |           12 |  0.0833333   |     0         |        0.161835   |                 33.5 | 1           |     1          |
| grounding                   | induction             | ungrounded |           12 |  0.0833333   |     0         |        0.288675   |                 33   | 1           |     1          |
| grounding                   | proposal              | ungrounded |           12 |  0.0833333   |     0         |        0.288675   |                 33   | 1           |     1          |
| grounding                   | outcome_imagination   | ungrounded |           12 |  0.0833333   |     0         |        0.288675   |                 33   | 1           |     1          |
| grounding                   | small_experiment      | ungrounded |           12 |  0.0833333   |     0         |        0.288675   |                 33   | 1           |     1          |
| grounding                   | literature_comparison | ungrounded |           12 |  0.166667    |     0         |        0.428174   |                 27.5 | 0.5         |     1          |
| overall                     | deduction             | ungrounded |           12 | -0.166667    |     0         |       -0.288675   |                 28.5 | 0.625       |     1          |
| overall                     | induction             | ungrounded |           12 | -0.166667    |     0         |       -0.288675   |                 28.5 | 0.625       |     1          |
| overall                     | proposal              | ungrounded |           12 |  0           |     0         |        0          |                 39   | 1           |     1          |
| overall                     | outcome_imagination   | ungrounded |           12 | -0.0833333   |     0         |       -0.161835   |                 33.5 | 1           |     1          |
| overall                     | small_experiment      | ungrounded |           12 | -0.333333    |     0         |       -0.677003   |                 18   | 0.125       |     0.75       |
| overall                     | literature_comparison | ungrounded |           12 |  0.0833333   |     0         |        0.288675   |                 33   | 1           |     1          |
| quality_mean                | deduction             | ungrounded |           12 | -0.133333    |    -0.2       |       -0.346726   |                 19   | 0.117188    |     0.585938   |
| quality_mean                | induction             | ungrounded |           12 | -0.1         |    -0.1       |       -0.297842   |                 26.5 | 0.363281    |     1          |
| quality_mean                | proposal              | ungrounded |           12 | -0.0166667   |    -0.1       |       -0.057735   |                 32   | 0.5625      |     1          |
| quality_mean                | outcome_imagination   | ungrounded |           12 | -0.0666667   |     0         |       -0.206484   |                 30.5 | 0.539062    |     1          |
| quality_mean                | small_experiment      | ungrounded |           12 | -0.183333    |    -0.2       |       -0.635085   |                 14   | 0.0546875   |     0.328125   |
| quality_mean                | literature_comparison | ungrounded |           12 | -3.70074e-17 |     0         |       -1.4465e-16 |                 34   | 0.734375    |     1          |
| novelty_feasibility_product | deduction             | ungrounded |           12 | -1.33333     |     0         |       -0.511766   |                 20   | 0.21875     |     1          |
| novelty_feasibility_product | induction             | ungrounded |           12 | -1           |     0         |       -0.331662   |                 25.5 | 0.453125    |     1          |
| novelty_feasibility_product | proposal              | ungrounded |           12 | -0.666667    |     0         |       -0.199637   |                 30.5 | 0.726562    |     1          |
| novelty_feasibility_product | outcome_imagination   | ungrounded |           12 | -0.666667    |     0         |       -0.23221    |                 29.5 | 0.6875      |     1          |
| novelty_feasibility_product | small_experiment      | ungrounded |           12 | -1.33333     |     0         |       -0.511766   |                 20   | 0.21875     |     1          |
| novelty_feasibility_product | literature_comparison | ungrounded |           12 | -0.333333    |     0         |       -0.124646   |                 34   | 1           |     1          |
| prior_overlap_fraction      | deduction             | ungrounded |           12 |  0.033776    |     0.0378046 |        2.21726    |                  0   | 0.000488281 |     0.00292969 |
| prior_overlap_fraction      | induction             | ungrounded |           12 |  0.0493133   |     0.0481157 |        2.46139    |                  0   | 0.000488281 |     0.00292969 |
| prior_overlap_fraction      | proposal              | ungrounded |           12 |  0.0302912   |     0.0303066 |        2.21066    |                  0   | 0.000488281 |     0.00292969 |
| prior_overlap_fraction      | outcome_imagination   | ungrounded |           12 |  0.0163011   |     0.013382  |        1.13929    |                  5   | 0.00488281  |     0.00488281 |
| prior_overlap_fraction      | small_experiment      | ungrounded |           12 |  0.022314    |     0.0202499 |        1.74476    |                  0   | 0.000488281 |     0.00292969 |
| prior_overlap_fraction      | literature_comparison | ungrounded |           12 |  0.0625649   |     0.0646632 |        2.83507    |                  0   | 0.000488281 |     0.00292969 |