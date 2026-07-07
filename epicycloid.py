import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox, CheckButtons, Button
from fractions import Fraction


class Epicycloid:
    def __init__(self, title: str):
        self._R = 10
        self._k = 3.0
        self._r = self._R / self._k
        self._need_anims = True

        self._x_path = None
        self._y_path = None
        self._phi_values = None
        self._frames = None
        self._compute_path(self._k)

        self._ani = None

        plt.rcParams['toolbar'] = 'None'

        self._figure, self._axes = plt.subplots(figsize=(8, 8))

        self._figure.canvas.manager.set_window_title(title)
        self._figure.canvas.window().setMinimumSize(650, 650)
        self._figure.tight_layout(pad=1)
        self._axes.set_aspect('equal')
        self._axes.grid(True, linestyle='--', alpha=0.5)

        self._init_ui()
        self._init_objects()
        self._set_limits()
        self._restart_animation()

    def _compute_path(self, k: float):
        r = self._R / k
        period = Fraction(k + 1).limit_denominator(1000).denominator
        total_angle = 2 * np.pi * period
        step = 500 * period
        self._phi_values = np.linspace(0, total_angle, step)
        self._x_path = r * ((k + 1) * np.cos(self._phi_values) - np.cos(self._phi_values * (k + 1)))
        self._y_path = r * ((k + 1) * np.sin(self._phi_values) - np.sin(self._phi_values * (k + 1)))
        self._r = r

        frame_step = max(1, len(self._phi_values) // 250)
        self._frames = list(range(0, len(self._phi_values), frame_step))
        if self._frames[-1] != len(self._phi_values) - 1:
            self._frames.append(len(self._phi_values) - 1)

    def _set_limits(self):
        lim = self._R + 2 * self._r + 5
        self._axes.set_xlim(-lim, lim)
        self._axes.set_ylim(-lim, lim)

    def _init_ui(self):
        ax_textbox = self._axes.inset_axes((0.06, 0.96, 0.17, 0.03))
        self._k_txbx = TextBox(ax_textbox, 'k =', str(self._k), textalignment='center')
        self._k_txbx.on_submit(self._on_k_submit)

        ax_checkbox = self._axes.inset_axes((0.06, 0.92, 0.17, 0.03))
        self._need_anims_chbx = CheckButtons(
            ax_checkbox,
            ['Анимация'], [self._need_anims],
            frame_props={'sizes': [60]}
        )
        self._need_anims_chbx.on_clicked(self._on_need_anims_click)

        ax_button = self._axes.inset_axes((0.06, 0.88, 0.17, 0.03))
        self._as_img_btn = Button(ax_button, 'Скачать')
        self._as_img_btn.on_clicked(self._on_as_img_click)

    def _init_objects(self):
        self._blue_circle = plt.Circle((0, 0), self._R, color='blue', fill=False, linewidth=3)
        self._axes.add_patch(self._blue_circle)

        self._green_circle = plt.Circle((self._R + self._r, 0), self._r, color='green', fill=False, linewidth=2)
        self._axes.add_patch(self._green_circle)

        self._radius = plt.Line2D((self._R, self._R + self._r), (0, 0), color='green')
        self._axes.add_line(self._radius)

        self._point_A = self._axes.plot([0], [0], 'bo', markersize=5)[0]
        self._point_B = self._axes.plot([], [], 'ro', markersize=5)[0]
        self._point_C = self._axes.plot([], [], 'go', markersize=5)[0]

        self._red_line = self._axes.plot([], [], color='red', linewidth=2.5)[0]

    def _reset_graph(self):
        self._red_line.set_data([], [])

        k = self._k
        r = self._r
        phi0 = self._phi_values[0]
        cx = r * (k + 1) * np.cos(phi0)
        cy = r * (k + 1) * np.sin(phi0)
        self._green_circle.center = (cx, cy)
        self._point_C.set_data([cx], [cy])
        bx, by = self._x_path[0], self._y_path[0]
        self._radius.set_data([bx, cx], [by, cy])
        self._point_B.set_data([bx], [by])

        self._figure.canvas.draw_idle()

    def _restart_animation(self):
        if self._ani is not None:
            self._ani.event_source.stop()
            self._ani = None

        self._reset_graph()

        self._ani = FuncAnimation(
            self._figure, self._update_graph,
            frames=len(self._frames),
            interval=10,
            repeat=True,
            repeat_delay=2500,
            cache_frame_data=False
        )

    def _on_k_submit(self, value):
        try:
            value = float(value)
            if value <= 0:
                raise ValueError
        except ValueError:
            self._k_txbx.set_val(str(self._k))
            return

        self._k = value
        self._compute_path(value)
        self._set_limits()
        self._green_circle.set_radius(self._r)

        if not self._need_anims:
            self._red_line.set_data(self._x_path, self._y_path)
        else:
            self._restart_animation()

    def _on_need_anims_click(self, _value):
        self._need_anims = not self._need_anims

        self._green_circle.set_visible(self._need_anims)
        self._blue_circle.set_visible(self._need_anims)
        self._radius.set_visible(self._need_anims)
        self._point_A.set_visible(self._need_anims)
        self._point_B.set_visible(self._need_anims)
        self._point_C.set_visible(self._need_anims)

        if self._need_anims:
            self._restart_animation()
        else:
            if self._ani is not None:
                self._ani.event_source.stop()
                self._ani = None

            self._red_line.set_data(self._x_path, self._y_path)
            self._figure.canvas.draw_idle()

    def _on_as_img_click(self, _value):
        fig, ax = plt.subplots(figsize=(5, 5))

        ax.set_title(f'Эпициклоида с k = {self._k}')
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.plot(self._x_path, self._y_path, 'red', linewidth=2.5)

        lim = self._R + 2 * self._r + 5
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)

        from datetime import datetime
        filename = f'epicycloid_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.png'
        fig.savefig(filename, bbox_inches='tight')
        plt.close(fig)

    def _update_graph(self, frame):
        idx = self._frames[frame]
        phi_current = self._phi_values[idx]
        k = self._k
        r = self._r

        cx = r * (k + 1) * np.cos(phi_current)
        cy = r * (k + 1) * np.sin(phi_current)
        self._green_circle.center = (cx, cy)
        self._point_C.set_data([cx], [cy])

        bx, by = self._x_path[idx], self._y_path[idx]
        self._radius.set_data([bx, cx], [by, cy])
        self._point_B.set_data([bx], [by])

        self._red_line.set_data(self._x_path[:idx + 1], self._y_path[:idx + 1])

        return self._red_line, self._green_circle, self._radius, self._point_B, self._point_C

    @staticmethod
    def show():
        plt.show()


if __name__ == '__main__':
    main = Epicycloid('Учебная практика №1')
    main.show()
