import numpy as np
import matplotlib.pyplot as plt

def campo_magnetico(Nb, Ic, Lb, mu_0):
    return float((mu_0 * Nb * Ic) / (Lb))

def fluxo_magnetico(B, A, theta):
    return B * A * np.cos(theta)

def forca_eletromotriz(N, B, A, theta):
    dfluxo_dt = N * B * A * np.sin(theta)
    return float(N * dfluxo_dt)

def bobina(area_do_fio, comprimento_do_fio, resistividade_do_fio):
    resistencia = float(comprimento_do_fio) / (resistividade_do_fio * area_do_fio)
    return resistencia

def calcular_bobina(Nb, Lb, tensao_aplicada, area_do_fio, comprimento_do_fio, resistividade_do_fio, velocidade_angular_inicial, velocidade_angular_final, tempo):
    # Resistencia
    resistencia = bobina(area_do_fio, comprimento_do_fio, resistividade_do_fio)

    # Area da bobina 
    r = Lb / (2 * np.pi)  
    A = np.pi * r**2  

    # Constante magnética
    mu_0 = 4 * np.pi * 10**-7

    # Velocidade angular 
    velocidade_angular = np.linspace(np.radians(velocidade_angular_inicial), np.radians(velocidade_angular_final), len(tempo))

    # Inicializando listas para os resultados dinâmicos
    B_dinamico = []
    fluxo_dinamico = []
    fem_dinamica = []

    for t, omega in zip(tempo, velocidade_angular):
        # Ângulo no instante t
        theta = omega / t

        # Corrente e Campo Magnético
        Ic = tensao_aplicada / resistencia
        B = campo_magnetico(Nb, Ic, Lb, mu_0)
        B_dinamico.append(B)

        # Fluxo Magnético
        fluxo = fluxo_magnetico(B, A, theta)
        fluxo_dinamico.append(fluxo)

        # Força Eletromotriz
        fem = forca_eletromotriz(Nb, B, A, theta)
        fem_dinamica.append(fem)

    return np.array(B_dinamico), np.array(fluxo_dinamico), np.array(fem_dinamica), velocidade_angular

# Exemplo de parâmetros definidos pelo aluno
Nb = 1000  # Número de espiras da bobina
tensao_aplicada = 20.0  # Tensão aplicada (em Volts)
area_do_fio = 5.3476 * 10 ** -5  # Área do fio em metros quadrados (53.476 mm²)
comprimento_do_fio = 25.9  # Comprimento do fio para 1000 voltas
resistividade_do_fio = 1.68 * 10 ** -8  # Resistividade do fio de cobre (em Ohm.m)
velocidade_angular_inicial = 60.0  # Velocidade angular inicial em graus/s
velocidade_angular_final = 90.0  # Velocidade angular final em graus/s
tempo = np.linspace(0, 1, 1000)  # Tempo de 0 a 1 segundo
Lb = 2.0  # Comprimento da bobina (em metros)


# Cálculo
campo_magnetico_dinamico, fluxo_magnetico_dinamico, fem_dinamica, velocidades_angular = calcular_bobina(
    Nb, Lb, tensao_aplicada, area_do_fio, comprimento_do_fio, resistividade_do_fio,
    velocidade_angular_inicial, velocidade_angular_final, tempo
)


# Gráficos
plt.figure(figsize=(14, 8))

# Gráfico do Campo Magnético
plt.subplot(3, 1, 1)
plt.plot(velocidades_angular, campo_magnetico_dinamico, label="Campo Magnético (B)", color="blue")
plt.xlabel("Velocidade Angular (rad/s)")
plt.ylabel("Campo Magnético (T)")
plt.title("Campo Magnético X Velocidade Angular")
plt.legend()
plt.grid(True)

# Gráfico do Fluxo Magnético
plt.subplot(3, 1, 2)
plt.plot(velocidades_angular, fluxo_magnetico_dinamico, label="Fluxo Magnético (Φ)", color="green")
plt.xlabel("Velocidade Angular (rad/s)")
plt.ylabel("Fluxo Magnético (Wb)")
plt.title("Fluxo Magnético X Velocidade Angular")
plt.legend()
plt.grid(True)

# Gráfico da Força Eletromotriz
plt.subplot(3, 1, 3)
plt.plot(velocidades_angular, fem_dinamica, label="Força Eletromotriz (EMF)", color="red")
plt.xlabel("Velocidade Angular (rad/s)")
plt.ylabel("Força Eletromotriz (V)")
plt.title("Força Eletromotriz X Velocidade Angular")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()