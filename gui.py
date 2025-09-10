from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from generators import middle_square, mult_congruential, numpy_rng
from tests import test_mean_uniform, test_variance_uniform, chi_square_uniform
from utils import export_csv, save_histogram

matplotlib.use("TkAgg")

class App(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master = master
        self.master.title("SimToolkit – Calculadora de Pruebas")
        self.master.geometry("980x680")
        self.pack(fill="both", expand=True)

        self.current_data = None  # últimos U(0,1) generados (np.ndarray)
        self._make_menu()
        self._make_tabs()

    def _make_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exportar datos...", command=self._export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.master.destroy)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Acerca de", command=self._about)
        menubar.add_cascade(label="Ayuda", menu=help_menu)

    def _about(self):
        messagebox.showinfo("Acerca de", "SimToolkit – Calculadora de Pruebas\nCuadrados Medios y Multiplicador\nPruebas: Media, Varianza, Chi²")

    def _make_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.tab_gen = ttk.Frame(notebook)
        self.tab_tests = ttk.Frame(notebook)
        self.tab_vars = ttk.Frame(notebook)

        notebook.add(self.tab_gen, text="Generadores")
        notebook.add(self.tab_tests, text="Pruebas")
        notebook.add(self.tab_vars, text="Variables")

        self._build_generators_tab(self.tab_gen)
        self._build_tests_tab(self.tab_tests)
        self._build_variables_tab(self.tab_vars)

    def _build_generators_tab(self, parent):
        frm = ttk.Frame(parent, padding=10)
        frm.pack(fill="both", expand=True)

        left = ttk.Frame(frm)
        left.pack(side="left", fill="y", padx=6, pady=6)

        ttk.Label(left, text="Algoritmo:").grid(row=0, column=0, sticky="w")
        self.gen_choice = tk.StringVar(value="middle")
        ttk.Radiobutton(left, text="Cuadrados Medios", variable=self.gen_choice, value="middle").grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(left, text="Multiplicador Constante", variable=self.gen_choice, value="mult").grid(row=2, column=0, sticky="w")
        ttk.Radiobutton(left, text="NumPy (benchmark)", variable=self.gen_choice, value="numpy").grid(row=3, column=0, sticky="w")

        ttk.Label(left, text="n (muestras)").grid(row=4, column=0, sticky="w", pady=(8,0))
        self.var_n = tk.StringVar(value="1000")
        ttk.Entry(left, textvariable=self.var_n, width=12).grid(row=5, column=0, sticky="w", pady=2)

        ttk.Label(left, text="semilla").grid(row=6, column=0, sticky="w", pady=(8,0))
        self.var_seed = tk.StringVar(value="12345678")
        ttk.Entry(left, textvariable=self.var_seed, width=18).grid(row=7, column=0, sticky="w", pady=2)

        ttk.Label(left, text="Parámetro a (mult)").grid(row=8, column=0, sticky="w", pady=(8,0))
        self.var_a = tk.StringVar(value="1664525")
        ttk.Entry(left, textvariable=self.var_a, width=18).grid(row=9, column=0, sticky="w", pady=2)

        ttk.Label(left, text="m (mult)").grid(row=10, column=0, sticky="w", pady=(8,0))
        self.var_m = tk.StringVar(value=str(2**32))
        ttk.Entry(left, textvariable=self.var_m, width=18).grid(row=11, column=0, sticky="w", pady=2)

        ttk.Label(left, text="Width (digits) - middle").grid(row=12, column=0, sticky="w", pady=(8,0))
        self.var_width = tk.StringVar(value="8")
        ttk.Entry(left, textvariable=self.var_width, width=12).grid(row=13, column=0, sticky="w", pady=2)

        btn_frame = ttk.Frame(left)
        btn_frame.grid(row=14, column=0, pady=10)
        ttk.Button(btn_frame, text="Generar", command=self._on_generate).pack(side="left")
        ttk.Button(btn_frame, text="Exportar datos", command=self._export_data).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Exportar histograma", command=self._export_hist).pack(side="left", padx=6)

        right = ttk.Frame(frm)
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)
        self.fig_gen, self.ax_gen = plt.subplots(figsize=(6,5), dpi=100)
        self.canvas_gen = FigureCanvasTkAgg(self.fig_gen, master=right)
        self.canvas_gen.get_tk_widget().pack(fill="both", expand=True)
        self.lbl_status = ttk.Label(right, text="Listo.")
        self.lbl_status.pack(anchor="w", pady=4)

    def _on_generate(self):
        try:
            n = int(self.var_n.get())
            seed = int(self.var_seed.get())
            choice = self.gen_choice.get()
            if n <= 0:
                raise ValueError("n debe ser positivo.")
            if choice == "middle":
                width = int(self.var_width.get())
                data = middle_square(seed=seed, n=n, width=width)
            elif choice == "mult":
                a = int(self.var_a.get())
                m = int(self.var_m.get())
                data = mult_congruential(seed=seed, a=a, m=m, n=n)
            else:
                data = numpy_rng(seed=seed, n=n)

            self.current_data = data
            self._draw_hist(self.ax_gen, data, "Histograma U(0,1) - Generador")
            self.canvas_gen.draw()
            self.lbl_status.config(text=f"Generadas {len(data)} muestras.")
        except Exception as e:
            messagebox.showerror("Error al generar", str(e))

    def _build_tests_tab(self, parent):
        frm = ttk.Frame(parent, padding=10)
        frm.pack(fill="both", expand=True)

        top = ttk.Frame(frm)
        top.pack(fill="x", pady=4)

        ttk.Label(top, text="Prueba:").grid(row=0, column=0, sticky="w")
        self.test_choice = tk.StringVar(value="mean")
        ttk.Radiobutton(top, text="Media", variable=self.test_choice, value="mean").grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(top, text="Varianza", variable=self.test_choice, value="variance").grid(row=2, column=0, sticky="w")
        ttk.Radiobutton(top, text="Chi²", variable=self.test_choice, value="chi2").grid(row=3, column=0, sticky="w")

        ttk.Label(top, text="k (Chi²)").grid(row=0, column=1, sticky="w")
        self.var_k = tk.StringVar(value="10")
        ttk.Entry(top, textvariable=self.var_k, width=10).grid(row=1, column=1, sticky="w", padx=6)

        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=6)
        ttk.Button(btn_frame, text="Probar", command=self._on_probar).pack(side="left")
        ttk.Button(btn_frame, text="Exportar resultados", command=self._export_results).pack(side="left", padx=6)

        self.txt_results = tk.Text(frm, height=8)
        self.txt_results.pack(fill="x", pady=4)
        self.fig_test, self.ax_test = plt.subplots(figsize=(6,4), dpi=100)
        self.canvas_test = FigureCanvasTkAgg(self.fig_test, master=frm)
        self.canvas_test.get_tk_widget().pack(fill="both", expand=True, pady=4)

    def _on_probar(self):
        try:
            if self.current_data is None:
                raise ValueError("Primero genere datos en la pestaña Generadores.")
            choice = self.test_choice.get()
            if choice == "mean":
                res = test_mean_uniform(self.current_data)
                text = f"Prueba de Medias:\nMedia muestral = {res.mean:.6f} (esperada {res.expected})\nEstadístico Z ≈ {res.statistic_z:.4f} (n={res.n})"
                self._set_results(text)
            elif choice == "variance":
                res = test_variance_uniform(self.current_data)
                text = f"Prueba de Varianza:\nVarianza muestral = {res.variance:.6f} (esperada {res.expected:.6f})\nEstadístico Chi² ≈ {res.chi2_stat:.4f} (n={res.n})"
                self._set_results(text)
            else:
                k = int(self.var_k.get())
                res = chi_square_uniform(self.current_data, k=k)
                lines = [f"Chi² = {res.statistic:.6f} con k={res.k}", "Intervalo\tObs\tExp"]
                for i in range(len(res.observed)):
                    a = res.bins[i]
                    b = res.bins[i+1]
                    lines.append(f"[{a:.3f}, {b:.3f})\t{int(res.observed[i])}\t{res.expected[i]:.2f}")
                self._set_results("\n".join(lines))
                self._draw_hist(self.ax_test, self.current_data, f"Histograma para Chi² (k={k})", bins=k)
                self.canvas_test.draw()
            if choice in ("mean", "variance"):
                self._draw_hist(self.ax_test, self.current_data, "Histograma para prueba", bins=20)
                self.canvas_test.draw()
        except Exception as e:
            messagebox.showerror("Error en prueba", str(e))

    def _build_variables_tab(self, parent):
        frm = ttk.Frame(parent, padding=10)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Variables auxiliares / Export").pack(anchor="w")
        ttk.Button(frm, text="Exportar datos actuales", command=self._export_data).pack(pady=6)
        ttk.Button(frm, text="Exportar histograma actual", command=self._export_hist).pack(pady=6)

    def _draw_hist(self, ax, data, title: str, bins: int | None = None):
        ax.clear()
        ax.hist(data, bins=(bins or 20), edgecolor="black")
        ax.set_title(title)
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")

    def _set_results(self, text: str):
        self.txt_results.delete("1.0", tk.END)
        self.txt_results.insert(tk.END, text)

    def _export_data(self):
        try:
            if self.current_data is None:
                raise ValueError("No hay datos generados aún.")
            path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], title="Guardar datos")
            if not path:
                return
            export_csv(self.current_data, path)
            messagebox.showinfo("Exportar", f"Datos guardados en:\n{path}")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))

    def _export_hist(self):
        try:
            if self.current_data is None:
                raise ValueError("No hay datos generados aún.")
            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png")], title="Guardar histograma")
            if not path:
                return
            save_histogram(self.current_data, path, bins=20, title="Histograma")
            messagebox.showinfo("Exportar", f"Histograma guardado en:\n{path}")
        except Exception as e:
            messagebox.showerror("Error al exportar histograma", str(e))

    def _export_results(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text","*.txt")], title="Guardar resultados")
            if not path:
                return
            text = self.txt_results.get("1.0", tk.END)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Exportar", f"Resultados guardados en:\n{path}")
        except Exception as e:
            messagebox.showerror("Error al exportar resultados", str(e))

def launch_app():
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    App(root)
    root.mainloop()
