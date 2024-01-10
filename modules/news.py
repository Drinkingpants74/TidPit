from gnews import GNews
import tkinter as tk

import prefs

GN = GNews()
GN.max_results = 3
GN.period = '1d'
GN.country = prefs.newsCountry
GN.languages = prefs.newsLanguage
GN.exclude_websites = prefs.newsExclude

if (prefs.newsSource != "none"):
    articles = GN.get_news_by_site(prefs.newsSource)
else:
    articles = GN.get_top_news()

articlePos = 0

class News(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure(bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        self.mess = tk.Message(self, bg="black", font=("Helvetica Neue", int(window.winfo_screenwidth() / 20), "bold"))
        self.mess.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.get_text()

    def restart(self):
        global articlePos
        articlePos = 0
        self.get_text()

    def set_text(self, text):
        self.mess.configure(text=text)
        self.after(10000, self.get_text)

    def get_text(self):
        global articles, articlePos
        if (len(articles) != 0):
            value = articles[articlePos]['title']
        if (articlePos >= (len(articles) - 1)):
            articlePos = 0
        else:
            articlePos += 1
        self.set_text(value)