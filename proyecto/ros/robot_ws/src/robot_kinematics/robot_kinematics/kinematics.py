#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math

class Robot():
  # Actualizamos las medidas a las que definió tu equipo: 0.2, 0.3, 0.5
  def __init__(self, l=(0.2, 0.3, 0.5)):
    self.l = l
    self.dt = 0.0

  def def_tray(self, t_f=2.0, frec=15.0, 
               th_i=(0.1, 0.1, 0.1), 
               xi_f=(0.6, 0.1, 0.0)):
    self.dt = 1.0 / frec
    self.muestras = int(t_f * frec + 1)
    
    x, y, z = xi_f
    l0, l1, l2 = self.l
    
    # 1. Cinemática Inversa Analítica Trigonométrica (¡A prueba de fallos!)
    # Ángulo de la base (paneo)
    th1_f = math.atan2(y, x)
    
    # Distancia en el plano del brazo
    r = math.sqrt(x**2 + y**2)
    s = z - l0 # Altura respecto a la base del hombro
    
    # Ecuación del codo (Cálculo de hipotenusa y ley de cosenos)
    D = (r**2 + s**2 - l1**2 - l2**2) / (2 * l1 * l2)
    # Protegemos la matemática por si el usuario hace clic fuera del alcance máximo
    D = max(min(D, 1.0), -1.0) 
    
    # Ángulo del codo (Configuración de "codo arriba" con el signo negativo)
    th3_f = math.atan2(-math.sqrt(1 - D**2), D)
    
    # Ángulo del hombro
    alpha = math.atan2(s, r)
    beta = math.atan2(l2 * math.sin(th3_f), l1 + l2 * math.cos(th3_f))
    th2_f = alpha - beta
    
    # 2. Generación de Trayectoria Suave en Espacio de Juntas
    self.t_m = np.zeros((1, self.muestras))
    self.th_m = np.zeros((3, self.muestras))
    self.xi_m = np.zeros((3, self.muestras))
    
    th_start = np.array(th_i)
    th_end = np.array([th1_f, th2_f, th3_f])
    
    for i in range(self.muestras):
        t = i * self.dt
        self.t_m[0, i] = t
        
        # Perfil de velocidad polinomial suave (curva en S)
        tau = t / t_f
        s_t = 10 * tau**3 - 15 * tau**4 + 6 * tau**5
        
        # Interpolar los motores directamente hacia el objetivo
        th_act = th_start + (th_end - th_start) * s_t
        self.th_m[:, i] = th_act
        
        # Cinemática Directa (Para que las gráficas y logs muestren dónde está la punta)
        r_act = l1 * math.cos(th_act[1]) + l2 * math.cos(th_act[1] + th_act[2])
        z_act = l0 + l1 * math.sin(th_act[1]) + l2 * math.sin(th_act[1] + th_act[2])
        x_act = r_act * math.cos(th_act[0])
        y_act = r_act * math.sin(th_act[0])
        
        self.xi_m[0, i] = x_act
        self.xi_m[1, i] = y_act
        self.xi_m[2, i] = z_act

  # Mantenemos las funciones vacías para que el publisher de tus compañeros no tire error al llamarlas
  def imp_tray(self):
    pass
    
  def imp_junt(self):
    pass
