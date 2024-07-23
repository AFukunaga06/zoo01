
..................................................
import customtkinter as ctk
import pyautogui
import pyperclip
import tkinter.messagebox as messagebox
import time

class CopyCoordApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("座標取得アプリ")
        self.geometry("220x150")  # ウィンドウサイズを調整

        self.start_button = ctk.CTkButton(self, text="開始位置", command=self.capture_start, fg_color="#0078D4", corner_radius=10, width=180, height=40)
        self.start_button.pack(pady=10, padx=20)
        
        self.end_button = ctk.CTkButton(self, text="終了位置", command=self.capture_end, state="disabled", fg_color="#0078D4", corner_radius=10, width=180, height=40)
        self.end_button.pack(pady=10, padx=20)

        self.start_pos = None
        self.end_pos = None

    def capture_start(self):
        self.start_pos = self.capture_position("開始位置")
        if self.start_pos:
            self.end_button.configure(state="normal")

    def capture_end(self):
        self.end_pos = self.capture_position("終了位置")
        if self.end_pos:
            self.after(2000, self.perform_drag_and_copy)  # 2秒後にドラッグを開始
            self.show_final_result()

    def capture_position(self, position_type):
        self.withdraw()
        time.sleep(3)  # 3秒待つ
        try:
            x, y = pyautogui.position()
            return (x, y)
        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました: {str(e)}")
            return None
        finally:
            self.deiconify()

    def perform_drag_and_copy(self):
        try:
            pyautogui.moveTo(self.start_pos[0], self.start_pos[1])
            pyautogui.mouseDown()
            pyautogui.moveTo(self.end_pos[0], self.end_pos[1], duration=0.5)
            pyautogui.mouseUp()
            pyautogui.hotkey('ctrl', 'c')
        except Exception as e:
            messagebox.showerror("エラー", f"ドラッグ＆コピー中にエラーが発生しました: {str(e)}")

    def show_final_result(self):
        if self.start_pos and self.end_pos:
            messagebox.showinfo("結果", 
                                f"開始位置: X={self.start_pos[0]}, Y={self.start_pos[1]}\n"
                                f"終了位置: X={self.end_pos[0]}, Y={self.end_pos[1]}\n"
                                "指定された範囲をドラッグしてコピーしました。")
            self.end_button.configure(state="disabled")
            self.start_button.configure(state="normal")
            self.start_pos = None
            self.end_pos = None

if __name__ == '__main__':
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = CopyCoordApp()
    app.mainloop()
