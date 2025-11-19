#!/usr/bin/env python3
"""
GUI приложение для взаимодействия с Qwen AI
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import threading
from webdriverAI import WebdriverAI
import os
import tempfile
import pyperclip
from PIL import Image, ImageTk
import io


class QwenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Qwen AI Assistant")
        self.root.geometry("900x700")
        
        # Инициализируем webdriverAI
        self.ai = None
        self.browser_id = 0
        
        # Путь к изображению
        self.image_path = None
        self.copied_image = None  # Изображение из буфера обмена
        
        self.setup_ui()
        self.setup_keyboard_bindings()
        self.init_ai()
    
    def setup_ui(self):
        # Основной фрейм
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Поле для ввода запроса
        tk.Label(main_frame, text="Ваш запрос:", font=("Arial", 12)).pack(anchor=tk.W)
        
        self.input_text = scrolledtext.ScrolledText(main_frame, height=6, font=("Arial", 11))
        self.input_text.pack(fill=tk.X, pady=(5, 10))
        
        # Кнопки управления
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.attach_btn = tk.Button(button_frame, text="Прикрепить изображение", command=self.attach_image)
        self.attach_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.paste_btn = tk.Button(button_frame, text="Вставить изображение (Ctrl+V)", command=self.paste_image)
        self.paste_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.send_btn = tk.Button(button_frame, text="Отправить запрос", command=self.send_request, bg="green", fg="white")
        self.send_btn.pack(side=tk.RIGHT)
        
        # Поле для отображения изображения
        self.image_frame = tk.Frame(main_frame)
        self.image_frame.pack(fill=tk.X, pady=5)
        
        self.image_label = tk.Label(self.image_frame, text="Изображение не прикреплено", fg="gray")
        self.image_label.pack(anchor=tk.W)
        
        # Предварительный просмотр изображения
        self.image_preview = tk.Label(self.image_frame)
        self.image_preview.pack(anchor=tk.W, pady=(5, 0))
        
        # Поле для вывода ответа
        tk.Label(main_frame, text="Ответ Qwen:", font=("Arial", 12)).pack(anchor=tk.W, pady=(10, 0))
        
        self.output_text = scrolledtext.ScrolledText(main_frame, height=15, font=("Arial", 11), state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
    
    def setup_keyboard_bindings(self):
        """Настройка горячих клавиш"""
        self.root.bind('<Control-v>', self.on_ctrl_v)
    
    def on_ctrl_v(self, event):
        """Обработка события Ctrl+V"""
        self.paste_image()
        return "break"  # Предотвращаем дальнейшую обработку события
    
    def init_ai(self):
        """Инициализация AI и браузера"""
        try:
            self.ai = WebdriverAI()
            self.ai.start_browsers(1)
            
            # Авторизация (вам нужно будет указать свои учетные данные)
            login_success = self.ai.login_to_ai(
                browser_id=self.browser_id,
                ai_type="qwen",
                email="your_email@example.com",  # ЗАМЕНИТЕ НА ВАШ EMAIL
                password="your_password"         # ЗАМЕНИТЕ НА ВАШ ПАРОЛЬ
            )
            
            if login_success:
                messagebox.showinfo("Успех", "Успешно подключено к Qwen!")
            else:
                messagebox.showerror("Ошибка", "Не удалось авторизоваться в Qwen")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось инициализировать AI: {str(e)}")
    
    def attach_image(self):
        """Прикрепить изображение из файловой системы"""
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            self.image_path = file_path
            self.copied_image = None  # Сбрасываем изображение из буфера
            self.image_label.config(text=f"Прикреплено изображение: {os.path.basename(file_path)}", fg="blue")
            self.show_image_preview(file_path)
    
    def paste_image(self):
        """Вставить изображение из буфера обмена"""
        try:
            # Попробуем получить изображение из буфера обмена
            image_data = pyperclip.paste()
            
            if isinstance(image_data, str) and image_data.startswith("http"):
                # Это может быть ссылка, а не изображение
                messagebox.showwarning("Предупреждение", "В буфере обмена находится текст/ссылка, а не изображение")
                return
            
            # Попробуем получить изображение напрямую из буфера
            try:
                # Для Windows может потребоваться специальная обработка
                import win32clipboard
                win32clipboard.OpenClipboard()
                try:
                    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                        data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                        # Создаем изображение из буфера
                        image = Image.frombuffer("RGB", (0, 0), data, "DIB", "BGR", 0)
                        self.copied_image = image
                        self.image_path = None  # Сбрасываем путь к файлу
                        
                        # Сохраняем временное изображение
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                            image.save(tmp_file.name, 'PNG')
                            self.image_path = tmp_file.name
                        
                        self.image_label.config(text="Изображение из буфера обмена", fg="blue")
                        self.show_image_preview(self.image_path)
                    else:
                        messagebox.showwarning("Предупреждение", "В буфере обмена нет изображения")
                finally:
                    win32clipboard.CloseClipboard()
            except ImportError:
                # Если win32clipboard недоступен, используем альтернативный подход
                messagebox.showwarning("Предупреждение", "Не удалось получить изображение из буфера обмена. Установите pywin32: pip install pywin32")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить изображение из буфера: {str(e)}")
    
    def show_image_preview(self, image_path):
        """Показать предварительный просмотр изображения"""
        try:
            image = Image.open(image_path)
            # Изменяем размер для предварительного просмотра
            image.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image)
            
            self.image_preview.config(image=photo)
            self.image_preview.image = photo  # Сохраняем ссылку на изображение
        except Exception as e:
            self.image_preview.config(image='', text=f"Ошибка загрузки превью: {str(e)}", fg="red")
    
    def send_request(self):
        """Отправить запрос в Qwen"""
        if not self.ai:
            messagebox.showerror("Ошибка", "AI не инициализирован")
            return
        
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите запрос")
            return
        
        # Отображаем запрос в окне вывода
        self.update_output(f"Ваш запрос: {user_input}\n\n")
        
        # Если есть изображение, прикрепляем его
        image_attached = False
        if self.image_path:
            try:
                self.ai.upload_image(self.browser_id, self.image_path)
                self.update_output("Изображение прикреплено к запросу\n\n")
                image_attached = True
            except Exception as e:
                self.update_output(f"Ошибка прикрепления изображения: {str(e)}\n\n")
        
        # Отправляем запрос в отдельном потоке, чтобы не блокировать GUI
        threading.Thread(target=self.process_request, args=(user_input, image_attached), daemon=True).start()
    
    def process_request(self, user_input, image_attached):
        """Обработка запроса в отдельном потоке"""
        try:
            # Создаем новый чат
            self.ai.new_chat(self.browser_id)
            
            # Отправляем сообщение
            self.ai.write_message(self.browser_id, user_input)
            self.ai.send(self.browser_id)
            
            # Получаем ответ
            answer = self.ai.get_answer(self.browser_id)
            
            # Обновляем интерфейс в основном потоке
            status = "с изображением" if image_attached else "без изображения"
            self.root.after(0, self.update_output, f"Ответ Qwen ({status}):\n{answer}\n\n" + "="*50 + "\n\n")
            
        except Exception as e:
            self.root.after(0, self.update_output, f"Ошибка при обработке запроса: {str(e)}\n\n")
    
    def update_output(self, text):
        """Обновление поля вывода"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def __del__(self):
        """Очистка временных файлов при закрытии"""
        if self.image_path and os.path.exists(self.image_path) and self.image_path.startswith(tempfile.gettempdir()):
            try:
                os.remove(self.image_path)
            except:
                pass  # Игнорируем ошибки при удалении временного файла


def main():
    root = tk.Tk()
    app = QwenGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()