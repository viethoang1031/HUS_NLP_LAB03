# Error Analysis

Model: Word2Vec CBOW, vector_size = 100, window = 5, min_count = 5, epochs = 10, trên C4 30K documents. Số liệu lấy từ word_embedding.ipynb (mục Error analysis).

## Ba similarity đúng

### 1. doctor - physician

Observed: cosine 0.776, physician đứng hạng 2 trong các từ gần doctor nhất.

Expected: cao, vì là hai từ đồng nghĩa.

Possible explanation: hai từ có context tương tự (distributional hypothesis).

Evidence from corpus: từ đứng ngay trước doctor là your (163), a (143), the (139); trước physician là a (45), the (41), your (35). Từ đứng ngay sau cả hai thường là and, who, or. Chỉ 3 câu chứa cả hai từ nên độ gần không đến từ việc cùng xuất hiện trong một câu mà từ việc cùng context.

### 2. doctor - dentist

Observed: cosine 0.823, hạng 1.

Expected: cao (cùng nhóm nghề y tế).

Possible explanation: dentist có cùng vai trò (người cung cấp dịch vụ chăm sóc sức khỏe) và thường đi sau "your", "the", "a" giống doctor.

Evidence from corpus: trước dentist là your (49), the (46), a (29); sau dentist là to (17), will (15), and (10). Có 6 câu chứa cả doctor và dentist, ví dụ "talk with your doctor and dentist before the visit".

### 3. doctor - nurse

Observed: cosine 0.602, hạng 10.

Expected: cao.

Possible explanation: nurse thuộc cùng lĩnh vực và thường đi cùng doctor.

Evidence from corpus: 11 câu chứa cả hai từ, 10 câu trong đó hai từ nằm trong window 5, ví dụ "met with doctor nurse coordinator" và "with doctor and nurse visits".

## Ba similarity sai hoặc bất ngờ

### 1. doctor - hospital

Observed: cosine 0.431, hạng 111.

Expected: cao hơn, vì hospital gắn rất chặt với doctor về chủ đề.

Possible explanation: Word2Vec ưu tiên các từ thay thế được cho nhau trong cùng context. doctor là người, hospital là địa điểm nên context khác nhau về vai trò; hospital gần clinic, icu, hospitals hơn là doctor. Nguyên nhân nằm ở bản chất của objective (similarity về vai trò trong câu), không hẳn là lỗi dữ liệu.

Evidence from corpus: 14 câu chứa cả hai từ, chỉ 7 câu trong window 5, ví dụ "the results were sent to the hospital s lab which then sent them to my primary care doctor". Top-5 của hospital là clinic, icu, hospitals, clinics, rehab, không có doctor.

### 2. doctor - disease

Observed: cosine 0.356, hạng 322.

Expected: trung bình đến cao (cùng chủ đề y tế).

Possible explanation: quan hệ chủ đề (topical) yếu hơn quan hệ cùng vai trò. disease thuộc nhóm bệnh (diseases, infection, chronic, obesity), khác nhóm với doctor. Window 5 và corpus web đa chủ đề cũng làm disease xuất hiện nhiều trong ngữ cảnh khác (tên bệnh, tổ chức, tin tức sức khỏe).

Evidence from corpus: chỉ 7 câu chứa cả doctor và disease, 3 câu trong window 5, ví dụ "follow your doctor instructions or the recommendations of the centers for disease control and prevention cdc" (disease nằm trong tên tổ chức).

### 3. doctor - child

Observed: cosine 0.590, hạng 14, cao hơn nhiều từ liên quan hơn về nghĩa như hospital và disease.

Expected: thấp.

Possible explanation: child là từ rất phổ biến (2,141 lần) và thường đứng ở vị trí giống doctor trong cấu trúc "your doctor", "your child", "the doctor", "the child". Embedding nắm bắt vai trò cú pháp chung (danh từ chỉ người sau your/the). Nguyên nhân thêm: tần suất cao, noisy data từ web (các câu về sức khỏe trẻ em).

Evidence from corpus: chỉ 2 trong 9 câu chứa cả hai từ nằm trong window 5, ví dụ "if your child is less than year then this is where discussions need to take place between you and your doctor". Hai từ không chia sẻ nghĩa nhưng chia sẻ cấu trúc context.

## Tổng kết nguyên nhân

Các nguyên nhân chính trong các trường hợp trên là: bản chất objective (similarity theo vai trò context thay vì theo chủ đề), tần suất từ, domain bias và noisy data của corpus web, và corpus còn nhỏ (doctor chỉ xuất hiện 814 lần, nhiều cặp chỉ có vài câu đồng xuất hiện).
