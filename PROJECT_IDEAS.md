# Final Project Proposal (Computational Linguistics)
 
## Title
 
**Morphosyntax-Only Dependency Parsing Across Typologies: Czech vs. English UD**
 
## Exact Methods (course-aligned, manageable workload)

**One-sentence methods summary:** Use a graph-based biaffine-style dependency parser with Chu-Liu-Edmonds MST decoding to compare lexicalized, morphosyntax-only (gold UPOS+UFeats), and mixed representations on UD Czech-PDT vs. UD English-EWT.

* **Parser**: Graph-based dependency parsing with a neural arc and label scorer (reuse the existing graph-based/biaffine-style parser implementation from the dependency parsing assignment).
* **Decoding**: **Chu-Liu-Edmonds** maximum spanning tree decoding (as covered in the course for graph-based dependency parsing).
* **Datasets (fixed choice)**:
  * **Czech**: UD Czech-PDT (morphologically rich, seven cases, relatively free word order)
  * **English**: UD English-EWT (analytic morphology, fixed word order)
* **Controlled representation conditions (core contribution)**:
  1. **Lexicalized baseline**: Word or subword identity as input (same setup as the assignment baseline).
  2. **Morphosyntax-only**: Inputs restricted to **UPOS + UD morphological features (UFeats)** only, with learned embeddings for these discrete features. No lexical identity.
  3. **Mixed**: Lexical identity + morphosyntax (reference upper bound).
* **Training setup note**:
  * If a pretrained encoder is used in the lexicalized condition, it can optionally be **frozen** to make comparisons primarily about the availability of lexical identity vs. morphosyntax. This does **not** apply to the morphosyntax-only condition, which uses only learned embeddings for UPOS/UFeats.
 
## Description
 
Dependency parsing makes hidden syntactic structure explicit by predicting head–dependent relations, but current neural parsers conflate multiple information sources: lexical identity, contextual embeddings, and morphosyntactic cues. Prior work on delexicalized parsing (Zeman & Resnik, 2008; McDonald et al., 2011) demonstrated that parsers can transfer across languages when lexical features are removed, but left open a finer-grained question: **which specific dependency relations are recoverable from morphosyntax alone, and how does this vary with a language's typological profile?** This project addresses that question through controlled ablations on two typologically distinct languages.
 
I will train a standard graph-based parser with Chu-Liu-Edmonds MST decoding on **UD Czech-PDT** and **UD English-EWT**, keeping the parsing architecture fixed and varying only the input representations across three conditions: lexicalized, morphosyntax-only (UPOS + UFeats), and mixed. This isolates the structural signal contributed by morphosyntactic features such as case, number, person, and agreement.
 
**Hypothesis (falsifiable, quantitative):** I predict that **core argument relations** (`nsubj`, `obj`, `iobj`) will show a smaller LAS drop under delexicalization in Czech than in English—specifically, **<5 points in Czech vs. >15 points in English**—because Czech overt case marking (nominative, accusative, dative) directly signals grammatical function. In contrast, **modifier relations** (`amod`, `advmod`, `nmod`) will degrade more uniformly across both languages, since these rely more on lexical selectional preferences than morphological marking.
 
**Evaluation and diagnostics:**
- **UAS and LAS** on held-out test sets, overall and broken down by dependency label.
- **Accuracy drop (Δ)** per relation: (lexicalized LAS) − (morphosyntax-only LAS), compared across languages.
- **Error confusion matrices** for mispredicted labels: e.g., does `nsubj` get confused with `obj` more often in English than in Czech under delexicalization? This tests whether case marking reduces argument confusability.
- **Dependency length analysis**: accuracy by arc length to test whether morphosyntax helps more for local vs. long-distance dependencies.
 
The deliverable is a **robustness map** showing which dependency relations are predictable from morphosyntax alone versus which depend on lexical identity, compared across typologically distinct languages. This directly addresses the computational linguistics goal of making hidden structure explicit: I quantify which observable linguistic signals (morphological features) encode which parts of syntactic structure (dependency relations), and how this encoding varies with language typology.
 
---
 
## References
 
- Dozat, T., & Manning, C. D. (2017). Deep biaffine attention for neural dependency parsing. In *Proceedings of ICLR*.
- McDonald, R., Petrov, S., & Hall, K. (2011). Multi-source transfer of delexicalized dependency parsers. In *Proceedings of EMNLP* (pp. 62–72).
- Nivre, J. (2008). Algorithms for deterministic incremental dependency parsing. *Computational Linguistics*, 34(4), 513–553.
- Zeman, D., & Resnik, P. (2008). Cross-language parser adaptation between related languages. In *Proceedings of the IJCNLP Workshop on NLP for Less Privileged Languages*.
- de Lhoneux, M., Shao, Y., Basirat, A., Kiperwasser, E., Stymne, S., Goldberg, Y., & Nivre, J. (2017). From raw text to Universal Dependencies—Look, no tags! In *Proceedings of CoNLL*.
- Nivre, J., et al. (2020). Universal Dependencies v2: An evergrowing multilingual treebank collection. In *Proceedings of LREC*.
