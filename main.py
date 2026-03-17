
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
import ctypes
import os

from deque_python import DequePython

cpp_ok = False
stl_ok = False
cpp_lib = None

cur_path = os.path.dirname(__file__)

cpp_lib = ctypes.CDLL(os.path.join(cur_path, "deque_cpp.dll"))

cpp_lib.deque_create.argtypes = []
cpp_lib.deque_create.restype = ctypes.c_void_p

cpp_lib.deque_destroy.argtypes = [ctypes.c_void_p]
cpp_lib.deque_destroy.restype = None

cpp_lib.deque_push_front.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]
cpp_lib.deque_push_front.restype = None

cpp_lib.deque_push_back.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]
cpp_lib.deque_push_back.restype = None

cpp_lib.deque_pop_front.argtypes = [ctypes.c_void_p]
cpp_lib.deque_pop_front.restype = ctypes.c_int

cpp_lib.deque_pop_back.argtypes = [ctypes.c_void_p]
cpp_lib.deque_pop_back.restype = ctypes.c_int

cpp_lib.deque_get_size.argtypes = [ctypes.c_void_p]
cpp_lib.deque_get_size.restype = ctypes.c_int

cpp_lib.deque_is_empty.argtypes = [ctypes.c_void_p]
cpp_lib.deque_is_empty.restype = ctypes.c_int

cpp_lib.deque_to_string.argtypes = [ctypes.c_void_p]
cpp_lib.deque_to_string.restype = ctypes.POINTER(ctypes.c_char)

cpp_lib.deque_free_string.argtypes = [ctypes.POINTER(ctypes.c_char)]
cpp_lib.deque_free_string.restype = None

cpp_lib.deque_clear.argtypes = [ctypes.c_void_p]
cpp_lib.deque_clear.restype = None

cpp_ok = True 

import last_deque_stl
stl_ok = True

cur_mod = "Python"
dq = None
dq_handle = None
cur_lib = None
stl_dq = None


def make_deque():
    global dq, dq_handle, cur_lib, stl_dq

    if cur_mod == "Python":
        dq = DequePython()
        dq_handle = None
        cur_lib = None
        stl_dq = None
    elif cur_mod == "C++":
        if cpp_ok:
            dq = None
            stl_dq = None
            cur_lib = cpp_lib
            dq_handle = cpp_lib.deque_create()
        else:
            showerror("Ошибка", "Модуль C++ не найден!")
            return False
    elif cur_mod == "STL":
        if stl_ok:
            dq = None
            dq_handle = None
            cur_lib = None
            stl_dq = last_deque_stl.DequeSTL()
        else:
            showerror("Ошибка", "Модуль STL не найден!")
            return False

    return True


def do_push_front(num1, txt):
    if cur_mod == "Python":
        dq.push_front(num1, txt)
    elif cur_mod == "C++":
        cur_lib.deque_push_front(dq_handle, num1, txt.encode('utf-8'))
    elif cur_mod == "STL":
        stl_dq.push_front(num1, txt)


def do_push_back(num1, txt):
    if cur_mod == "Python":
        dq.push_back(num1, txt)
    elif cur_mod == "C++":
        cur_lib.deque_push_back(dq_handle, num1, txt.encode('utf-8'))
    elif cur_mod == "STL":
        stl_dq.push_back(num1, txt)


def do_pop_front():
    if cur_mod == "Python":
        return dq.pop_front()
    elif cur_mod == "C++":
        return cur_lib.deque_pop_front(dq_handle) == 1
    elif cur_mod == "STL":
        return stl_dq.pop_front()


def do_pop_back():
    if cur_mod == "Python":
        return dq.pop_back()
    elif cur_mod == "C++":
        return cur_lib.deque_pop_back(dq_handle) == 1
    elif cur_mod == "STL":
        return stl_dq.pop_back()


def do_get_size():
    if cur_mod == "Python":
        return dq.get_size()
    elif cur_mod == "C++":
        return cur_lib.deque_get_size(dq_handle)
    elif cur_mod == "STL":
        return stl_dq.get_size()


