import numpy as np
import matplotlib.pyplot as plt
import customtkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CTkTable import *
import i18n
import sys
import os

# 率、ダメ
CRIT = np.array([54, 62, 70, 78])
# 攻撃
ATK = np.array([41, 47, 53, 58])
# スコア確率
NUMS = np.array([41, 47, 53, 58, 54, 62, 70, 78, 54, 62, 70, 78, 0, 0, 0, 0])
# 初期オプ数
OPTION = 4
# 初期オプに含まれているか
IS_CRIT_DMG = True
IS_CRIT_RATE = True
IS_ATK = True
# 初期スコア
INIT_SCORE = 0
# 調査スコア
SCORE = 0
# 強化回数
COUNT = 5
# GUIフォント
FONT_TYPE = "meiryo"
# 言語
LANGUAGE = "en"

class AppLanguage(tk.CTk):

    def __init__(self):
        super().__init__()

        # メンバー変数の設定
        self.fonts = (FONT_TYPE, 15)
        # フォームサイズ設定
        self.geometry("350x200")
        self.title("Basic GUI")

        # フォームのセットアップをする
        self.setup_form()
    
    def setup_form(self):
        # tk のフォームデザイン設定
        tk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # フォームサイズ設定
        self.geometry("600x400")
        self.title("Artifact distribution")

        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        self.grid_rowconfigure(0, weight=1)
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)

        # 1つ目のフレームの設定
        self.option_frame = LanguageSelect(master=self, header_name="Choose Language")
        self.option_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

class LanguageSelect(tk.CTkFrame):
    def __init__(self, *args, header_name="OptionSelect", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        self.grid_rowconfigure(0, weight=1)
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.label = tk.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 13))
        self.label.grid(row=0, column=0, padx=20, sticky="ew")

        # 言語選択
        self.count = tk.CTkOptionMenu(master=self, font=self.fonts, values=["English", "Japanese"], command=self.language_function)
        self.count.grid(row=1, column=0, padx=20, pady=(0,20), sticky="ew")

        # クローズボタン
        self.close_button = tk.CTkButton(master=self, text="Choose", command=self.master.destroy, font=self.fonts)
        self.close_button.grid(row=1, column=2, padx=10, pady=20, sticky="ew")

    def language_function(self, value):
        global LANGUAGE
        if value == "English":
            LANGUAGE = "en"
        elif value == "Japanese":
            LANGUAGE = "ja"

class App(tk.CTk):

    def __init__(self):
        super().__init__()

        # メンバー変数の設定
        self.fonts = (FONT_TYPE, 15)
        # フォームサイズ設定
        self.geometry("350x200")
        self.title("Basic GUI")

        # フォームのセットアップをする
        self.setup_form()
    
    def setup_form(self):
        # tk のフォームデザイン設定
        tk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        
        # フォームサイズ設定
        self.geometry("1000x1200")
        self.title("Artifact distribution")

        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        self.grid_rowconfigure(0, weight=1)
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)

        self.scroll_frame = ScrollFrame(master=self, header_name="ScrollFrame", fg_color="transparent")
        self.scroll_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

