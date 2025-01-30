from tkinter import font as tkfont, ttk
from most_trending_hash import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.widgets import TextBox, Button

class SocialMediaDashboard:

    # Create and set up the main dashboard
    def __init__(self, master):
        width = 1200
        height = 850
        self.master = master
        self.master.title("TrendWave")
        self.master.geometry("1200x850")
        self.master.configure(bg="#f0f0f0")
        self.title_font = tkfont.Font(family="Helvetica", size=32, weight="bold")
        self.subtitle_font = tkfont.Font(family="Helvetica", size=16)
        self.button_font = tkfont.Font(family="Helvetica", size=32, weight="bold")

        self.title_label = tk.Label(self.master, text="TrendWave Dashboard", font=self.title_font, bg="#f0f0f0",fg="#333333")
        self.title_label.pack(pady=(30, 0))
        self.subtitle_label = tk.Label(self.master,
                                       text="Our vision is to empower SMBs and individual content creators with an intuitive, powerful tool that takes the guesswork out of social media strategy. \nBy harnessing advanced analytics, we analyze recent posts contents to forecast emerging Instagram trends before they hit the mainstream. "
                                            "\nCheck out social media platforms below to see the trend analysis!",
                                       font=self.subtitle_font, bg="#f0f0f0", fg="#666666")
        self.subtitle_label.pack(pady=(5, 25))
        self.canvas = tk.Canvas(self.master, width=width, height=height, bg="#f0f0f0", highlightthickness=0)
        self.canvas.pack()
        self.create_clickable_rectangle(width * (1 / 8), height * (1 / 8), width * (3 / 5), height * (3 / 8), "#ff9248",
                                        "Instagram", self.open_instagram)
        self.create_clickable_rectangle(width * (1 / 8), height * (4 / 8), width * (3 / 5), height * (6 / 8), "#982B1C",
                                        "Reddit", self.open_reddit)

    # Create two social media options that is clickable
    def create_clickable_rectangle(self, x1, y1, x2, y2, color, text, command):
        rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)
        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text, font=self.button_font, fill="white")
        self.canvas.tag_bind(rectangle, "<Button-1>", command)
        additional_text = "Click to see advanced metrics and trend analysis for " + text
        self.canvas.create_text(x2 + 20, (y1 + y2) / 2, text=additional_text, font=self.subtitle_font, fill="#333333",
                                anchor="w")
        self.search_entry = None

    # Open a new window for Instagram once the user click the option
    def open_instagram(self, event):
        self.open_new_window("Instagram", "#ff9248")

    # Open a new window for Reddit once the user click the option
    def open_reddit(self, event):
        self.open_new_window("Reddit", "#982B1C")

    # Open a new window for Twitter once the user click the option
    def open_twitter(self):
        self.open_new_window("Twitter", "#4285F4")

    # Opens a new window for trend analysis of a specific platform
    def open_new_window(self, platform, color):
        new_window = tk.Toplevel(self.master)
        new_window.title(f"{platform} Trend Analysis")
        new_window.geometry("1300x900")
        new_window.configure(bg="#f0f0f0")
        label = tk.Label(new_window, text=f"Welcome to {platform} Trend Dashboard!", font=self.title_font, bg="#f0f0f0", fg=color)
        label.pack(pady=10)
        if platform in ["Instagram", "Reddit"]:
            twitter_button = tk.Button(new_window, text="Validate at Twitter Trend", command=self.open_twitter, font=("Arial", 16))
            twitter_button.place(relx=1, rely=0, anchor="ne", x=-10, y=10)
            twitter_button.config(height=2)
        back_button = tk.Button(new_window, text="Back to the Main Page", command=new_window.destroy,
                                font=("Arial", 16))
        back_button.place(relx=0, rely=0, anchor="nw", x=10, y=10)
        back_button.config(height=2)
        reddit_df = pd.read_csv("trendy_reddit_topics.csv")
        instagram_df = pd.read_csv("instagram_posts.csv")
        preprocessed_reddit, preprocessed_instagram = preprocess_data(reddit_df, instagram_df)
        if platform == "Twitter":
            self.twitter(new_window)
        elif platform == "Reddit":
            self.reddit(preprocessed_reddit, new_window)
        elif platform == "Instagram":
            self.instagram(preprocessed_instagram, new_window)

    # Displays the Twitter search interface
    def twitter(self, window):
        subtitle = tk.Label(window, text="Enter text here to check the popularity on Twitter", font=("Arial", 24),
                            bg="#f0f0f0", fg="#666666")
        subtitle.pack(pady=(150, 20))
        search_frame = tk.Frame(window, bg="#f0f0f0")
        search_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 32), width=25)
        self.search_entry.pack(pady=(20, 15))
        search_button = tk.Button(search_frame, text="Search", command=lambda: self.perform_search(self.search_entry.get(), window),
                                  font=("Arial", 22), padx=30, pady=15)

        search_button.pack()
        tk.Label(search_frame, text="", bg="#f0f0f0").pack(pady=60)
        result_frame = tk.Frame(window, bg="#f0f0f0")
        result_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)
        self.result_text = tk.Text(result_frame, font=("Arial", 14), wrap=tk.WORD, height=10)
        self.result_text.pack(expand=True, fill=tk.BOTH)
        self.result_text.config(state=tk.DISABLED)

    # Search for trending topics on Twitter based on user input.
    def perform_search(self, query, window):
        df = pd.read_csv('Twitter_trends.csv')
        df['Trending Topic'] = df['Trending Topic'].str.lower()
        matches = df[df['Trending Topic'].str.contains('|'.join(r'\b' + word + r'\b' for word in query.lower().split()),
                                                       case=False, regex=True)]
        if not matches.empty:
            result_window = tk.Toplevel(window)
            result_window.title(f"Search Results for '{query}'")
            result_window.geometry("800x700")
            tree = ttk.Treeview(result_window, columns=list(matches.columns), show="headings")
            for column in matches.columns:
                tree.heading(column, text=column)
                tree.column(column, width=100)
            for _, row in matches.iterrows():
                tree.insert("", "end", values=list(row))
            tree.pack(fill="both", expand=True)
            result_message = f"Results for '{query}' displayed in a new window."
        else:
            result_message = f"'{query}' is not a trending word on Twitter."
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_message)
        self.result_text.config(state=tk.DISABLED)
        self.search_entry.delete(0, tk.END)

    # Create and display Reddit trend analysis plots and tables
    def reddit(self, preprocessed_reddit, window):
        fig, axs = plt.subplots(2, 2, figsize=(14, 14), gridspec_kw={'height_ratios': [1, 1]})
        plot_top_subreddits(preprocessed_reddit, axs[0, 0])
        axs[0, 0].set_title("Top 10 Subreddits by Engagement", fontsize=14, fontweight='bold')
        plot_average_score_distribution(preprocessed_reddit, axs[0, 1])
        axs[0, 1].set_title("Average Score Distribution Among Top 5 Subreddits", fontsize=18, fontweight='bold')
        table_data = [
            get_top_subreddits_by_engagement(preprocessed_reddit).head(),
            get_average_score_per_subreddit(preprocessed_reddit).head()
        ]
        table_titles = ["Top Subreddits by Engagement", "Top Subreddits by Score"]
        for i in range(2):
            axs[1, i].axis('off')
            table = axs[1, i].table(cellText=table_data[i].values, colLabels=table_data[i].columns, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 3.5)
            axs[1, i].set_title(table_titles[i], fontsize=14, fontweight='bold', y=1.0, pad=-30)

        plt.tight_layout(pad=3.0, h_pad=1, w_pad=1.0)
        fig.subplots_adjust(wspace=0.2, hspace=0.5)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Create and display Instagram trend analysis plots and trending probability check.
    def instagram(self, preprocessed_instagram, window):
        ignore_list = ['instagram', 'reelsinstagram', 'trending', 'viral', 'trend', 'new']
        fig, axs = plt.subplots(2, 3, figsize=(18, 16), gridspec_kw={'height_ratios': [1, 0.8]})
        plot_trending_hashtags(preprocessed_instagram, ignore_list, axs[0, 0])
        axs[0, 0].set_title("Top 10 Trending Hashtags by Frequency", fontsize=14, fontweight='bold')
        plot_hashtag_reach_vs_frequency(preprocessed_instagram, ignore_list, axs[0, 1])
        axs[0, 1].set_title("Hashtag Reach vs Frequency", fontsize=14, fontweight='bold')
        axs[0, 2].axis('off')
        axs[0, 2].text(0.5, 0.9, "Trending Probability Check", fontsize=14, fontweight='bold', ha='center', va='center')
        textbox_ax = fig.add_axes([0.7, 0.7, 0.2, 0.05])
        text_box = TextBox(textbox_ax, label='')
        fig.text(0.83, 0.80, 'Enter a caption for trending prediction', fontsize=10, horizontalalignment='center')
        button_ax = fig.add_axes([0.86, 0.7, 0.1, 0.05])
        button = Button(button_ax, 'Check')
        result_text = axs[0, 2].text(0, 0.3, '', fontsize=12,fontweight='bold' )
        table_data1 = get_trending_hashtags_by_frequency(preprocessed_instagram).head()
        table_data2 = get_trending_hashtags_by_reach(preprocessed_instagram).head()
        table_data3 = get_average_likes_comments_per_post(preprocessed_instagram).head()
        table_data = [table_data1, table_data2, table_data3]
        table_titles = ["Top 10 Trending Hashtags by Frequency", "Top 10 Trending Hashtags by Reach", "Average Likes and Comments per Post"]
        for i in range(3):
            axs[1, i].axis('off')
            table = axs[1, i].table(cellText=table_data[i].values, colLabels=table_data[i].columns, cellLoc='center',loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 3)
            axs[1, i].set_title(table_titles[i], fontsize=12, fontweight='bold', y=1.0, pad=-30)
        fig.tight_layout(pad=3.0, h_pad=2.0, w_pad=2.0)
        fig.subplots_adjust(top=0.93, hspace=0.4)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # User click "check for probability" button
        def on_button_click(event):
            caption = text_box.text
            trending_probability = check_trending_probability(caption, preprocessed_instagram)
            result_message = f"Trending Probability for {caption}: {trending_probability:.2f}"
            result_text.set_text(result_message)
            fig.canvas.draw_idle()  # Redraw the figure to update the text
        button.on_clicked(on_button_click)

root = tk.Tk()
app = SocialMediaDashboard(root)
root.mainloop()