def do_is_empty():
    if cur_mod == "Python":
        return dq.is_empty()
    elif cur_mod == "C++":
        return cur_lib.deque_is_empty(dq_handle) == 1
    elif cur_mod == "STL":
        return stl_dq.is_empty()


def do_to_string():
    if cur_mod == "Python":
        return dq.to_string()
    elif cur_mod == "C++":
        res = cur_lib.deque_to_string(dq_handle)
        if res:
            s = ctypes.cast(res, ctypes.c_char_p).value.decode('utf-8')
            cur_lib.deque_free_string(res)
            return s
        return ""
    elif cur_mod == "STL":
        return stl_dq.to_string()

def do_clear():
    if cur_mod == "Python":
        dq.clear()
    elif cur_mod == "C++":
        cur_lib.deque_clear(dq_handle)
    elif cur_mod == "STL":
        stl_dq.clear()


def pick_python():
    global cur_mod
    cur_mod = "Python"
    lbl_mod['text'] = "Текущий модуль: Python"
    if make_deque():
        refresh()
        showinfo("Инфо", "Подключен модуль Python")


def pick_cpp():
    global cur_mod
    if not cpp_ok:
        showerror("Ошибка", "Модуль C++ не найден!")
        return

    cur_mod = "C++"
    lbl_mod['text'] = "Текущий модуль: C++"
    if make_deque():
        refresh()
        showinfo("Инфо", "Подключен модуль C++")


def pick_stl():
    global cur_mod
    if not stl_ok:
        showerror("Ошибка", "Модуль STL не найден!")
        return

    cur_mod = "STL"
    lbl_mod['text'] = "Текущий модуль: STL"
    if make_deque():
        refresh()
        showinfo("Инфо", "Подключен модуль STL (pybind11)")


def btn_push_back():
    if dq is None and dq_handle is None and stl_dq is None:
        showerror("Ошибка", "Сначала выберите модуль!")
        return

    num1 = ent_num.get()
    txt = ent_txt.get()

    if num1 == "" or txt == "":
        showinfo("Внимание", "Заполните все поля!")
        return

    num2 = int(num1)
    if len(txt) > 9:
        showinfo("Внимание", "Текст макс 9 символов!")
        return

    do_push_back(num2, txt)
    clear_fields()
    refresh()


def btn_push_front():
    if dq is None and dq_handle is None and stl_dq is None:
        showerror("Ошибка", "Сначала выберите модуль!")
        return

    num1 = ent_num.get()
    txt = ent_txt.get()

    if num1 == "" or txt == "":
        showinfo("Внимание", "Заполните все поля!")
        return

    num2 = int(num1)
    if len(txt) > 9:
        showinfo("Внимание", "Текст макс 9 символов!")
        return

    do_push_front(num2, txt)
    clear_fields()
    refresh()


def btn_pop_back():
    if dq is None and dq_handle is None and stl_dq is None:
        showerror("Ошибка", "Сначала выберите модуль!")
        return

    if do_is_empty():
        showinfo("Внимание", "Дек пуст!")
        return

    do_pop_back()
    refresh()


def btn_pop_front():
    if dq is None and dq_handle is None and stl_dq is None:
        showerror("Ошибка", "Сначала выберите модуль!")
        return

    if do_is_empty():
        showinfo("Внимание", "Дек пуст!")
        return

    do_pop_front()
    refresh()


def clear_fields():
    ent_num.delete(0, tk.END)
    ent_txt.delete(0, tk.END)


def btn_clear():
    if dq is None and dq_handle is None and stl_dq is None:
        showerror("Ошибка", "Сначала выберите модуль!")
        return

    do_clear()
    clear_fields()
    refresh()
    showinfo("Инфо", "Дек очищен")