class ScrollFrame(tk.CTkScrollableFrame):
    def __init__(self, *args, header_name="SubOptionSelect", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name

        self.calculator = Calculator()

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1つ目のフレームの設定
        self.option_frame = OptionSelect(master=self, header_name=i18n.t("lang.option_select_header"))
        self.option_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # 2つ目のフレームの設定
        self.distribution_frame = Distribution(master=self, header_name=i18n.t("lang.distribution_header"))
        self.distribution_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        


class OptionSelect(tk.CTkFrame):
    def __init__(self, *args, header_name="OptionSelect", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)

        self.label = tk.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")

        self.option_frame = SubOptionSelect(master=self, header_name=i18n.t("lang.sub_option_select_header"))
        self.option_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        # クローズボタン
        self.close_button = tk.CTkButton(master=self, text=i18n.t("lang.close"), command=sys.exit, font=self.fonts)
        self.close_button.grid(row=1, column=1, padx=10, pady=20, sticky="ew")

        #初期スコア
        self.init_slider_label = tk.CTkLabel(self, text=i18n.t("lang.init_score"), font=(FONT_TYPE, 13))
        self.init_slider_label.grid(row=4, column=0, padx=20, pady=(20,0), sticky="ew")
        self.init_slider = tk.CTkSlider(master=self, from_=0.0, to=40.0, number_of_steps=400, hover=False, width=100, command=self.init_slider_event)
        self.init_slider.grid(row=5, column=0, padx=20, pady=(0,20), sticky="ew")
        self.init_score = tk.CTkEntry(master=self, placeholder_text=i18n.t("lang.init_score"), width=150, font=self.fonts)
        self.init_score.grid(row=6, column=0, padx=10, pady=20)
        self.apply_init_score = tk.CTkButton(master=self, text=i18n.t("lang.apply"), command=self.init_function, font=self.fonts)
        self.apply_init_score.grid(row=6, column=1, padx=10, pady=20)
        #調査スコア
        self.search_slider_label = tk.CTkLabel(self, text=i18n.t("lang.search_score"), font=(FONT_TYPE, 13))
        self.search_slider_label.grid(row=7, column=0, padx=20, pady=(20,0), sticky="ew")
        self.search_slider = tk.CTkSlider(master=self, from_=0.0, to=65.0, number_of_steps=650, hover=False, width=100, command=self.search_slider_event)
        self.search_slider.grid(row=8, column=0, padx=20, pady=(0,20), sticky="ew")
        self.search_score = tk.CTkEntry(master=self, placeholder_text=i18n.t("lang.search_score"), width=150, font=self.fonts)
        self.search_score.grid(row=9, column=0, padx=10, pady=20)
        self.apply_search_score = tk.CTkButton(master=self, text=i18n.t("lang.apply"), command=self.search_function, font=self.fonts)
        self.apply_search_score.grid(row=9, column=1, padx=10, pady=20)
    
    def init_slider_event(self, value):
        global INIT_SCORE
        self.init_score.delete(0, tk.END)
        self.init_score.insert(0, round(value, 1))
        INIT_SCORE = round(value, 1)
    
    def init_function(self):
        global INIT_SCORE
        try:
            value = round(float(self.init_score.get()), 1)
            if value < 0:
                value = 0
            elif 40 < value:
                value = 40
            self.init_slider.set(value)
            self.init_score.delete(0, tk.END)
            self.init_score.insert(0, value)
            INIT_SCORE = value
        except ValueError:
            self.init_score.delete(0, tk.END)

    def search_slider_event(self, value):
        global SCORE
        self.search_score.delete(0, tk.END)
        self.search_score.insert(0, round(value, 1))
        SCORE = round(value, 1)
    
    def search_function(self):
        global SCORE
        try:
            value = round(float(self.search_score.get()), 1)
            if value < 0:
                value = 0
            elif 65 < value:
                value = 65
            self.search_slider.set(value)
            self.search_score.delete(0, tk.END)
            self.search_score.insert(0, value)
            SCORE = value
        except ValueError:
            self.search_score.delete(0, tk.END)

class SubOptionSelect(tk.CTkFrame):
    def __init__(self, *args, header_name="SubOptionSelect", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name

        self.calculator = Calculator()

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.init_option_label = tk.CTkLabel(self, text=i18n.t("lang.init_option"), font=(FONT_TYPE, 13))
        self.init_option_label.grid(row=0, column=0, padx=10, pady=(20,0), sticky="ew")

        self.sub_option_label = tk.CTkLabel(self, text=i18n.t("lang.sub_option"), font=(FONT_TYPE, 13))
        self.sub_option_label.grid(row=0, column=1, padx=10, pady=(20,0), sticky="ew")

        self.reinforcement_label = tk.CTkLabel(self, text=i18n.t("lang.reinforcement"), font=(FONT_TYPE, 13))
        self.reinforcement_label.grid(row=0, column=2, padx=10, pady=(20,0), sticky="ew")

        # サブオプ数
        self.option_radio = tk.IntVar(value=3)
        self.option_3 = tk.CTkRadioButton(master=self, text=i18n.t("lang.3_option"), command=self.radio_function, variable=self.option_radio, value=3)
        self.option_4 = tk.CTkRadioButton(master=self, text=i18n.t("lang.4_option"), command=self.radio_function, variable=self.option_radio, value=4)
        self.option_3.grid(row=1, column=0, padx=10, pady=(0,10))
        self.option_4.grid(row=2, column=0, padx=10, pady=(0,10))

        # サブオプ
        self.crit_dmg = tk.CTkCheckBox(master=self, text=i18n.t("lang.crit_dmg"), command=self.check_function)
        self.crit_rate = tk.CTkCheckBox(master=self, text=i18n.t("lang.crit_rate"), command=self.check_function)
        self.atk = tk.CTkCheckBox(master=self, text=i18n.t("lang.atk"), command=self.check_function)
        self.crit_dmg.grid(row=1, column=1, padx=10, pady=(0,10))
        self.crit_rate.grid(row=2, column=1, padx=10, pady=(0,10))
        self.atk.grid(row=3, column=1, padx=10, pady=(0,10))

        # 強化回数
        self.count = tk.CTkOptionMenu(master=self, font=self.fonts, values=["5"], command=self.count_function)
        self.count.grid(row=1, column=2, padx=20, pady=(0,20), sticky="ew")

    def radio_function(self):
        global OPTION, COUNT
        OPTION = self.option_radio.get()
        if OPTION == 4:
            self.count.configure(values=["1", "2", "3", "4", "5"])
            self.count.set("5")
            COUNT = 5
        else:
            self.count.configure(values=["5"])
            self.count.set("5")
            COUNT = 5

    def count_function(self, value):
        global COUNT
        COUNT = int(value)
    
    def check_function(self):
        global NUMS, IS_CRIT_DMG, IS_CRIT_RATE, IS_ATK
        NUMS = np.zeros(16, dtype = int)
        IS_CRIT_DMG = False
        IS_CRIT_RATE = False
        IS_ATK = False
        if self.crit_dmg.get():
            NUMS[0:4] = CRIT
            IS_CRIT_DMG = True
        if self.crit_rate.get():
            NUMS[4:8] = CRIT
            IS_CRIT_RATE = True
        if self.atk.get():
            NUMS[8:12] = ATK
            IS_ATK = True        

class Distribution(tk.CTkFrame):
    def __init__(self, *args, header_name="Distribution", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name

        self.calculator = Calculator()

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)

        self.label = tk.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")

        self.outputarea_frame = OutPutArea(master=self, header_name=i18n.t("lang.out_put_area_header"))
        self.outputarea_frame.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

        # 更新ボタン
        self.update_button = tk.CTkButton(master=self, text=i18n.t("lang.update"), command=self.update_function, font=self.fonts)
        self.update_button.grid(row=1, column=0, padx=10, pady=20)

        self.update_function()

    def update_function(self):
        # プロットをキャンバスに貼り付ける
        y = self.calculator.calculate()
        self.fig, self.ax = plt.subplots()
        x = np.zeros(y.shape[0])
        for i in range(x.shape[0]):
            x[i] = i / COUNT
        self.ax.bar(INIT_SCORE + x * COUNT / 10, y, width = 0.05)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=2,column=0, padx=20, pady=20, sticky="ew")
        self.canvas.draw()

        self.outputarea_frame.update_function(x, y)

        self.master.update()

class OutPutArea(tk.CTkFrame):
    def __init__(self, *args, header_name="OutPutArea", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name

        self.calculator = Calculator()

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)

        self.label = tk.CTkLabel(self, text=i18n.t("lang.statistics_data"), font=(FONT_TYPE, 13))
        self.label.grid(row=0, column=0, padx=20, sticky="w")
    
    def update_function(self, x, y):
        percentile = [[i18n.t("lang.percentile_rank"), i18n.t("lang.score")],
         [0, SCORE],
         [0, 0],
         [25, 0],
         [50, 0],
         [75, 0],
         [100, 0]]
        sum = 0.0
        for i in range(x.shape[0]):
            if INIT_SCORE + x[i] * COUNT / 10 >= SCORE:
                sum += y[i]
        percentile[1][0] = round(sum * 100, 1)
        for row in range(2, len(percentile), 1):
            percentile[row][1] = round(self.getScore(x, y, percentile[row][0] / 100), 1)
        table = CTkTable(master=self, row=len(percentile), column=2, values=percentile)
        table.grid(row=1,column=0, padx=20, pady=(0, 20), sticky="ew")

        data = [[i18n.t("lang.average"), 0],
        [i18n.t("lang.variance"), 0]]
        ave = 0.0
        for i in range(x.shape[0]):
            ave += (INIT_SCORE + x[i] * COUNT / 10) * y[i]
        data[0][1] = round(ave, 1)
        variance = 0.0
        for i in range(x.shape[0]):
            variance += ((INIT_SCORE + x[i] * COUNT / 10) - ave) ** 2 * y[i]
        data[1][1] = round(variance, 1)
        table = CTkTable(master=self, row=len(data), column=2, values=data)
        table.grid(row=2,column=0, padx=20, pady=(0, 20), sticky="ew")

    def getScore(self, x, y, percent):
        if percent == 0:
            for i in range(x.shape[0] - 1, -1, -1):
                if y[i] != 0:
                    return INIT_SCORE + x[i] * COUNT / 10
        elif percent == 1.0:
            for i in range(x.shape[0]):
                if y[i] != 0:
                    return INIT_SCORE + x[i] * COUNT / 10
        else:
            sum = 0.0
            for i in range(x.shape[0] - 1, -1, -1):
                sum += y[i]
                if sum >= percent:
                    return INIT_SCORE + x[i] * COUNT / 10

class Calculator():
    def getDistribution(self, nums, count):
        dp = np.zeros((count + 1, max(nums) * count + 1))
        dp[0][0] = 1.0

        for i in range(count):
            for num in nums:
                prev = dp[i][:dp.shape[1] - num]
                dp[i + 1][num:] += prev / nums.shape[0]
        
        return dp[count]

    def calculate(self):
        if OPTION == 4:
            y = self.getDistribution(NUMS, COUNT)
            return y
        else:
            NUMS_4OP = []
            if not IS_CRIT_DMG:
                tmp = np.copy(NUMS)
                tmp[12:] = CRIT
                NUMS_4OP.append(tmp)
            if not IS_CRIT_RATE:
                tmp = np.copy(NUMS)
                tmp[12:] = CRIT
                NUMS_4OP.append(tmp)
            if not IS_ATK:
                tmp = np.copy(NUMS)
                tmp[12:] = ATK
                NUMS_4OP.append(tmp)
            
            main_probability = (7 - len(NUMS_4OP)) / 7
            sub_probability = 0
            if len(NUMS_4OP) != 0:
                sub_probability = (1 - main_probability) / len(NUMS_4OP)

            y = np.zeros(np.amax(CRIT) * COUNT + 1) # COUNT = 5

            main_y = self.getDistribution(NUMS, 4)
            y[0:main_y.shape[0]] += main_y * main_probability

            for nums in NUMS_4OP: 
                for num_4th in nums:
                    sub_y = self.getDistribution(nums, 4)
                    y[num_4th:num_4th + sub_y.shape[0]] += sub_y / len(nums) * sub_probability

            return y

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def click_close():
    pass

if __name__ == "__main__":
    # main
    app_lang = AppLanguage()
    app_lang.protocol("WM_DELETE_WINDOW", click_close)
    app_lang.mainloop()
    i18n.load_path.append(resource_path("locales"))
    i18n.set("locale", LANGUAGE)
    i18n.set("fallback", LANGUAGE)
    i18n.set("file_format", "json")
    i18n.set("skip_locale_root_data", True)
    app = App()
    app.protocol("WM_DELETE_WINDOW", click_close)
    app.mainloop()