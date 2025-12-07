# Bookmark Classifier

Classify you bookmarks into different categories.

## Overview

It takes your browser bookmarks HTML file as input, parses it to extract URLs and titles of the bookmarks, and then classifies them into predefined categories using machine learning models.

For training the models, I used my personal bookmark collection which is categorized into different folders. I considered the leaf directores as categories for classification (for MVP).

I parsed the URLs and used the clean URLs (without www, http, https, etc.) and combined with the title of the bookmark to make a new text feature.

First I used TF-IDF for vectorization and trained multiple models like Logistic Regression, Linear SVC, Random Forest, etc. I also used hyperparameter tuning using GridSearchCV to find the best parameters for the models.

The accuracy scores are as follows:
- Multinomial NB: 20.0%
- Logistic Regression: 37.5%
- Linear SVC: 45.0%
- Random Forest: 40.0%

Models are not performing well because of High-dimensional sparse TF-IDF matrix (99.61% sparsity).

The problem is not with the models but with the feature representation. So I switched to Sentence Transformers for better text embeddings.

I used the 'all-MiniLM-L6-v2' pre-trained model from Sentence Transformers to generate dense embeddings for the combined text feature (title + clean URL). Then I trained the same models on these embeddings. The accuracy scores improved significantly:
- Logistic Regression: 52.5%
- Linear SVC: 57.5%
- Random Forest: 47.5%

Agian I did some feature engineering by adding only domain name as an additional feature as OHE (One-Hot Encoding) vectors to the Sentence Transformer embeddings. This further improved the model performance:
- Logistic Regression: 62.5%
- Linear SVC: 55.0%
- Random Forest: 37.5%


The best performing model is Logistic Regression with Sentence Transformer embeddings and domain name feature with an accuracy of 62.5%.

But this is very low.

I need more data to train the models better. Currently I have only around 400 bookmarks which is very less for multi-class classification with around 20 categories.

## Lessons Learned
- Always start with simple models for comparison.
- Bias-Variance Tradeoff: Instead of using complex models, focus on better feature representation.
- You need around 2000-5000 data in total for NLP tasks for better performance.

## Conclusion
Need more data

## TODO
- [ ] Arange the code into proper format (from .ipyynb to .py files)
- [ ] Arange the .ipynb files into proper sections