def refresh():
    txt_out.delete(1.0, tk.END)
    txt_out.insert(tk.END, f"Модуль: {cur_mod}\n")
    txt_out.insert(tk.END, "=" * 50 + "\n")
    txt_out.insert(tk.END, "Содержимое дека:\n")
    txt_out.insert(tk.END, "-" * 50 + "\n")

    if dq is not None or dq_handle is not None or stl_dq is not None:
        s = do_to_string()
        if s:
            txt_out.insert(tk.END, s)
        else:
            txt_out.insert(tk.END, "(пусто)\n")

        txt_out.insert(tk.END, "-" * 50 + "\n")
        txt_out.insert(tk.END, f"Размер: {do_get_size()} элементов")
    else:
        txt_out.insert(tk.END, "Модуль не выбран")


def about():
    msg = "Демонстрация работы с деком\n\n"
    msg += "Модули:\n"
    msg += f"  Python: Да\n"
    msg += f"  C++ (ctypes): {'Да' if cpp_ok else 'Нет'}\n"
    msg += f"  STL (pybind11): {'Да' if stl_ok else 'Нет'}\n"
    showinfo("О программе", msg)


win = tk.Tk()
win.title("Работа с деком")
win.geometry("600x500")

lib_menu = tk.Menu()
lib_menu.add_command(label="Python", command=pick_python)
lib_menu.add_command(label="C++", command=pick_cpp)
lib_menu.add_command(label="STL", command=pick_stl)

hlp_menu = tk.Menu()
hlp_menu.add_command(label="О программе", command=about)

m_menu = tk.Menu()
m_menu.add_cascade(label="Библиотеки", menu=lib_menu)
m_menu.add_cascade(label="Справка", menu=hlp_menu)

win.config(menu=m_menu)

lbl_mod = tk.Label(win, text="Модуль не выбран", font=("Arial", 12, "bold"))
lbl_mod.pack(pady=10)

frm_in = tk.LabelFrame(win, text="Ввод данных", font=("Arial", 10, "bold"))
frm_in.pack(pady=10, padx=20, fill="x")

frm_num = tk.Frame(frm_in)
frm_num.pack(pady=5, fill="x")
lbl_num = tk.Label(frm_num, text="Целое число:", width=25, anchor="w")
lbl_num.pack(side=tk.LEFT, padx=5)
ent_num = tk.Entry(frm_num, width=20)
ent_num.pack(side=tk.LEFT, padx=5)

frm_txt = tk.Frame(frm_in)
frm_txt.pack(pady=5, fill="x")
lbl_txt = tk.Label(frm_txt, text="Строка (макс 9 символов):", width=25, anchor="w")
lbl_txt.pack(side=tk.LEFT, padx=5)
ent_txt = tk.Entry(frm_txt, width=20)
ent_txt.pack(side=tk.LEFT, padx=5)

frm_btn = tk.LabelFrame(win, text="Операции", font=("Arial", 10, "bold"))
frm_btn.pack(pady=10, padx=20, fill="x")

b1 = tk.Button(frm_btn, text="Push_back", command=btn_push_back, width=12)
b1.grid(row=0, column=0, padx=10, pady=10)

b2 = tk.Button(frm_btn, text="Push_front", command=btn_push_front, width=12)
b2.grid(row=0, column=1, padx=10, pady=10)

b3 = tk.Button(frm_btn, text="Pop_back", command=btn_pop_back, width=12)
b3.grid(row=0, column=2, padx=10, pady=10)

b4 = tk.Button(frm_btn, text="Pop_front", command=btn_pop_front, width=12)
b4.grid(row=0, column=3, padx=10, pady=10)

b5 = tk.Button(frm_btn, text="Очистить", command=btn_clear, width=54)
b5.grid(row=1, column=0, columnspan=4, pady=10)

lbl_out = tk.Label(win, text="Результат:", font=("Arial", 10, "bold"))
lbl_out.pack(pady=(10, 5))

txt_out = tk.Text(win, height=12, width=70)
txt_out.pack(pady=5, padx=20, fill="both", expand=True)

refresh()

win.mainloop()