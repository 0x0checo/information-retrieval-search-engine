# Croatian News Information Retrieval: TF-IDF vs BM25 vs BM25+SBERT

This repository evaluates **ranking algorithms for a Croatian-language IR system** using a news-article setup where **article titles act as queries** and the corresponding **article bodies are the target documents**. We compare **TF-IDF**, **BM25**, and a **dual-stage BM25 + SBERT re-ranking** pipeline, and we also test whether **hand-annotated semantic similarity scores** between article pairs meaningfully improve retrieval. 

## Project Summary

* **Goal:** Identify the best-performing ranking approach for Croatian IR and check whether similarity-score annotations are useful. 
* **Main finding:** **BM25** performs best overall; **similarity scores have negligible impact** in our evaluation setting. 

## Dataset

We use data derived from **“Article-BERTic: Croatian article semantic similarity dataset”** (Ir2718, 2023). 
From the original paired format, we construct:

* **Document collection:** **2,109** unique news articles (id, title, body). 
* **Similarity pairs:** **313** article pairs with similarity score **≥ 4** (high similarity). 

## Methods

We compare three retrieval/ranking approaches: 

### 1) TF-IDF + Cosine Similarity (Baseline)

* Build a TF-IDF representation of documents
* Convert each **title query** into a TF-IDF vector
* Rank documents by cosine similarity and return **top-5** 

### 2) BM25

* Standard BM25 scoring with **k1 = 1.5**, **b = 0.75**
* Query is preprocessed the same way as documents
* Rank by BM25 score and return **top-5** 

### 3) Dual-Stage BM25 + SBERT Re-ranking

* Stage 1: Use **BM25** to retrieve top-k candidates
* Stage 2: Use multilingual **SBERT** to re-rank candidates by cosine similarity in embedding space
* SBERT variants tested:

  * `distiluse-base-multilingual-cased-v1`
  * `distiluse-base-multilingual-cased-v2`
* Candidate sizes tested: **k = 5, 25, 50, 100** 

## Preprocessing (Croatian)

Croatian is morphologically rich, so we normalize aggressively:

* Tokenize + lowercase + lemmatize using **CLASSLA** (`lang='hr'`)
* Remove punctuation + Croatian stopwords
* Cache lemmatized data (preprocessing takes ~**20 minutes**) 

## Evaluation

We evaluate using titles-as-queries and expect the paired body to be retrieved. Metrics: 

* **Accuracy@5:** % queries where the correct document is in top-5
* **Average Rank Position:** mean rank of the correct document when retrieved
* **MAP:** mean average precision
* **Similarity Score Usefulness (custom):** how often a highly similar paired article is *not* returned when its partner is retrieved (intended to estimate the added value of similarity links). 

## Results

Summary table (higher is better for Accuracy@5 and MAP; lower is better for Avg Rank): 

| Method   |   k | Accuracy@5 (%) | Avg Rank |        MAP | Sim. Score |
| -------- | --: | -------------: | -------: | ---------: | ---------: |
| TF-IDF   |   – |          94.22 |     1.39 |     0.8061 |     0.0002 |
| **BM25** |   – |      **95.78** | **1.31** | **0.8466** |     0.0001 |
| SBERT v1 |   5 |          95.78 |     1.78 |     0.7183 |     0.0001 |
| SBERT v1 |  25 |          75.44 |     1.74 |     0.5796 |     0.0002 |
| SBERT v1 |  50 |          69.46 |     1.72 |     0.5348 |     0.0003 |
| SBERT v1 | 100 |          64.58 |     1.71 |     0.5009 |     0.0003 |
| SBERT v2 |   5 |          95.78 |     1.62 |     0.7570 |     0.0001 |
| SBERT v2 |  25 |          84.07 |     1.59 |     0.6741 |     0.0002 |
| SBERT v2 |  50 |          80.65 |     1.57 |     0.6521 |     0.0002 |
| SBERT v2 | 100 |          78.24 |     1.55 |     0.6375 |     0.0002 |

**Takeaways**

* **BM25 is best overall**, slightly outperforming TF-IDF and outperforming BM25+SBERT on MAP/robustness. 
* **SBERT re-ranking gets worse as k increases**, likely due to a precision–recall trade-off and limited dataset size; v2 consistently beats v1. 
* **Similarity-score usefulness is extremely low (≈ 0.0001–0.0003)** in this setup; long, descriptive title queries already contain enough information to retrieve relevant documents without needing similarity links. 

## Runtime Notes

* Lemmatization + preprocessing: ~**20 minutes** (cached afterward). 
* SBERT with **k=100** can take ~**3 hours** in their environment, indicating compute constraints for embedding-heavy retrieval. 

## Limitations

* Dataset is relatively small (**2,109** docs; only **313** high-similarity pairs), which may limit the benefit of semantic re-ranking and similarity links. 
* Using titles as queries is efficient, but assumes essentially one “main” relevant document per query and may reduce the apparent value of similarity scores (titles are often long). 

## Ethical Considerations

News data can include personal information. Any future deployment should ensure proper licensing, and compliance with EU/Croatian data protection requirements. Retrieval ranking can also shape which stories gain visibility and influence public opinion. 

## Authors

Kai Garcia, Tin Cvrlje, Qin Wang, Wenyu Li (Uppsala University). 
