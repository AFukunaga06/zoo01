import customtkinter as ctk
import pyautogui
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import time

class CopyCoordApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("座標取得アプリ")
        self.geometry("300x250")
        
        self.start_button = ctk.CTkButton(self, text="開始位置", command=self.capture_start)
        self.start_button.pack(pady=10)
        
        self.end_button = ctk.CTkButton(self, text="終了位置", command=self.capture_end, state="disabled")
        self.end_button.pack(pady=10)
        
        self.copy_button = ctk.CTkButton(self, text="同じ座標軸のコピー", command=self.copy_coordinates, state="disabled", fg_color="blue")
        self.copy_button.pack(pady=10)
        
        self.start_pos = None
        self.end_pos = None

    def capture_start(self):
        self.start_pos = self.capture_position("開始位置")
        if self.start_pos:
            self.end_button.configure(state="normal")

    def capture_end(self):
        self.end_pos = self.capture_position("終了位置")
        if self.end_pos:
            self.perform_drag_and_copy()
            self.show_final_result()
            self.copy_button.configure(state="normal")

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

    def copy_coordinates(self):
        start_x = simpledialog.askinteger("開始位置X", "開始位置のX座標を入力してください")
        start_y = simpledialog.askinteger("開始位置Y", "開始位置のY座標を入力してください")
        end_x = simpledialog.askinteger("終了位置X", "終了位置のX座標を入力してください")
        end_y = simpledialog.askinteger("終了位置Y", "終了位置のY座標を入力してください")

        if None not in (start_x, start_y, end_x, end_y):
            self.start_pos = (start_x, start_y)
            self.end_pos = (end_x, end_y)
            self.perform_drag_and_copy()
            messagebox.showinfo("コピー完了", "同じ座標軸をコピーしました。")
        else:
            messagebox.showerror("エラー", "コピーする座標が無効です。")

if __name__ == '__main__':
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = CopyCoordApp()
    app.mainloop()
