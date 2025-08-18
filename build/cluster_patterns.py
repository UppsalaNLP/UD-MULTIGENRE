#!/usr/bin/env python
# coding: utf-8

from sklearn.feature_extraction.text import HashingVectorizer
import hdbscan

def cluster_strings_hdbscan(strings, min_cluster_size=10):
    # n-gram hashing
    vectorizer = HashingVectorizer(analyzer='char_wb', ngram_range=(2, 2), n_features=2**12, alternate_sign=False)
    X = vectorizer.transform(strings)

    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric='euclidean')
    labels = clusterer.fit_predict(X)

    # Group results
    clusters = {}
    for label, s in zip(labels, strings):
        clusters.setdefault(label, []).append(s)
    return clusters

def longest_common_substring(strings):
    if not strings:
        return ""
    
    shortest = min(strings, key=len)
    length = len(shortest)
    best = ""
    for i in range(length):
        for j in range(i + 1, length + 1):
            candidate = shortest[i:j]
            if len(candidate) > len(best) and all(candidate in s for s in strings):
                best = candidate
    return best
