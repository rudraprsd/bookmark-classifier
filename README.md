# **Bookmark Classifier**

A machine learning pipeline that classifies browser bookmarks into predefined categories using parsed bookmark data and text embeddings.

![Bookmark Classifier](project_logo.png)
---

## **Overview**

This project takes a browser bookmarks HTML file, extracts bookmark titles and URLs, and assigns each bookmark to a category. The categories are derived from the leaf folders in the user’s own bookmark structure.

A combined text feature (`title + cleaned URL`) is used as input for model training.

---

## **Approach**

### **1. Feature Extraction**

* Parsed bookmark HTML to extract titles, URLs, and domain names
* Cleaned URLs by removing prefixes (`http`, `https`, `www`)
* Constructed a text feature: **title + clean URL**
* Added **domain name** as an additional categorical feature (OHE)

### **2. Vectorization**

* **TF-IDF** produced a highly sparse feature matrix (99.61% sparsity) → poor performance
* Switched to **Sentence Transformer embeddings** (`all-MiniLM-L6-v2`) for dense, semantic vectors

### **3. Models Evaluated**

* Logistic Regression
* Linear SVM
* Random Forest
* Multinomial Naive Bayes (TF-IDF only)

---

## **Results**

### **TF-IDF Baseline**

| Model               | Accuracy |
| ------------------- | -------- |
| Multinomial NB      | 20%      |
| Logistic Regression | 37.5%    |
| Linear SVC          | 45%      |
| Random Forest       | 40%      |

### **Sentence Transformer Embeddings**

| Model               | Accuracy |
| ------------------- | -------- |
| Logistic Regression | 52.5%    |
| Linear SVC          | 57.5%    |
| Random Forest       | 47.5%    |

### **Sentence Transformers + Domain Feature**

| Model                   | Accuracy  |
| ----------------------- | --------- |
| **Logistic Regression** | **62.5%** |
| Linear SVC              | 55%       |
| Random Forest           | 37.5%     |

**Best model:** Logistic Regression with SentenceTransformer embeddings + domain feature
**Current limitation:** Only ~400 bookmarks across ~20 categories → insufficient for higher accuracy.

---

## **Key Takeaways**

* Feature representation matters more than model complexity
* Dense embeddings outperform sparse TF-IDF for small datasets
* Multi-class NLP tasks require significantly more data (typically 2k–5k+ samples)

---

## **Future Work**

* [ ] Restructure the project into proper Python modules (`.py` files)
* [ ] Organize notebooks into clean, logical sections
* [ ] Collect more labeled bookmark data
* [ ] Experiment with stronger embedding models or fine-tuning

---