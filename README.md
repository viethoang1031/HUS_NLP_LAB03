# LAB 03 - Word Representations and Embeddings

Bài làm mẫu (đáp án tham chiếu) cho LAB 03.

## Nội dung

- calculations.md: Bài 1 đến Bài 4, bài tập CBOW vs Skip-gram, bài tập analogy.
- prediction.md: 4 prediction trước thực nghiệm (Prediction, Reason, Confidence) và đối chiếu sau khi chạy.
- cooccurrence.py: build_vocabulary, build_cooccurrence_matrix, cosine_similarity, most_similar, ppmi (không dùng Word2Vec).
- word_embedding.ipynb: Experiment 1 đến 4, evaluation (similarity, analogy), application (semantic search), error analysis, polysemy. Output đã được chạy sẵn trong notebook.
- results.csv: kết quả số của tất cả thực nghiệm (cột experiment, setting, item, metric, value).
- error_analysis.md: 3 similarity đúng và 3 similarity bất ngờ.
- reflection.md: bảng so sánh các representation và câu hỏi về bank.

## Cài đặt và chạy

```powershell
pip install numpy scipy pandas scikit-learn gensim jupyter
cd LAB03
python cooccurrence.py
python -m jupyter nbconvert --to notebook --execute --inplace word_embedding.ipynb
```

Notebook cần file data/c4-train.00000-of-01024-30K.json ở thư mục gốc repository. Thời gian chạy khoảng 15 đến 20 phút, chủ yếu cho 5 lần huấn luyện Word2Vec.

## Quy ước

- Corpus: C4 30K documents (617,420 câu, 10,818,756 token). Tách câu bằng dấu câu và xuống dòng, lowercase, giữ chữ cái và apostrophe nội bộ, bỏ số.
- Co-occurrence: window đối xứng, chỉ đếm trong cùng một câu; từ ngoài vocabulary bị bỏ trước khi tính khoảng cách (giống Word2Vec).
- Core implementation dùng vocabulary 20,000 từ phổ biến nhất (min_count = 5). Ngoài vector count thô còn dùng PPMI vì vector count bị chi phối bởi từ tần suất cao.
- Word2Vec (gensim): CBOW (sg=0), negative sampling (negative=5), vector_size = 100, window = 5, min_count = 5, epochs = 10, seed = 42, workers = 1 (để tái lập kết quả).
- Experiment 3: window 2, 5, 10. Experiment 4: dimension 50, 100, 300 (window 5).
- Evaluation similarity: 5 cặp của đề và 24 cặp có điểm trực giác tự đặt (0 đến 10), đo bằng Spearman. Analogy: 170 câu thuộc 3 nhóm (capital-country, gender, comparative). Downstream: phân loại 90 từ vào 6 chủ đề bằng logistic regression, 5-fold cross-validation.
- Application: 10,000 document đầu của corpus, document vector là trung bình có trọng số IDF của word vector, so sánh với TF-IDF của LAB01.

## Kết quả chính

| Mục | Kết quả |
|-----|---------|
| Top-5 của doctor (Word2Vec) | dentist, physician, veterinarian, surgeon, therapist |
| doctor-physician / doctor-hospital / doctor-banana | 0.776 / 0.431 / -0.150 |
| Spearman 24 cặp: Word2Vec / co-occurrence PPMI | 0.791 / 0.674 |
| Analogy top-1 / top-5 (170 câu) | 0.535 / 0.724 |
| king - man + woman | queen (0.712) |
| Dimension 50 / 100 / 300: analogy top-1 | 0.482 / 0.535 / 0.535 |
| Dimension 50 / 100 / 300: thời gian huấn luyện (s) | 132 / 124 / 273 |

Ghi chú cho người chấm: các giá trị số có thể khác nhẹ nếu thay đổi phiên bản gensim hoặc tokenization; điều cần kiểm tra là kết luận định tính (doctor gần physician và dentist hơn banana, window lớn không luôn tốt hơn, dimension lớn không luôn tốt hơn, bank chỉ có một vector).
