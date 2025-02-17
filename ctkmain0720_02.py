import customtkinter
from customtkinter import CTk, CTkLabel, CTkButton, CTkTextbox, CTkComboBox, CTkEntry
import pyautogui as p
import os
import subprocess
import tkinter.messagebox as messagebox
import time
import pyperclip
from collections import Counter
import sys
import re


# スクリプトのファイル名を取得
file_name = os.path.basename(sys.argv[0])

def process_clipboard_data(jancode, clipboard_data):
    lines = clipboard_data.split('\n')
    output_data = ""

    for line in lines:
        if line.strip():
            if '\t' in line:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    label, value = parts
                    if label == "商品サイズ" or label == "重量":
                        output_data += f"{label}\t{value}\n"
                    else:
                        output_data += f"{label}\t{value}\n"
                else:
                    output_data += line.strip() + "\n"
            else:
                output_data += line.strip() + "\n"

    if jancode:
        output_data = f"JANコード\t{jancode}\n{output_data}"
    else:
        output_data = output_data.lstrip()

    output_data = output_data.rstrip()

    with open('input.txt', 'a', encoding='utf-8') as file:
        file.write(output_data)
        file.write('\n\n')

    print('新しいデータがinput.txtに追加されました。')

def check_and_count_jan_codes(output):
    try:
        with open('input.txt', 'r', encoding='utf-8') as f:
            data_str = f.read()
        jan_codes = []
        discontinued_codes = []
        jan_code_count = data_str.count('JANコード')
        lines = data_str.split('\n')
        latest_jan_code = ""
        for i in range(len(lines)):
            line = lines[i]
            if "JANコード" in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    jan_code = parts[1]
                    latest_jan_code = jan_code
                    jan_codes.append(jan_code)
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        if "ブランド名" in next_line:
                            next_parts = next_line.split('\t')
                            if len(next_parts) >= 2:
                                brand_name = next_parts[1]
                                if brand_name == "廃番":
                                    discontinued_codes.append(jan_code)
        duplicate_jan_codes = [code for code, count in Counter(jan_codes).items() if count > 1]
        output.delete("1.0", customtkinter.END)
        if duplicate_jan_codes:
            for duplicate in duplicate_jan_codes:
                output.insert(customtkinter.END, f"JANコード {duplicate} が重複しています\n")
        else:
            output.insert(customtkinter.END, "重複はありません\n")
        if discontinued_codes:
            for code in discontinued_codes:
                output.insert(customtkinter.END, f"JANコード {code} は廃番です\n")
        output.insert(customtkinter.END, f"JANコードは上から{jan_code_count}番目です\n")
        if latest_jan_code:
            output.insert(customtkinter.END, f"現在のJANコードは{latest_jan_code}です\n")
    except FileNotFoundError:
        output.delete("1.0", customtkinter.END)
        output.insert(customtkinter.END, "input.txtファイルが見つかりません。\n")
    except Exception as e:
        output.delete("1.0", customtkinter.END)
        output.insert(customtkinter.END, f"エラーが発生しました： {str(e)}\n")

def click_two_positions(z, c, de, xd, skip_first_clicks=False):
    x = -120
    y = 150
    x1 = -1003
    y1 = 604

    if not skip_first_clicks:
        x += xd
        c = 0
        z = -50
        p.click(x, y + de, duration=0.3)
        p.sleep(2)
        p.click(x1, y1 + de, duration=0.2)
        p.sleep(2)

    adjusted_xa = x + 890
    adjusted_ya = y + 264 + c
    adjusted_xb = x + 505
    adjusted_yb = y + 480 + z

    p.moveTo(adjusted_xa, adjusted_ya)
    p.mouseDown()
    p.moveTo(adjusted_xb, adjusted_yb, duration=0.8)
    p.mouseUp()
    p.hotkey('ctrl', 'c')
    p.moveTo(550, 360)
    time.sleep(0.5)

    clipboard_data = pyperclip.paste()
    if not clipboard_data:
        messagebox.showwarning("警告", "値がありません")
        return None

    return clipboard_data

