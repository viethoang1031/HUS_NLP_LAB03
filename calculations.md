# Calculations

## Bài 1 - Co-occurrence

Corpus:

```text
the cat eats fish
the dog eats fish
the cat likes milk
the dog likes meat
```

Window k = 1, chỉ đếm các từ nằm cùng câu. Các từ context (cột), theo thứ tự: the, cat, dog, eats, likes, fish, milk, meat.

cat:
- câu 1: the, eats
- câu 3: the, likes

dog:
- câu 2: the, eats
- câu 4: the, likes

eats:
- câu 1: cat, fish
- câu 2: dog, fish

likes:
- câu 3: cat, milk
- câu 4: dog, meat

Ma trận word-context:

| Word | the | cat | dog | eats | likes | fish | milk | meat |
|------|-----|-----|-----|------|-------|------|------|------|
| cat | 2 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| dog | 2 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| eats | 0 | 1 | 1 | 0 | 0 | 2 | 0 | 0 |
| likes | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |

Vector:

```text
cat   = [2, 0, 0, 1, 1, 0, 0, 0]
dog   = [2, 0, 0, 1, 1, 0, 0, 0]
eats  = [0, 1, 1, 0, 0, 2, 0, 0]
likes = [0, 1, 1, 0, 0, 0, 1, 1]
```

cat và dog có vector giống hệt nhau (cosine = 1) vì xuất hiện trong cùng context.

## Bài 2 - Similarity

x = [1, 2, 1], y = [2, 4, 2]

```text
x . y = 1*2 + 2*4 + 1*2 = 12
|x| = sqrt(1 + 4 + 1) = sqrt(6)
|y| = sqrt(4 + 16 + 4) = sqrt(24) = 2*sqrt(6)
cos(x, y) = 12 / (sqrt(6) * 2*sqrt(6)) = 12 / 12 = 1
```

Cosine bằng 1 nghĩa là hai vector cùng hướng (y = 2x). Cosine chỉ đo góc giữa hai vector, không phụ thuộc độ lớn, nên hai vector khác độ dài vẫn có thể giống nhau hoàn toàn về hướng. Với count vector, điều này tương đương việc hai từ có cùng phân phối context, dù một từ xuất hiện nhiều hơn.

## Bài 3 - So sánh semantic similarity

```text
v_doctor    = [0.8, 0.1, 0.7]
v_physician = [0.7, 0.2, 0.8]
v_banana    = [-0.2, 0.9, -0.1]
```

Dự đoán trước khi tính: physician gần doctor hơn banana.

cos(doctor, physician):

```text
doctor . physician = 0.56 + 0.02 + 0.56 = 1.14
|doctor|    = sqrt(0.64 + 0.01 + 0.49) = sqrt(1.14) = 1.0677
|physician| = sqrt(0.49 + 0.04 + 0.64) = sqrt(1.17) = 1.0817
cos = 1.14 / (1.0677 * 1.0817) = 1.14 / 1.1549 = 0.987
```

cos(doctor, banana):

```text
doctor . banana = -0.16 + 0.09 - 0.07 = -0.14
|banana| = sqrt(0.04 + 0.81 + 0.01) = sqrt(0.86) = 0.9274
cos = -0.14 / (1.0677 * 0.9274) = -0.14 / 0.9902 = -0.141
```

physician gần doctor hơn banana (0.987 so với -0.141), đúng với dự đoán.

## Bài 4 - Sparse vs dense

1. Biểu diễn 10,000 chiều với 30 non-zero entries là sparse (30/10,000 = 0.3% khác 0).
2. Biểu diễn 300 chiều với hầu hết thành phần khác 0 là dense.
3. Dense representation nén thông tin context vào không gian ít chiều, nên các từ có context tương tự (kể cả không trùng từ context cụ thể nào) vẫn có vector gần nhau. Với sparse vector, hai từ chỉ giống nhau khi cùng xuất hiện với các context word giống hệt nhau, nên thông tin thưa và ít chồng lấn. Dense vector còn ít chiều hơn nên tiết kiệm bộ nhớ và tính toán hơn.
4. Không. Sparse count vector dễ diễn giải (mỗi chiều là một từ hoặc một feature cụ thể), không cần huấn luyện, và vẫn rất hiệu quả cho các bài toán dựa trên khớp từ như lexical search với TF-IDF. Dense embedding cần đủ dữ liệu để huấn luyện, khó diễn giải từng chiều, và có thể làm mất thông tin chi tiết. Hiệu quả phụ thuộc vào bài toán và dữ liệu.

## Bài tập prediction - CBOW vs Skip-gram

Câu: the cat eats fish, window = 1.

CBOW (context -> target):

| Context | Target |
|---------|--------|
| [cat] | the |
| [the, eats] | cat |
| [cat, fish] | eats |
| [eats] | fish |

Skip-gram (target -> context), mỗi cặp là một training example:

| Target | Context |
|--------|---------|
| the | cat |
| cat | the |
| cat | eats |
| eats | cat |
| eats | fish |
| fish | eats |

CBOW có 4 example (mỗi vị trí một example, input là các context word gộp lại, output là target). Skip-gram có 6 example (mỗi cặp target-context một example, input là target, output là một context word).

CBOW và Skip-gram khác nhau ở input và target: CBOW dùng các context word để dự đoán target word; Skip-gram dùng target word để dự đoán từng context word.

## Bài tập tính analogy

```text
king  = [8, 2, 7]
man   = [5, 1, 5]
woman = [5, 3, 5]

king - man + woman = [8-5+5, 2-1+3, 7-5+5] = [8, 4, 7]
```

king - man = [3, 1, 2] là phần chênh lệch giữa king và man, tức thành phần "hoàng gia/quyền lực" sau khi loại phần "nam giới, người trưởng thành". Cộng thêm woman cho vector [8, 4, 7], tức hoàng gia kết hợp với giới nữ. Vector này đại diện cho quan hệ giới tính trong cặp (king, queen) và gần với vị trí kỳ vọng của queen. Đây là một pattern trong không gian vector (offset man -> woman gần song song với king -> queen), không phải bằng chứng embedding hiểu quan hệ như con người.
