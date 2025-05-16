# CMHLU
## README: Modeling Non-Native Speaker Use of Non-Veridical Preferential Predicates + Wh-Clauses with RSA

**Coursework for:** Cognitive models of human language understanding

**Original Model Base:** Vanilla RSA model from the seminar (adapted).

**Goal of this Notebook:**
This notebook aims to explore the conditions under which non-native English speakers (L2 speakers) might produce or be interpreted as using non-veridical preferential predicates followed by wh-clauses. Examples include utterances like "I hope what will happen" or "She fears who might come," which can be ungrammatical, marked, or interpreted differently by native English speakers compared to standard constructions (e.g., "I hope that something good will happen," "She fears that X might come," or "I wonder what will happen").

**Methodology:**
The Rational Speech Act (RSA) framework is employed. RSA models pragmatic reasoning in communication, where listeners infer a speaker's intended meaning by considering why the speaker chose a particular utterance from a set of alternatives, given their literal meanings, costs, and the speaker's presumed goals.

This notebook extends a basic RSA model to differentiate between:
1.  A **Native Speaker Model**: Assumes the speaker has standard English grammar and pragmatic norms. Marked constructions like "hope-wh" would have a high cost or a very low prior probability of being uttered.
2.  A **Non-Native Speaker Model**: Allows for the possibility that L2 speakers might have different production probabilities (priors) for these marked constructions (perhaps due to L1 influence, overgeneralization of L2 rules, or different perceived utterance costs).

The model explores how a pragmatic listener (L1) might interpret such utterances, particularly focusing on how the listener's assumptions about the speaker (native vs. non-native) influence their interpretation of the speaker's intended meaning (e.g., the speaker's underlying desires or preferences).

**Key Parameters Explored (Illustrative Example: "hope-wh")**:
* **Objects/States (o):** Represent the speaker's underlying desire regarding an uncertain situation 'S'.
    * `o1 (desire_positive_S)`: Speaker desires a positive outcome for S.
    * `o2 (uncertain_about_S)`: Speaker is uncertain/information-seeking about S.
* **Messages (m):** The utterances a speaker might choose.
    * `m1 ("hope that S_good")`: "I hope that S turns out good." (Standard, explicitly positive preference)
    * `m2 ("wonder what S")`: "I wonder what S will be." (Standard, information-seeking)
    * `m3 ("hope what S")`: "I hope what S will be." (Target marked/L2 utterance)
* **Truth Table (Semantics):** Literal mapping of messages to speaker states. For `m3`, it's assumed that if uttered, it still fundamentally conveys a hope for a good outcome for S, similar to `m1`.
* **Costs of Utterances (C(m)):** `m3` might have a higher cost in the native speaker model than in the non-native model (or when a listener models an L2 speaker).
* **Priors over Speaker Utterances (P(m)):** `P(m3)` is assumed to be lower for native speakers than for non-native speakers.
* **Speaker Optimality (alpha):** Controls how rationally the speaker chooses utterances to maximize utility.

**Expected Outcome (Illustrative):**
The model aims to demonstrate how changes in utterance costs and priors (reflecting native vs. non-native speaker characteristics) can affect the pragmatic listener's interpretation. For instance, a listener might be more likely to infer a coherent desire (e.g., speaker hopes for a good outcome for S) from the marked utterance `m3` if they model the speaker as non-native, for whom `m3` might be less costly or have a higher prior probability.

**How to Use the Notebook:**
1.  Ensure you have Python installed with Jupyter Notebook or JupyterLab. Alternatively, upload the `.ipynb` file (`RSA_Non_Veridical_L2.ipynb`) to Google Colab.
2.  Install the required libraries listed in `requirements.txt` (e.g., using `pip install -r requirements.txt`).
3.  Open and run the cells in the Jupyter Notebook sequentially. The plots will be displayed inline and also saved as PNG files in the same directory where the notebook is run.