def paste_and_execute():
    clipboard_data = pyperclip.paste()
    if clipboard_data is None:
        messagebox.showwarning("警告", "クリップボードにデータがありません。")
        return

    process_clipboard_data("", clipboard_data)
    # ウィンドウを閉じずに出力にデータを追加
    window.output.insert(customtkinter.END, clipboard_data + "\n")
  
def open_checksheet10():
    try:
        os.startfile(r'c:\test\checksheet10.bat')
    except FileNotFoundError:
        messagebox.showwarning("ファイルが見つかりません", "checksheet10.batファイルが見つかりません。")
    except Exception as e:
        messagebox.showerror("エラー", f"ファイルを開く際にエラーが発生しました： {str(e)}")

def open_input_file():
    file_path = 'input.txt'
    if os.path.exists(file_path):
        try:
            os.startfile(file_path)
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルを開く際にエラーが発生しました： {str(e)}")
    else:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('')
        try:
            os.startfile(file_path)
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルを開く際にエラーが発生しました： {str(e)}")

def open_syouhin_n():
    try:
        os.startfile('syouhin_n.bat')
    except FileNotFoundError:
        messagebox.showwarning("ファイルが見つかりません", "syouhin_n.batファイルが見つかりません。")
    except Exception as e:
        messagebox.showerror("エラー", f"ファイルを開く際にエラーが発生しました： {str(e)}")

def execute_type1_and_open_output01():
    try:
        subprocess.run(["Type1.bat"])
        time.sleep(1)
        os.startfile('output01.txt')
    except FileNotFoundError as e:
        if 'Type1.bat' in str(e):
            messagebox.showwarning("ファイルが見つかりません", "Type1.batファイルが見つかりません。")
        elif 'output01.txt' in str(e):
            with open('output01.txt', 'w', encoding='utf-8') as file:
                file.write('')
            os.startfile('output01.txt')
    except Exception as e:
        messagebox.showerror("エラー", f"ファイルの実行または開く際にエラーが発生しました： {str(e)}")

def execute_type2_and_open_output():
    try:
        subprocess.run(["Type2.bat"])
        time.sleep(1)
        os.startfile('output.txt')
    except FileNotFoundError as e:
        if 'Type2.bat' in str(e):
            messagebox.showwarning("ファイルが見つかりません", "Type2.batファイルが見つかりません。")
        elif 'output.txt' in str(e):
            with open('output.txt', 'w', encoding='utf-8') as file:
                file.write('')
            os.startfile('output.txt')
    except Exception as e:
        messagebox.showerror("エラー", f"ファイルの実行または開く際にエラーが発生しました： {str(e)}")

def open_fujiwarasanngyou():
    try:
        os.startfile('fujiwarasanngyou.bat')
    except FileNotFoundError:
        messagebox.showwarning("ファイルが見つかりません", "fujiwarasanngyou.batファイルが見つかりません。")
    except Exception as e:
        messagebox.showerror("エラー", f"ファイルを開く際にエラーが発生しました： {str(e)}")

def clear_files():
    confirm = messagebox.askyesno("確認", "本当にクリアして良いですか？")
    if confirm:
        try:
            files = ["check01.txt", "output01.txt", "output02.txt", "output.txt", "input.txt"]
            for file in files:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write('')
            messagebox.showinfo("クリア完了", "ファイルのデータをクリアしました。")
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルをクリアする際にエラーが発生しました： {str(e)}")

def confirm_jancode(output):
    jancode = window.jancode_entry.get()
    if len(jancode) == 13:
        with open('input.txt', 'a', encoding='utf-8') as file:
            file.write(f"JANコード\t{jancode}\nブランド名\t廃番\n\n")
        messagebox.showinfo("JANコード確定", "JANコードが正常に登録されました。")
        output.insert(customtkinter.END, f"JANコード\t{jancode}\nブランド名\t廃番\n\n")
        window.jancode_entry.delete(0, customtkinter.END)
        pyperclip.copy("")
    else:
        messagebox.showerror("JANコードエラー", "JANコードは13桁の数字を入力してください。")

