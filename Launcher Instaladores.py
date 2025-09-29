
import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
import shutil
import subprocess

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXEC_DIR = os.path.join(BASE_DIR, "executables")
JSON_FILE = os.path.join(BASE_DIR, "apps.json")

# ---------- Funciones ----------
def load_apps():
    if not os.path.exists(JSON_FILE):
        return {"apps": []}
    with open(JSON_FILE, "r") as f:
        return json.load(f)

def save_apps(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def refresh_list():
    listbox.configure(state="normal")
    listbox.delete("1.0", ctk.END)
    for idx, app in enumerate(apps_data["apps"], start=1):
        listbox.insert(ctk.END, f"{idx}. {app['name']}\n")
    listbox.configure(state="disabled")

def run_selected():
    try:
        line_index = listbox.index("insert linestart")
        line_num = int(line_index.split(".")[0]) - 1
        if line_num < 0 or line_num >= len(apps_data["apps"]):
            return
        app = apps_data["apps"][line_num]
        subprocess.Popen(os.path.abspath(app["path"]), shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar:\n{e}")

def add_app():
    file_path = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe")])
    if not file_path:
        return
    file_name = os.path.basename(file_path)
    dest_path = os.path.join(EXEC_DIR, file_name)

    shutil.copy(file_path, dest_path)
    apps_data["apps"].append({"name": file_name, "path": dest_path})
    save_apps(apps_data)
    refresh_list()

def delete_app():
    try:
        line_index = listbox.index("insert linestart")
        line_num = int(line_index.split(".")[0]) - 1
        if line_num < 0 or line_num >= len(apps_data["apps"]):
            return
        app = apps_data["apps"][line_num]

        if os.path.exists(app["path"]):
            os.remove(app["path"])
        del apps_data["apps"][line_num]
        save_apps(apps_data)
        refresh_list()
    except:
        pass

def run_all_sequentially():
    for app in apps_data["apps"]:
        try:
            absolute_path = os.path.abspath(app["path"])
            process = subprocess.Popen(absolute_path, shell=True)
            process.wait()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar {app['name']}:\n{e}")

# ---------- MAIN ----------
if not os.path.exists(EXEC_DIR):
    os.makedirs(EXEC_DIR)

apps_data = load_apps()

ctk.set_appearance_mode("system")  # "light", "dark", "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

root = ctk.CTk()
root.title("Launcher Portable")
root.geometry("400x450")

frame = ctk.CTkFrame(root, corner_radius=15)
frame.pack(padx=20, pady=20, fill="both", expand=True)

label = ctk.CTkLabel(frame, text="Aplicaciones", font=("Arial", 18, "bold"))
label.pack(pady=10)

listbox = ctk.CTkTextbox(frame, width=320, height=150, state="disabled")
listbox.pack(pady=10, fill="x")

btn_run_all = ctk.CTkButton(frame, text="▶ Ejecutar todo", command=run_all_sequentially,fg_color="#228B22", hover_color="#006400")
btn_run_all.pack(pady=5, fill="x")

btn_run = ctk.CTkButton(frame, text="▶ Ejecutar seleccionado", command=run_selected)
btn_run.pack(pady=5, fill="x")

btn_add = ctk.CTkButton(frame, text="➕ Agregar ejecutable", command=add_app)
btn_add.pack(pady=5, fill="x")

btn_del = ctk.CTkButton(frame, text="🗑 Eliminar seleccionado", fg_color="red", hover_color="#b22222", command=delete_app)
btn_del.pack(pady=5, fill="x")

refresh_list()
root.mainloop()

