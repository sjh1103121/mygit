import customtkinter as ctk
from tkinter import messagebox
import threading
from langchain_community.llms import tongyi
import time

# 设置外观模式和默认颜色主题
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

API_KEY = 'sk-ce8aa4d016dd4541a87f59cbd9bff46c'

class ModernChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant - Pro")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)  # 设置最小窗口大小

        # 网格布局配置
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # --- 侧边栏 ---
        self.sidebar = ctk.CTkFrame(self.root, width=180, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        # Logo 标题
        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="AI 助手", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 侧边栏按钮：新建对话
        self.sidebar_button_1 = ctk.CTkButton(
            self.sidebar, 
            text="新建对话", 
            command=self.clear_chat,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE")
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        # 侧边栏底部：外观模式切换
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="外观模式:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # --- 主聊天区域 ---
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)

        # 1. 聊天记录显示区 - 使用Textbox替代ScrollableFrame
        self.chat_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # 初始化 LLM
        try:
            self.llm = tongyi.Tongyi(api_key=API_KEY)
            self.add_message("系统", "模型已连接，赵军大模型可为您服务。", is_system=True)
        except Exception as e:
            self.add_message("系统", f"模型连接失败: {e}", is_system=True)

        # 2. 底部输入区
        self.entry_frame = ctk.CTkFrame(self.main_frame, height=60, fg_color="transparent")
        self.entry_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.entry_frame.grid_columnconfigure(0, weight=1)
        
        self.user_input = ctk.CTkEntry(
            self.entry_frame, 
            placeholder_text="输入您的问题...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message_event)

        self.send_button = ctk.CTkButton(
            self.entry_frame, 
            text="发送", 
            width=80,
            height=40,
            font=ctk.CTkFont(size=14),
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1)

    def add_message(self, role, text, is_system=False):
        """添加消息气泡到界面"""
        if is_system:
            # 系统消息样式 - 居中显示
            sys_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent", height=30)
            sys_frame.pack(fill="x", pady=2)
            sys_frame.grid_columnconfigure(0, weight=1)
            
            label = ctk.CTkLabel(
                sys_frame, 
                text=text, 
                text_color="gray",
                font=ctk.CTkFont(size=11, slant="italic")
            )
            label.grid(row=0, column=0)
            return
            
        # 创建消息容器
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.pack(fill="x", pady=5, padx=5)
        
        if role == "我":
            # 用户消息：靠右，蓝色
            msg_container.grid_columnconfigure(0, weight=1)
            
            inner_frame = ctk.CTkFrame(
                msg_container, 
                fg_color="#3b8ed0", 
                corner_radius=15
            )
            inner_frame.grid(row=0, column=1, sticky="e", padx=(20, 5))
            
            # 用户消息使用 Textbox 以支持复制（可选，如果用户也需要复制自己的话）
            text_box = ctk.CTkTextbox(
                inner_frame,
                wrap="word",
                fg_color="transparent", # 背景透明，显示父容器的蓝色
                border_width=0,         # 无边框
                text_color="white",
                font=ctk.CTkFont(size=13)
            )
            text_box.insert("0.0", text)
            text_box.configure(state="disabled") # 设为只读
            text_box.pack(padx=15, pady=10, fill="both", expand=True)
            
            # 添加用户标签
            user_label = ctk.CTkLabel(
                msg_container,
                text="我",
                text_color="gray",
                font=ctk.CTkFont(size=11)
            )
            user_label.grid(row=1, column=1, sticky="e", padx=(0, 10))
            
        else:
            # AI 消息：靠左，灰色
            msg_container.grid_columnconfigure(1, weight=1)
            
            inner_frame = ctk.CTkFrame(
                msg_container, 
                fg_color=("gray90", "gray30"), 
                corner_radius=15
            )
            inner_frame.grid(row=0, column=0, sticky="w", padx=(5, 20))
            
            # 【关键修改】AI 回复使用 Textbox 替代 Label
            text_box = ctk.CTkTextbox(
                inner_frame,
                wrap="word",             # 按单词换行
                fg_color="transparent",  # 背景透明
                border_width=0,          # 无边框
                text_color=("gray10", "gray90"),
                font=ctk.CTkFont(size=13)
            )
            text_box.insert("0.0", text)
            text_box.configure(state="disabled") # 设为只读，但允许选择和复制
            text_box.pack(padx=15, pady=10, fill="both", expand=True)
            
            # 添加AI标签
            ai_label = ctk.CTkLabel(
                msg_container,
                text="AI助手",
                text_color="gray",
                font=ctk.CTkFont(size=11)
            )
            ai_label.grid(row=1, column=0, sticky="w", padx=(10, 0))
        
        # 滚动到底部
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def clear_chat(self):
        """清空聊天记录"""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.add_message("系统", "对话已清空，开始新的对话。", is_system=True)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def send_message_event(self, event):
        self.send_message()

    def send_message(self):
        question = self.user_input.get().strip()
        if not question:
            return

        # 显示用户消息
        self.add_message("我", question)
        self.user_input.delete(0, "end")
        
        # 禁用输入和按钮，显示加载状态
        self.user_input.configure(state="disabled")
        self.send_button.configure(state="disabled", text="思考中...")
        
        # 开启线程获取AI响应
        threading.Thread(target=self.fetch_ai_response, args=(question,), daemon=True).start()

    def fetch_ai_response(self, question):
        try:
            # 模拟思考时间，避免立即响应
            time.sleep(0.5)
            response = self.llm.invoke(question)
            # 在主线程更新UI
            self.root.after(0, self.add_message, "AI", response)
        except Exception as e:
            self.root.after(0, self.add_message, "系统", f"错误: {str(e)}", True)
        finally:
            # 恢复输入和按钮状态
            self.root.after(0, lambda: self.user_input.configure(state="normal"))
            self.root.after(0, lambda: self.send_button.configure(state="normal", text="发送"))
            self.root.after(0, lambda: self.user_input.focus())

if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernChatApp(root)
    root.mainloop()