class AdjustmentSubForm(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("x軸とy軸の調整")
        self.geometry("400x300")
        
        self.label_xd = customtkinter.CTkLabel(self, text="xd（整数）")
        self.label_xd.pack(padx=10, pady=5)

        self.xd_entry = customtkinter.CTkEntry(self, width=200)
        self.xd_entry.pack(padx=10, pady=5)

        self.label_yc = customtkinter.CTkLabel(self, text="y軸の調整左上(c)")
        self.label_yc.pack(padx=10, pady=5)

        self.yc_combobox = customtkinter.CTkComboBox(self, values=[str(i) for i in range(-100, 101, 5)], width=200)
        self.yc_combobox.pack(padx=10, pady=5)

        self.label_yb = customtkinter.CTkLabel(self, text="y軸の調整右下(z)")
        self.label_yb.pack(padx=10, pady=5)

        self.yb_combobox = customtkinter.CTkComboBox(self, values=[str(i) for i in range(-100, 101, 5)], width=200)
        self.yb_combobox.pack(padx=10, pady=5)
        
        self.label_yde = customtkinter.CTkLabel(self, text="y軸の調整始めと2度目(de)")
        self.label_yde.pack(padx=10, pady=5)

        self.yde_combobox = customtkinter.CTkComboBox(self, values=[str(i) for i in range(-100, 101, 5)], width=200)
        self.yde_combobox.pack(padx=10, pady=5)

        self.adjust_button = customtkinter.CTkButton(self, text="座標調整を実行", command=self.adjust_coordinates)
        self.adjust_button.pack(padx=10, pady=10)

    def adjust_coordinates(self):
        try:
            xd = int(self.xd_entry.get())
            yc = int(self.yc_combobox.get())
            yb = int(self.yb_combobox.get())
            yde = int(self.yde_combobox.get())
            messagebox.showinfo("調整結果", f"調整完了：xd={xd}, yc={yc}, yb={yb}, yde={yde}")
        except ValueError:
            messagebox.showerror("入力エラー", "すべての値を整数として正しく入力してください。")

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.title("Application - " + file_name)
        self.geometry("800x600")
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(fill=customtkinter.BOTH, expand=True, padx=20, pady=20)

        self.output = CTkTextbox(self.frame, width=760, height=100)
        self.output.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        self.check_button = CTkButton(self.frame, text="重複と項目抜けのチェック", command=lambda: check_and_count_jan_codes(self.output), fg_color="#0078D4")
        self.check_button.grid(row=1, column=0, padx=5, pady=2, sticky="ew")

        self.yc_label = CTkLabel(self.frame, text="y軸の調整左上(c)")
        self.yc_label.grid(row=2, column=0, padx=5, pady=2, sticky="ew")

        self.yc_combobox = CTkComboBox(self.frame, values=[str(i) for i in range(-100, 101, 5)], width=100, command=self.update_c_selection)
        self.yc_combobox.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        self.yb_label = CTkLabel(self.frame, text="y軸の調整右下(z)")
        self.yb_label.grid(row=2, column=2, padx=5, pady=2, sticky="ew")

        self.yb_combobox = CTkComboBox(self.frame, values=[str(i) for i in range(-100, 101, 5)], width=100, command=self.update_z_selection)
        self.yb_combobox.set("-55")
        self.yb_combobox.grid(row=2, column=3, padx=5, pady=2, sticky="ew")

        self.yde_label = CTkLabel(self.frame, text="y軸の調整始めと2度目(de)")
        self.yde_label.grid(row=3, column=0, padx=5, pady=2, sticky="ew")

        self.yde_combobox = CTkComboBox(self.frame, values=[str(i) for i in range(-100, 101, 5)], width=100, command=self.update_de_selection)
        self.yde_combobox.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        self.de_note_label = CTkLabel(self.frame, text="※deの値の調整で始めのクリックを決める")
        self.de_note_label.grid(row=4, column=0, columnspan=4, padx=5, pady=2, sticky="ew")

        self.xd_label = CTkLabel(self.frame, text="x軸の調整(xd)")
        self.xd_label.grid(row=5, column=0, padx=5, pady=2, sticky="ew")

        self.xd_combobox = CTkComboBox(self.frame, values=[str(i) for i in range(-100, 101, 5)], width=100, command=self.update_xd_selection)
        self.xd_combobox.grid(row=5, column=1, padx=5, pady=2, sticky="ew")

        self.adjust_button = CTkButton(self.frame, text="座標調整", command=self.adjust_coordinates, fg_color="#0078D4")
        self.adjust_button.grid(row=5, column=2, padx=5, pady=2, sticky="ew")

        self.drag_and_copy_button = CTkButton(self.frame, text="ドラッグとコピー", command=self.drag_and_copy, fg_color="#0078D4")
        self.drag_and_copy_button.grid(row=6, column=0, padx=5, pady=2, sticky="ew")

        self.paste_button = CTkButton(self.frame, text="2.テキストに貼り付けと実行", command=paste_and_execute, fg_color="#0078D4")
        self.paste_button.grid(row=6, column=1, padx=5, pady=2, sticky="ew")

        self.open_input_button = CTkButton(self.frame, text="3.input.txtを開く", command=open_input_file, fg_color="#0078D4")
        self.open_input_button.grid(row=6, column=2, padx=5, pady=2, sticky="ew")

        self.open_checksheet10_button = CTkButton(self.frame, text="チェックシートを開く", command=open_checksheet10, fg_color="#0078D4")
        self.open_checksheet10_button.grid(row=7, column=0, padx=5, pady=2, sticky="ew")

        self.open_syouhin_n_button = CTkButton(self.frame, text="商品情報入力シートを開く", command=open_syouhin_n, fg_color="#0078D4")
        self.open_syouhin_n_button.grid(row=7, column=1, padx=5, pady=2, sticky="ew")

        self.open_fujiwarasanngyou_button = CTkButton(self.frame, text="藤原産業を開く", command=open_fujiwarasanngyou, fg_color="#0078D4")
        self.open_fujiwarasanngyou_button.grid(row=7, column=2, padx=5, pady=2, sticky="ew")

        self.execute_type1_and_output01_button = CTkButton(self.frame, text="Type1.bat実行とoutput01.txt表示", command=execute_type1_and_open_output01, fg_color="#0078D4")
        self.execute_type1_and_output01_button.grid(row=8, column=0, padx=5, pady=2, sticky="ew")

        self.execute_type2_and_output_button = CTkButton(self.frame, text="Type2.bat実行とoutput.txt表示", command=execute_type2_and_open_output, fg_color="#0078D4")
        self.execute_type2_and_output_button.grid(row=8, column=1, padx=5, pady=2, sticky="ew")

        self.subform_button = CTkButton(self.frame, text="サブフォーム廃番処理", command=self.open_subform, fg_color="#0078D4")
        self.subform_button.grid(row=8, column=2, padx=5, pady=2, sticky="ew")

        self.clear_files_button = CTkButton(self.frame, text="クリップボードのクリア", command=self.clear_files, fg_color="#0078D4")
        self.clear_files_button.grid(row=9, column=0, padx=5, pady=2, sticky="ew")

        self.jancode_copy_button = CTkButton(self.frame, text="JANコードコピーとチェック", command=self.jancode_copy, fg_color="#0078D4")
        self.jancode_copy_button.grid(row=9, column=1, padx=5, pady=2, sticky="ew")

        self.check_input_button = CTkButton(self.frame, text="input.txtのチェック", command=self.check_input_file, fg_color="#0078D4")
        self.check_input_button.grid(row=9, column=2, padx=5, pady=2, sticky="ew")

        self.coordinate_copy_button = CTkButton(self.frame, text="座標軸とコピー", command=self.open_coordinate_subform, fg_color="#0078D4")
        self.coordinate_copy_button.grid(row=10, column=0, padx=5, pady=2, sticky="ew")

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)

        self.z = 0
        self.c = 0
        self.de = 0
        self.xd = 0

        self.clipboard_disable_var = customtkinter.StringVar(value="No")

    def update_selection(self, value):
        self.z = int(value)
        self.click_and_select(skip_first_clicks=True)

    def update_c_selection(self, value):
        self.c = int(value)
        self.click_and_select(skip_first_clicks=True)
        
    def update_z_selection(self, value):
        self.z = int(value)
        self.click_and_select(skip_first_clicks=True)

    def update_de_selection(self, value):
        self.de = int(value)
        self.click_and_select(skip_first_clicks=True)

    def update_xd_selection(self, value):
        self.xd = int(value)
        self.click_and_select(skip_first_clicks=True)

    def click_and_select(self, skip_first_clicks=False):
        clipboard_data = click_two_positions(self.z, self.c, self.de, self.xd, skip_first_clicks=skip_first_clicks)
        if clipboard_data is not None:
            self.output.insert(customtkinter.END, clipboard_data + "\n")

    def adjust_coordinates(self):
        self.click_and_select(skip_first_clicks=True)

    def drag_and_copy(self):
        clipboard_data = click_two_positions(self.z, self.c, self.de, self.xd)
        if clipboard_data is not None:
            self.output.insert(customtkinter.END, clipboard_data + "\n")
            process_clipboard_data("", clipboard_data)

    def jancode_copy(self):
        try:
            subprocess.Popen(['python', 'jancopy0708_01.py'])
        except FileNotFoundError:
            messagebox.showwarning("ファイルが見つかりません", "jancopy0708_01.pyファイルが見つかりません。")
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルを実行する際にエラーが発生しました： {str(e)}")

    def open_subform(self):
        try:
            subprocess.Popen(['python', 'ckt0412sab01.py'])
        except FileNotFoundError:
            messagebox.showwarning("ファイルが見つかりません", "ckt0412sab01.pyファイルが見つかりません。")
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルを実行する際にエラーが発生しました： {str(e)}")

    def open_coordinate_subform(self):
        try:
            subprocess.Popen(['python', 'Copycoord0720_05.py'])
        except FileNotFoundError:
            messagebox.showwarning("ファイルが見つかりません", "Copycoord0720_05.pyファイルが見つかりません。")
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルを実行する際にエラーが発生しました： {str(e)}")

    def clear_files(self):
        confirm = messagebox.askyesno("確認", "本当にクリアして良いですか？")
        if confirm:
            try:
                files = ["check01.txt", "output01.txt", "output02.txt", "output.txt", "input.txt"]
                for file in files:
                    with open(file, 'w', encoding='utf-8') as f:
                        f.write('')
                messagebox.showinfo("クリア完了", "ファイルのデータをクリアしました。")
            except Exception as e:
                messagebox.showerror("エラー", f"ファイルをクリアする際にエラーが発生しました： {str(e)}")

    def check_input_file(self):
        try:
            with open('input.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()

            invalid_an_code_lines = []
            thirteen_digit_lines = []

            for i, line in enumerate(lines, 1):
                if 'ANコード' in line:
                    if 'JANコード' not in line:
                        invalid_an_code_lines.append(i)
                if re.match(r'^\d{13}$', line.strip()):
                    thirteen_digit_lines.append(i)

            message = ""
            if invalid_an_code_lines:
                message += f"「ANコード」に「J」が含まれていない行: {', '.join(map(str, invalid_an_code_lines))}\n"
            else:
                message += "全ての「ANコード」に「J」が含まれています。\n"

            if thirteen_digit_lines:
                message += f"13桁の数値のみを含む行: {', '.join(map(str, thirteen_digit_lines))}\n"
            else:
                message += "13桁の数値のみを含む行はありません。\n"

            messagebox.showinfo("チェック結果", message)

        except FileNotFoundError:
            messagebox.showerror("エラー", "input.txtファイルが見つかりません。")
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルのチェック中にエラーが発生しました： {str(e)}")

class CoordinateSubForm(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("座標取得アプリ")
        self.geometry("300x200")
        
        self.start_button = customtkinter.CTkButton(self, text="開始位置", command=self.capture_start)
        self.start_button.pack(pady=20)
        
        self.end_button = customtkinter.CTkButton(self, text="終了位置", command=self.capture_end, state="disabled")
        self.end_button.pack(pady=20)
        
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

    def capture_position(self, position_type):
        self.withdraw()
        time.sleep(3)  # 3秒待つ
        try:
            x, y = p.position()
            return (x, y)
        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました: {str(e)}")
            return None
        finally:
            self.deiconify()

    def perform_drag_and_copy(self):
        try:
            p.moveTo(self.start_pos[0], self.start_pos[1])
            p.mouseDown()
            p.moveTo(self.end_pos[0], self.end_pos[1], duration=0.5)
            p.mouseUp()
            p.hotkey('ctrl', 'c')
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
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    window = MainWindow()
    window.mainloop()
