"""LAB 03 - Co-occurrence word vectors (khong dung Word2Vec)."""
import json
import re
from collections import Counter

import numpy as np
from scipy import sparse

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
TOKEN = re.compile(r"[a-z]+(?:'[a-z]+)?")


def tokenize(text):
    return TOKEN.findall(text.lower())


def split_sentences(text):
    sentences = (tokenize(s) for s in SENTENCE_SPLIT.split(text))
    return [s for s in sentences if len(s) > 1]


def load_corpus(path, max_documents=None):
    """Doc file JSON lines (truong "text"), tra ve list cac cau (list token)."""
    sentences = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if max_documents is not None and i >= max_documents:
                break
            sentences.extend(split_sentences(json.loads(line)["text"]))
    return sentences


def build_vocabulary(sentences, min_count=1, max_size=None):
    """Tra ve dict word -> index, sap xep theo tan suat giam dan (hoa dong hang theo alphabet)."""
    counts = Counter(w for s in sentences for w in s)
    items = sorted(((w, c) for w, c in counts.items() if c >= min_count), key=lambda x: (-x[1], x[0]))
    if max_size is not None:
        items = items[:max_size]
    return {w: i for i, (w, _) in enumerate(items)}


def build_cooccurrence_matrix(sentences, vocabulary, window=1, chunk_size=20000):
    """X[i, j] = so lan tu j xuat hien trong cua so +-window quanh tu i (trong cung mot cau).
    Tu ngoai vocabulary bi bo truoc khi tinh khoang cach."""
    size = len(vocabulary)
    total = sparse.csr_matrix((size, size), dtype=np.float64)
    for start in range(0, len(sentences), chunk_size):
        rows, cols = [], []
        for sentence in sentences[start:start + chunk_size]:
            ids = np.fromiter((vocabulary[w] for w in sentence if w in vocabulary), dtype=np.int64)
            for d in range(1, window + 1):
                if len(ids) <= d:
                    break
                rows.append(ids[:-d]); cols.append(ids[d:])
                rows.append(ids[d:]); cols.append(ids[:-d])
        if rows:
            r, c = np.concatenate(rows), np.concatenate(cols)
            total = total + sparse.coo_matrix((np.ones(len(r)), (r, c)), shape=(size, size)).tocsr()
    return total


def ppmi(matrix):
    """Positive pointwise mutual information tu ma tran count."""
    matrix = sparse.csr_matrix(matrix)
    total = matrix.sum()
    row = np.asarray(matrix.sum(axis=1)).ravel()
    col = np.asarray(matrix.sum(axis=0)).ravel()
    coo = matrix.tocoo()
    pmi = np.log(coo.data * total / (row[coo.row] * col[coo.col]))
    keep = pmi > 0
    return sparse.csr_matrix((pmi[keep], (coo.row[keep], coo.col[keep])), shape=matrix.shape)


def cosine_similarity(u, v):
    u = np.asarray(u.todense()).ravel() if sparse.issparse(u) else np.asarray(u, dtype=float)
    v = np.asarray(v.todense()).ravel() if sparse.issparse(v) else np.asarray(v, dtype=float)
    norm = np.linalg.norm(u) * np.linalg.norm(v)
    return 0.0 if norm == 0 else float(u @ v / norm)


def word_vector(word, matrix, vocabulary):
    return matrix[vocabulary[word]]


def word_similarity(w1, w2, matrix, vocabulary):
    return cosine_similarity(word_vector(w1, matrix, vocabulary), word_vector(w2, matrix, vocabulary))


def most_similar(word, matrix, vocabulary, top_k=5):
    """Top-k tu gan nhat theo cosine (khong tinh chinh tu do)."""
    matrix = sparse.csr_matrix(matrix)
    index = vocabulary[word]
    norms = np.sqrt(np.asarray(matrix.multiply(matrix).sum(axis=1)).ravel())
    scores = matrix @ matrix[index].T
    scores = np.asarray(scores.todense()).ravel()
    with np.errstate(divide="ignore", invalid="ignore"):
        scores = np.where(norms > 0, scores / (norms * norms[index]), 0.0)
    scores[index] = -np.inf
    words = list(vocabulary)
    top = np.argsort(-scores)[:top_k]
    return [(words[i], float(scores[i])) for i in top]


if __name__ == "__main__":
    toy = [s.split() for s in [
        "the cat eats fish", "the dog eats fish", "the cat likes milk", "the dog likes meat"]]
    vocab = build_vocabulary(toy)
    X = build_cooccurrence_matrix(toy, vocab, window=1)
    print(list(vocab))
    print(X.toarray().astype(int))
    print(most_similar("cat", X, vocab, top_k=3))
