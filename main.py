import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import filedialog


def newton(n, k):
    """Oblicza wartość dwumianu Newtona.

    Args:
        n (int): Liczba całkowita dodatnia.
        k (int): Liczba całkowita dodatnia mniejsza lub równa n.

    Returns:
        int: Wynik dwumianu Newtona dla danych wartości n i k.
    """
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def bernstein_polynomial(i, n, t):
    """Oblicza wartość wielomianu Bernsteina.

    Args:
        i (int): Indeks.
        n (int): Stopień wielomianu.
        t (float): Wartość zmiennej.

    Returns:
        float: Wartość wielomianu Bernsteina dla danych wartości i, n i t.
    """
    return newton(n, i) * (t ** (n - i)) * (1 - t) ** i


def bezier_surface(control_points, resolution=5):
    """Generuje powierzchnię Béziera na podstawie punktów kontrolnych.

    Args:
        control_points (numpy.ndarray): Tablica punktów kontrolnych.
        resolution (int, optional): Rozdzielczość powierzchni. Domyślnie 5.

    Returns:
        numpy.ndarray: Powierzchnia Béziera.
    """
    n, m, _ = control_points.shape
    n -= 1
    m -= 1
    u = np.linspace(0, 1, resolution)
    v = np.linspace(0, 1, resolution)
    U, V = np.meshgrid(u, v)
    B_u = np.array([bernstein_polynomial(i, n, U) for i in range(n + 1)])
    B_v = np.array([bernstein_polynomial(j, m, V) for j in range(m + 1)])
    surface = np.zeros((resolution, resolution, 3))
    for i in range(n + 1):
        for j in range(m + 1):
            surface += (B_u[i, :, :] * B_v[j, :, :])[:, :, np.newaxis] * control_points[i, j]
    return surface


# Pliki z punktami kontrolnymi (bez rozszerzenia)
files = ['teapot', 'spoon', 'teacup']


def load_and_draw(file_index):
    """Wczytuje plik i rysuje powierzchnię Béziera."""
    if file_index < len(files):
        file_name = files[file_index]
        draw_surface(read_txt_file(f'{file_name}.txt'))
    else:
        load_custom_file()


def read_txt_file(file_path):
    """Wczytuje plik tekstowy i zwraca listę punktów kontrolnych."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    control_points_list = []
    control_points = []
    for line in lines:
        points = list(map(float, line.split()))
        if len(points) == 3:
            control_points.append(points)
            if len(control_points) == 16:
                control_points_list.append(np.array(control_points).reshape((4, 4, 3)))
                control_points = []
    return control_points_list


def create_gui():
    """Tworzy interfejs użytkownika."""
    root = tk.Tk()
    root.title("Wybierz plik")
    root.geometry("300x200")

    label = tk.Label(root, text="Wybierz plik:")
    label.pack(pady=10)

    for file_name in files:
        button = tk.Button(root, text=file_name.capitalize(),
                           command=lambda file_name=file_name: load_and_draw(files.index(file_name)))
        button.pack()

    custom_button = tk.Button(root, text="Inny plik", command=load_custom_file)
    custom_button.pack()

    root.mainloop()


def load_custom_file():
    """Wczytuje plik z zewnątrz."""
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        draw_surface(read_txt_file(file_path))


def draw_surface(control_points_list):
    """Rysuje powierzchnie Béziera."""
    plt.close()  # Zamknięcie poprzedniego okna, jeśli istnieje
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    for i, control_points in enumerate(control_points_list):
        surface = bezier_surface(control_points)
        ax.plot_surface(surface[:, :, 0], surface[:, :, 1], surface[:, :, 2], alpha=0.6)
        plt.gca().set_xlim([-2.2, 2.2])
        plt.gca().set_ylim([-2.2, 2.2])
        plt.gca().set_zlim([-2.2, 2.2])
    plt.show()


# Uruchomienie GUI
create_gui()
