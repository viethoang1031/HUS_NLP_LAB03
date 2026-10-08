# Prediction

## Prediction 1 - Những từ nào gần nhau nhất?

Từ: doctor, physician, hospital, banana, car.

Prediction: doctor và physician gần nhau nhất. Tiếp theo là doctor-hospital. banana và car xa các từ còn lại (và xa nhau).

Reason: doctor và physician là cặp gần nghĩa, thường xuất hiện trong các context y tế giống nhau (patient, treat, medical, clinic). hospital cùng chủ đề nhưng là danh từ chỉ nơi chốn, context chỉ chồng lấn một phần. banana (thực phẩm) và car (phương tiện) có context khác hẳn nhóm y tế.

Confidence: cao với doctor-physician cao nhất và banana xa nhất (khoảng 85%); trung bình với thứ tự giữa hospital và car (khoảng 60%).

## Prediction 2 - Window tăng từ 2 lên 5

Prediction: similarity có thay đổi. Window nhỏ cho quan hệ gần về cú pháp và chức năng (cùng loại từ, thay thế được cho nhau, ví dụ doctor-physician). Window lớn cho quan hệ gần về chủ đề (doctor-hospital, doctor-patient tăng).

Reason: window lớn đưa vào nhiều từ cùng chủ đề trong câu, ít phụ thuộc vị trí; window nhỏ chỉ lấy các từ sát bên nên phản ánh vai trò ngữ pháp.

Confidence: cao rằng có thay đổi (khoảng 90%); trung bình về hướng thay đổi (khoảng 65%).

## Prediction 3 - Dimension tăng 50 -> 100 -> 300

Prediction: không chắc chắn tăng chất lượng. Từ 50 lên 100 có thể cải thiện nhẹ; lên 300 có thể không cải thiện hoặc cải thiện rất ít với corpus này, trong khi thời gian huấn luyện và kích thước model tăng.

Reason: số chiều là capacity của model. Corpus chỉ khoảng 10 triệu token nên dữ liệu có thể không đủ để tận dụng 300 chiều, và có nguy cơ vector học nhiễu. Chất lượng phụ thuộc cả dữ liệu, window và số epoch.

Confidence: trung bình (khoảng 60%).

## Prediction 4 - doctor và physician có chắc chắn gần nhau nếu corpus chỉ có 100 câu?

Prediction: không chắc chắn.

Reason: embedding học từ thống kê context. Với 100 câu, doctor và physician có thể xuất hiện rất ít lần (thậm chí không xuất hiện hoặc không chung context), nên vector gần như phụ thuộc khởi tạo ngẫu nhiên và nhiễu. Hai từ có thể không có context chung dù đồng nghĩa; quan hệ gần nghĩa chỉ được học khi dữ liệu thể hiện đủ các context tương tự.

Confidence: cao (khoảng 85%).

## Đối chiếu sau khi chạy thực nghiệm

Prediction 1: kết quả khớp. doctor-physician có cosine 0.776 (cao nhất trong các cặp liên quan đến doctor), doctor-hospital 0.431, doctor-banana -0.150. car-automobile đạt 0.608 (không dùng car để so với doctor trong thí nghiệm).

Prediction 2: có thay đổi nhưng nhỏ và không theo hướng dự đoán. Từ window 2 đến 5: doctor-physician 0.783 -> 0.776, doctor-hospital 0.457 -> 0.431. Dự đoán rằng quan hệ theo chủ đề tăng khi window lớn là chưa đúng với corpus này.

Prediction 3: đúng. Tăng dimension từ 100 lên 300 không cải thiện rõ (analogy top-1 0.535 và 0.535, Spearman 0.791 và 0.803), trong khi thời gian huấn luyện tăng từ 124s lên 273s.

Prediction 4: đúng về mặt lý luận; trong thí nghiệm, ngay cả với 10 triệu token, doctor và physician chỉ có 3 câu chứa cả hai từ, nên độ gần phụ thuộc vào việc chia sẻ context chứ không phải việc cùng xuất hiện. Với 100 câu thì không đủ dữ liệu để đảm bảo điều đó.
