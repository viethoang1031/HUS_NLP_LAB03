# Reflection

## Bảng so sánh

| Representation | Context-dependent? | Sparse/Dense | Một từ có nhiều vector? |
|----------------|--------------------|--------------|--------------------------|
| TF-IDF | Không (trọng số theo tần suất từ trong document và corpus, không xét từ lân cận) | Sparse | Không (mỗi từ là một chiều, một giá trị cố định theo document) |
| Co-occurrence | Chỉ theo window cố định, gộp trên cả corpus nên một từ có một vector | Sparse (có thể giảm chiều thành dense) | Không |
| Word2Vec | Không (static embedding, vector học trên cả corpus) | Dense | Không |
| Contextual embedding | Có (vector phụ thuộc cả câu) | Dense | Có (mỗi lần xuất hiện có một vector khác nhau) |

## Tại sao bank cần contextual representation?

bank có ít nhất hai nghĩa: ngân hàng (I deposited money in the bank) và bờ sông (We sat on the river bank). Static Word2Vec chỉ có một vector cho bank, thực chất là trung bình có trọng số theo tần suất của mọi context mà bank từng xuất hiện. Trong thí nghiệm, vector bank gần currency, credit, banks (nghĩa tài chính) và gần như không có dấu vết nghĩa bờ sông (cos(bank, river) = 0.132, trong khi cos(bank, loan) = 0.493). Một điểm duy nhất trong không gian vector không thể vừa gần money vừa gần river, nên hai câu trên bị biểu diễn bằng cùng một vector cho bank.

Contextual embedding giải quyết vấn đề này bằng cách tính vector của bank từ toàn bộ câu chứa nó. Ở câu đầu, các từ deposited và money làm vector bank gần nghĩa tài chính; ở câu sau, river làm vector gần nghĩa bờ sông. Cơ chế này (attention trong Transformer) cho phép mỗi từ nhìn các từ khác trong câu để quyết định biểu diễn của chính nó, vì vậy Transformer là bước tiếp theo sau static embeddings.
