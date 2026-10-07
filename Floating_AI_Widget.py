import customtkinter as ctk
import requests
import json
import threading
import os
import webbrowser
from gtts import gTTS
import pygame

# Khởi tạo âm thanh
pygame.mixer.init()

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class FloatingAIWidget(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MMA AI - Nổi")
        self.geometry("380x750")
        self.attributes("-topmost", True) # LUÔN NỔI TRÊN CÙNG
        
        # ============ UI LAYOUT ============
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=10)
        
        self.title_lbl = ctk.CTkLabel(self.header_frame, text="🤖 MMA - Trợ Lý AI", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1a73e8")
        self.title_lbl.pack()
        
        self.credit_lbl = ctk.CTkLabel(self.header_frame, text="Design by ThayHauAI.com", font=ctk.CTkFont(size=12, underline=True), text_color="#1a73e8", cursor="hand2")
        self.credit_lbl.pack()
        self.credit_lbl.bind("<Button-1>", lambda e: webbrowser.open("https://www.ThayHauAI.com"))

        # API Key
        self.api_entry = ctk.CTkEntry(self, placeholder_text="Nhập DeepSeek API Key (sk-...)", show="*")
        self.api_entry.pack(padx=15, pady=(0, 10), fill="x")
        
        # Ngôn ngữ
        self.lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lang_frame.pack(padx=15, pady=5, fill="x")
        
        self.src_lang = ctk.CTkOptionMenu(self.lang_frame, values=["Tiếng Anh", "Tiếng Việt", "Tiếng Nhật", "Tiếng Trung"], width=140)
        self.src_lang.pack(side="left", padx=(0, 5))
        
        self.tgt_lang = ctk.CTkOptionMenu(self.lang_frame, values=["Tiếng Việt", "Tiếng Anh", "Tiếng Nhật", "Tiếng Trung"], width=140)
        self.tgt_lang.pack(side="right", padx=(5, 0))

        # Đầu vào
        self.input_lbl = ctk.CTkLabel(self, text="📄 Nội dung cần xử lý (Copy & Paste):", font=ctk.CTkFont(size=12, weight="bold"))
        self.input_lbl.pack(padx=15, anchor="w")
        
        self.input_text = ctk.CTkTextbox(self, height=120)
        self.input_text.pack(padx=15, fill="x")
        
        self.btn_speak_in = ctk.CTkButton(self, text="🔊 Đọc văn bản gốc", fg_color="#9c27b0", hover_color="#7b1fa2", width=120, height=28, command=lambda: self.speak_text(self.input_text.get("1.0", "end-1c"), self.src_lang.get(), self.btn_speak_in))
        self.btn_speak_in.pack(padx=15, pady=4, anchor="e")

        # Nút chức năng
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(padx=15, pady=5, fill="x")
        
        self.btn_trans = ctk.CTkButton(self.btn_frame, text="🌐 Dịch", command=lambda: self.process_ai("translate"))
        self.btn_trans.pack(side="left", expand=True, padx=2)
        
        self.btn_expl = ctk.CTkButton(self.btn_frame, text="💡 Giải thích", fg_color="#188038", hover_color="#13602a", command=lambda: self.process_ai("explain"))
        self.btn_expl.pack(side="left", expand=True, padx=2)
        
        self.btn_sum = ctk.CTkButton(self.btn_frame, text="📋 Tóm tắt", fg_color="#f29900", hover_color="#c97f00", command=lambda: self.process_ai("summarize"))
        self.btn_sum.pack(side="left", expand=True, padx=2)
        
        # Loader
        self.loader_lbl = ctk.CTkLabel(self, text="", text_color="#1a73e8", font=ctk.CTkFont(weight="bold"))
        self.loader_lbl.pack(pady=2)

        # Đầu ra
        self.output_lbl = ctk.CTkLabel(self, text="✨ Kết quả từ AI:", font=ctk.CTkFont(size=12, weight="bold"))
        self.output_lbl.pack(padx=15, anchor="w")
        
        self.output_text = ctk.CTkTextbox(self, height=180)
        self.output_text.pack(padx=15, fill="x")
        
        self.btn_speak_out = ctk.CTkButton(self, text="🔊 Đọc kết quả", fg_color="#9c27b0", hover_color="#7b1fa2", width=120, height=28, command=lambda: self.speak_text(self.output_text.get("1.0", "end-1c"), self.tgt_lang.get(), self.btn_speak_out))
        self.btn_speak_out.pack(padx=15, pady=4, anchor="e")
        
        # Hướng dẫn
        self.hint = ctk.CTkLabel(self, text="* Cửa sổ này luôn nổi trên cùng khi thuyết trình full màn hình", font=ctk.CTkFont(size=10, slant="italic"), text_color="gray")
        self.hint.pack(pady=5)
        
        # Load API key saved previously if possible (basic load)
        if os.path.exists("api_key.txt"):
            with open("api_key.txt", "r") as f:
                self.api_entry.insert(0, f.read().strip())

    def process_ai(self, action):
        api_key = self.api_entry.get().strip()
        if not api_key:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", "❌ Lỗi: Bạn chưa nhập API Key!")
            return
            
        with open("api_key.txt", "w") as f:
            f.write(api_key)

        text = self.input_text.get("1.0", "end-1c").strip()
        if not text:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", "❌ Lỗi: Bạn chưa dán nội dung cần xử lý!")
            return

        target_lang = self.tgt_lang.get()
        
        if action == "translate":
            prompt = f"Hãy dịch nội dung sau sang {target_lang} tự nhiên, dễ hiểu nhất:\n\n{text}"
        elif action == "explain":
            prompt = f"Hãy giải thích chi tiết, rõ ràng khái niệm trong nội dung sau bằng {target_lang}:\n\n{text}"
        elif action == "summarize":
            prompt = f"Hãy tóm tắt ngắn gọn ý chính của nội dung sau bằng {target_lang}:\n\n{text}"
            
        self.loader_lbl.configure(text="⏳ AI đang phân tích...")
        self.output_text.delete("1.0", "end")
        
        # Run in thread so UI doesn't freeze
        threading.Thread(target=self.call_api, args=(prompt, api_key)).start()

    def call_api(self, prompt, api_key):
        url = "https://api.deepseek.com/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a friendly and enthusiastic assistant. Do NOT use any markdown formatting like asterisks (**) or hashes (#). Use plain text only. Use lively emojis to make the response engaging. Write naturally as if talking to a friend."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()
            if "error" in data:
                result = "❌ Lỗi API: " + data["error"]["message"]
            else:
                result = data["choices"][0]["message"]["content"]
        except Exception as e:
            result = "❌ Lỗi kết nối: " + str(e)
            
        # Update UI in main thread
        self.after(0, lambda: self.loader_lbl.configure(text=""))
        self.after(0, lambda: self.output_text.insert("1.0", result))

    def speak_text(self, text, lang_name, btn_obj):
        if not text.strip():
            return
            
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            btn_obj.configure(text="🔊 Đọc văn bản" if "gốc" in btn_obj.cget("text") else "🔊 Đọc kết quả")
            return
            
        btn_obj.configure(text="⏸ Dừng đọc")
        self.loader_lbl.configure(text="⏳ Đang tạo giọng chuẩn Google TTS...")
        threading.Thread(target=self._generate_and_play, args=(text, lang_name, btn_obj)).start()

    def _generate_and_play(self, text, lang_name, btn_obj):
        # Map lang name to gTTS code
        lang_map = {
            "Tiếng Việt": "vi",
            "Tiếng Anh": "en",
            "Tiếng Nhật": "ja",
            "Tiếng Trung": "zh-CN"
        }
        lang_code = lang_map.get(lang_name, "vi")
        
        try:
            # gTTS generates a highly natural Google TTS mp3
            tts = gTTS(text=text, lang=lang_code, slow=False)
            filename = "temp_speech.mp3"
            tts.save(filename)
            
            self.after(0, lambda: self.loader_lbl.configure(text=""))
            
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Watchdog to reset button text when finished playing
            def check_play():
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                # finished
                try:
                    default_txt = "🔊 Đọc văn bản gốc" if "gốc" in btn_obj.cget("text").lower() else "🔊 Đọc kết quả"
                    self.after(0, lambda: btn_obj.configure(text=default_txt))
                except:
                    pass
            threading.Thread(target=check_play).start()
            
        except Exception as e:
            self.after(0, lambda: self.loader_lbl.configure(text="❌ Lỗi tạo giọng đọc: Cần có mạng Internet"))
            try:
                default_txt = "🔊 Đọc văn bản gốc" if "gốc" in btn_obj.cget("text").lower() else "🔊 Đọc kết quả"
                self.after(0, lambda: btn_obj.configure(text=default_txt))
            except:
                pass

if __name__ == "__main__":
    app = FloatingAIWidget()
    app.mainloop()
