import tkinter as tk
import random
import threading
import time

# CLASE SENSOR
class Sensor:
    def __init__(self):
        self.temperatura = 0
        self.humedad = 0

    def generar_datos(self):
        self.temperatura = random.uniform(0, 50)
        self.humedad = random.uniform(20, 90)
        return self.temperatura, self.humedad

    def simular_lecturas(self, interfaz):
        try:
            while True:
                temperatura, humedad = self.generar_datos()
                interfaz.actualizar_datos(temperatura, humedad)
                time.sleep(1)
        except Exception as e:
            print(f"Error al generar datos: {e}")
        finally:
            print("Simulación finalizada")

# CLASE INTERFAZ
class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Monitoreo Ambiental")
        self.root.geometry("400x300")
        self.root.configure(bg="#f2f2f2")

        # Frame principal
        main_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="groove", borderwidth=2)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Etiquetas de temperatura y humedad
        self.label_temp = tk.Label(main_frame, text="Temperatura: --°C", font=("Arial", 14), bg="#ffffff")
        self.label_temp.pack(pady=5)

        self.label_humedad = tk.Label(main_frame, text="Humedad: --%", font=("Arial", 14), bg="#ffffff")
        self.label_humedad.pack(pady=5)

        # Entrada para umbral
        tk.Label(main_frame, text="Ingrese umbral de temperatura (°C):", bg="#ffffff", font=("Arial", 10)).pack(pady=(10, 0))
        self.umbral_entry = tk.Entry(main_frame, font=("Arial", 12), justify="center")
        self.umbral_entry.pack(pady=5)

        # Botón para configurar umbral
        self.btn_configurar = tk.Button(main_frame, text="Configurar Umbral", command=self.configurar_umbral,
                                        bg="#4da6ff", fg="white", font=("Arial", 12), relief="raised")
        self.btn_configurar.pack(pady=10)

        # Estado de alerta
        self.label_estado = tk.Label(main_frame, text="Estado: Normal", font=("Arial", 12), bg="#e6ffe6", fg="green", width=25)
        self.label_estado.pack(pady=10)

        self.umbral_temp = None

    def actualizar_datos(self, temperatura, humedad):
        self.label_temp.config(text=f"Temperatura: {temperatura:.2f}°C")
        self.label_humedad.config(text=f"Humedad: {humedad:.2f}%")

        if self.umbral_temp is not None and temperatura > self.umbral_temp:
            self.label_estado.config(text="Estado: ¡Alerta!", bg="#ffe6e6", fg="red")
        else:
            self.label_estado.config(text="Estado: Normal", bg="#e6ffe6", fg="green")

    def configurar_umbral(self):
        try:
            umbral = float(self.umbral_entry.get())
            self.umbral_temp = umbral
        except ValueError:
            self.label_estado.config(text="Error: Umbral no válido", bg="#ffe6e6", fg="red")
        else:
            self.label_estado.config(text="Umbral configurado correctamente", bg="#e6ffe6", fg="green")

# MAIN
def iniciar_simulacion():
    root = tk.Tk()
    interfaz = Interfaz(root)
    sensor = Sensor()

    threading.Thread(target=sensor.simular_lecturas, args=(interfaz,), daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    iniciar_simulacion()
