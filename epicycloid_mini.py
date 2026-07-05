import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction


k = float(input('Введите k: '))
R = 10
r = R / k

total_angle = 2 * np.pi * Fraction(k).limit_denominator().denominator
theta_values = np.linspace(0, total_angle, 10000)
x_path = r * ((k + 1) * np.cos(theta_values) - np.cos(theta_values * (k + 1)))
y_path = r * ((k + 1) * np.sin(theta_values) - np.sin(theta_values * (k + 1)))

plt.figure(figsize=(4, 4))
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(-(R + 2 * r + 5), R + 2 * r + 5)
plt.ylim(-(R + 2 * r + 5), R + 2 * r + 5)
plt.axis('scaled')

plt.plot(x_path, y_path, color='red', linewidth=2)

if input('Нужно ли сохранить как изображение? (д/н) ').lower() == 'д':
    from datetime import datetime
    filename = f'epicycloid_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.png'
    plt.savefig(filename, bbox_inches='tight')

plt.show()
