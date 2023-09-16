import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# 数据预处理：读取数据，请将数据文件路径替换为实际路径
data = pd.read_csv("C:/Users/jacks/Desktop/AI - Own System/dataset/Final.csv")

# 创建TF-IDF向量化器
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8, min_df=2)
tfidf_matrix = tfidf_vectorizer.fit_transform(data['keywords'].fillna(''))

# 计算书籍之间的余弦相似度
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# 创建书籍标题到索引的映射
indices = pd.Series(data.index, index=data['title']).drop_duplicates()

# 定义一个函数来根据用户输入的书籍关键词推荐相似的书籍
def recommend_books(user_input):
    # 基于用户输入，计算与所有书籍的相似度
    user_tfidf = tfidf_vectorizer.transform([user_input])
    cosine_similarities = linear_kernel(user_tfidf, tfidf_matrix).flatten()
    related_books_indices = cosine_similarities.argsort()[::-1]
    recommended_books = data[['title', 'image_url']].iloc[related_books_indices]
    return recommended_books

# 创建 tkinter GUI 窗口
window = tk.Tk()
window.title("Book Recommendation System")

# 创建标签
label = tk.Label(window, text="Enter a book title or keywords:")
label.pack()

# 创建文本框
entry = tk.Entry(window)
entry.pack()

# 创建一个标签和输入框，用于输入要推荐的书籍数量
num_books_label = tk.Label(window, text="Number of books to recommend:")
num_books_label.pack()
num_books_entry = tk.Entry(window)  # 用户输入要推荐的书籍数量
num_books_entry.pack()

# 创建推荐按钮
button = tk.Button(window, text="Recommend")
button.pack()

# 创建可滚动的框架
scrollable_frame = ttk.Frame(window)
scrollable_frame.pack(fill='both', expand=True)

# 创建垂直滚动条
scrollbar = ttk.Scrollbar(scrollable_frame, orient='vertical')
scrollbar.pack(side='right', fill='y')

# 创建 Canvas 以包含书籍图像和标题
canvas = tk.Canvas(scrollable_frame, yscrollcommand=scrollbar.set)
canvas.pack(fill='both', expand=True)

# 设置 Canvas 内部的窗口为可滚动区域
canvas_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=canvas_frame, anchor='nw')

def resize_canvas(event):
    canvas.config(scrollregion=canvas.bbox('all'))
    canvas.itemconfig(canvas_frame, width=event.width)  # 更新 canvas_frame 的宽度
    canvas.itemconfig(output_text, width=event.width)  # 更新 output_text 的宽度


# 创建 output_text_widget
output_text_widget = tk.Text(canvas_frame, height=200, width=400)
output_text_widget.pack()

# 定义一个函数来调整 output_text_widget 的大小
# 定义一个函数来调整 output_text_widget 的大小
def resize_output_text(event):
    new_width = event.width
    new_height = event.height
    output_text_widget.config(width=new_width, height=new_height)









# 用于跟踪当前加载的书籍数量
current_num_books = 0

# 定义一个函数来显示推荐的书籍图像和标题
def display_book_images(recommended_books, num_books, start_index=0):
    output_text_widget.delete(1.0, tk.END)  # 清空之前的内容
    for i in range(start_index, min(start_index + num_books, len(recommended_books))):
        # 显示书籍标题
        title = recommended_books.iloc[i]['title']
        output_text_widget.insert(tk.END, title + '\n')

        # 显示书籍图像
        image_url = recommended_books.iloc[i]['image_url']
        if not pd.isna(image_url):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                }
                response = requests.get(image_url, headers=headers)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    image = Image.open(image_data)
                    image = image.resize((150, 200), Image.LANCZOS)  # 使用LANCZOS进行重采样
                    photo = ImageTk.PhotoImage(image)
                    image_label = tk.Label(output_text_widget, image=photo)
                    image_label.image = photo
                    output_text_widget.window_create(tk.END, window=image_label)
                else:
                    output_text_widget.insert(tk.END, "Image not available\n")
            except Exception as e:
                print(f"Error loading image: {e}")
                output_text_widget.insert(tk.END, "Image not available\n")
        else:
            output_text_widget.insert(tk.END, "Image not available\n")

# 定义一个函数来执行推荐操作
def recommend():
    global current_num_books
    user_input = entry.get()  # 获取用户输入
    recommended_books = recommend_books(user_input)  # 调用推荐函数
    
    # 获取用户输入的要推荐的书籍数量
    num_books_text = num_books_entry.get()
    
    # 添加输入验证，如果用户未输入数量或输入无效，则默认为10
    try:
        num_books = int(num_books_text)
        if num_books <= 0:
            num_books = 10  # 默认为10本书
    except ValueError:
        num_books = 10  # 默认为10本书

    # 显示推荐书籍的图像和标题
    display_book_images(recommended_books, num_books)

    # 更新当前加载的书籍数量
    current_num_books = num_books

# 在应用程序启动时显示初始的书籍
recommend()

# 绑定推荐按钮的点击事件
button.config(command=recommend)

# 启动 tkinter 主循环
window.mainloop()     

