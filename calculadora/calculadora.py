import tkinter as tk
from tkinter import messagebox

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("350x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#1C1C1C")
        
        self.expresion = ""
        
        self.crear_display()
        self.crear_botones()
    
    def crear_display(self):
        marco = tk.Frame(self.root, bg="#1C1C1C")
        marco.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="ew")
        
        self.display = tk.Entry(marco, font=("Segoe UI", 32), justify="right", 
                               bd=0, bg="#2D2D2D", fg="white", insertbackground="white")
        self.display.grid(row=0, column=0, ipadx=8, ipady=15, sticky="ew")
        marco.columnconfigure(0, weight=1)
    
    def crear_botones(self):
        estilos = {
            "numero": {"bg": "#3B3B3B", "fg": "white", "activebackground": "#505050"},
            "operador": {"bg": "#FF9500", "fg": "white", "activebackground": "#FFB143"},
            "limpiar": {"bg": "#A5A5A5", "fg": "black", "activebackground": "#C5C5C5"},
            "igual": {"bg": "#FF9500", "fg": "white", "activebackground": "#FFB143"},
            "funcion": {"bg": "#2D2D2D", "fg": "white", "activebackground": "#404040"},
        }
        
        botones = [
            ("C", 1, 0, "limpiar", 2),
            ("⌫", 1, 2, "funcion", 1),
            ("÷", 1, 3, "operador", 1),
            ("%", 1, 4, "funcion", 1),
            
            ("7", 2, 0, "numero", 1),
            ("8", 2, 1, "numero", 1),
            ("9", 2, 2, "numero", 1),
            ("×", 2, 3, "operador", 1),
            ("+/-", 2, 4, "funcion", 1),
            
            ("4", 3, 0, "numero", 1),
            ("5", 3, 1, "numero", 1),
            ("6", 3, 2, "numero", 1),
            ("-", 3, 3, "operador", 1),
            (".", 3, 4, "numero", 1),
            
            ("1", 4, 0, "numero", 1),
            ("2", 4, 1, "numero", 1),
            ("3", 4, 2, "numero", 1),
            ("+", 4, 3, "operador", 1),
            
            ("0", 5, 0, "numero", 2),
            ("=", 5, 3, "igual", 2),
        ]
        
        for texto, fila, col, estilo, colspan in botones:
            btn = tk.Button(
                self.root, text=texto, font=("Segoe UI", 18),
                width=4, height=2, bd=0,
                **estilos[estilo],
                command=lambda t=texto: self.click(t)
            )
            btn.grid(row=fila, column=col, columnspan=colspan, padx=3, pady=3, sticky="nsew")
        
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.root.grid_columnconfigure(j, weight=1)
    
    def click(self, valor):
        if valor == "C":
            self.expresion = ""
            self.display.delete(0, tk.END)
        
        elif valor == "⌫":
            self.expresion = self.expresion[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expresion)
        
        elif valor == "+/-":
            if self.expresion:
                try:
                    if self.expresion.startswith("-"):
                        self.expresion = self.expresion[1:]
                    else:
                        self.expresion = "-" + self.expresion
                    self.display.delete(0, tk.END)
                    self.display.insert(0, self.expresion)
                except:
                    pass
        
        elif valor == "%":
            if self.expresion:
                try:
                    resultado = str(float(self.expresion) / 100)
                    self.expresion = resultado
                    self.display.delete(0, tk.END)
                    self.display.insert(0, resultado)
                except:
                    messagebox.showerror("Error", "Operación inválida")
        
        elif valor == "=":
            try:
                expresion = self.expresion.replace("×", "*").replace("÷", "/")
                resultado = str(eval(expresion))
                if resultado.endswith(".0"):
                    resultado = resultado[:-2]
                self.display.delete(0, tk.END)
                self.display.insert(0, resultado)
                self.expresion = resultado
            except ZeroDivisionError:
                messagebox.showerror("Error", "No se puede dividir entre cero")
                self.expresion = ""
                self.display.delete(0, tk.END)
            except Exception:
                messagebox.showerror("Error", "Expresión inválida")
                self.expresion = ""
                self.display.delete(0, tk.END)
        
        else:
            self.expresion += valor
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expresion)

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()
