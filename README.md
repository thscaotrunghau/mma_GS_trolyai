# 🤖 MMA - Trợ Lý AI GS (Google Slides AI Assistant)

Một tiện ích mở rộng siêu mạnh mẽ dành cho Google Slides và PowerPoint, giúp bạn tự động hoá việc dịch thuật, giải thích và thuyết trình bằng Trí tuệ Nhân tạo (DeepSeek AI). 

Tự hào được thiết kế bởi **[ThayHauAI.com](https://www.thayhauai.com)**.

---

## 🌟 Các Tính Năng Đỉnh Cao

1. **🌐 Dịch thuật & Giải thích Đa ngôn ngữ:** Tích hợp AI DeepSeek để dịch chuẩn xác các thuật ngữ chuyên ngành (Anh, Việt, Nhật, Trung).
2. **🗣️ Đọc Giọng Tự Nhiên (TTS):** Xoá bỏ hoàn toàn giọng Robot với công nghệ AI Text-to-Speech mượt mà. Kèm chức năng điều chỉnh tốc độ đọc (0.6x - 1.3x).
3. **👯‍♂️ Highlight Karaoke Kép (Dual-Highlighting):** Chữ đang đọc đến đâu sẽ được bôi vàng nổi bật đến đó. Đặc biệt, hệ thống tự động ánh xạ tỷ lệ phần trăm (Proportional Alignment) để bôi vàng song song cả bản gốc và bản dịch cùng một lúc!
4. **🚀 Auto Presenter (Tự Động Thuyết Trình):** Chỉ với 1 Click, AI sẽ tự động đọc, tự động dịch và tự động lật trang Google Slides của bạn từ đầu đến cuối một cách chuyên nghiệp.
5. **🔥 Ứng dụng Desktop Nổi (Floating Widget):** Đi kèm một phần mềm Python nhỏ gọn luôn "Nổi trên cùng". Giúp bạn có thể xài Trợ lý ngay cả khi đang trình chiếu Full Screen bằng PowerPoint hay Google Slides.

---

## 🛠️ Hướng dẫn cài đặt

### Dành cho Google Slides (Add-on)
1. Mở bất kỳ file Google Slides nào của bạn.
2. Trên thanh menu, chọn **Tiện ích mở rộng** (Extensions) > **Apps Script**.
3. Copy toàn bộ nội dung của file `Code.js` dán đè vào file `Code.gs` trên màn hình.
4. Bấm dấu `+` tạo thêm file HTML mới, đặt tên là `Sidebar.html`.
5. Copy toàn bộ nội dung file `Sidebar.html` trong repo này dán vào đó.
6. Bấm Lưu (Save). Quay lại Google Slides và tải lại trang (F5).
7. Menu **MMA - Trợ Lý AI GS** sẽ xuất hiện!

### Dành cho Ứng dụng Windows (Floating Widget)
Yêu cầu: Máy tính đã cài đặt Python.
1. Mở Terminal / Command Prompt.
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install customtkinter requests gTTS pygame
   ```
3. Chạy ứng dụng:
   ```bash
   python Floating_AI_Widget.py
   ```

---

## 🔑 Cấu hình
Bạn cần có mã API Key của **DeepSeek** (bắt đầu bằng `sk-...`) để Trợ lý có thể hoạt động. Nhập mã này vào ô API Key trong giao diện, mã sẽ tự động được lưu lại cho các lần sử dụng sau.

*Chúc các bạn có những buổi thuyết trình thật sự thăng hoa cùng MMA AI!* 🚀
