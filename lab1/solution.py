import csv
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def configure_matplotlib_for_cyrillic() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [
        "DejaVu Sans",
        "Arial",
        "Liberation Sans",
        "Noto Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False


@dataclass
class ModelParams:
    g: float = 9.81
    alpha_deg: float = 45.0
    v0: float = 1.0
    x0: float = 0.0
    y0: float = 0.0
    c: float = 0.15
    s: float = 3.0
    rho_air: float = 1.225
    rho_cast_iron: float = 7200.0
    r_ball: float = 0.01

    @property
    def alpha_rad(self) -> float:
        return math.radians(self.alpha_deg)

    @property
    def beta(self) -> float:
        return self.c * self.s * self.rho_air / 2.0

    @property
    def mass(self) -> float:
        volume = 4.0 / 3.0 * math.pi * self.r_ball ** 3
        return self.rho_cast_iron * volume


def galileo_landing(alpha_rad: float, v0: float, g: float, x0: float, y0: float, n_points: int = 600) -> dict:
    cos_a = math.cos(alpha_rad)
    sin_a = math.sin(alpha_rad)
    if abs(cos_a) < 1e-12:
        raise ValueError("cos(alpha) слишком близок к нулю, формула y(x) неустойчива.")

    # y(t) = y0 + v0*sin(a)*t - g*t^2/2 = 0
    a_q = -0.5 * g
    b_q = v0 * sin_a
    c_q = y0
    disc = b_q * b_q - 4.0 * a_q * c_q
    if disc < 0:
        raise ValueError("Для заданных параметров нет реального времени падения.")

    sqrt_disc = math.sqrt(disc)
    t_candidates = [(-b_q + sqrt_disc) / (2.0 * a_q), (-b_q - sqrt_disc) / (2.0 * a_q)]
    t_land = max(t for t in t_candidates if t >= 0.0)

    t_vals = np.linspace(0.0, t_land, n_points)
    x_vals = x0 + v0 * cos_a * t_vals
    y_vals = y0 + v0 * sin_a * t_vals - 0.5 * g * t_vals * t_vals

    return {
        "t": t_vals,
        "x": x_vals,
        "y": y_vals,
        "t_land": float(t_land),
        "x_land": float(x_vals[-1]),
        "y_max": float(np.max(y_vals)),
    }


def newton_rhs(state: np.ndarray, params: dict) -> np.ndarray:
    x, y, u, w = state
    _ = x, y
    g = params["g"]
    beta = params["beta"]
    m = params["m"]

    speed = math.sqrt(u * u + w * w)
    du_dt = -(beta / m) * u * speed
    dw_dt = -g - (beta / m) * w * speed
    dx_dt = u
    dy_dt = w
    return np.array([dx_dt, dy_dt, du_dt, dw_dt], dtype=float)


def rk4_step(state: np.ndarray, dt: float, rhs, params: dict) -> np.ndarray:
    k1 = rhs(state, params)
    k2 = rhs(state + 0.5 * dt * k1, params)
    k3 = rhs(state + 0.5 * dt * k2, params)
    k4 = rhs(state + dt * k3, params)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def simulate_newton_rk4(
    alpha_rad: float,
    v0: float,
    x0: float,
    y0: float,
    g: float,
    beta: float,
    m: float,
    dt: float = 1e-3,
    t_max: float = 10.0,
) -> dict:
    u0 = v0 * math.cos(alpha_rad)
    w0 = v0 * math.sin(alpha_rad)

    state = np.array([x0, y0, u0, w0], dtype=float)
    params = {"g": g, "beta": beta, "m": m}

    t_vals = [0.0]
    x_vals = [x0]
    y_vals = [y0]
    u_vals = [u0]
    w_vals = [w0]

    t = 0.0
    landed = False
    t_land = None
    x_land = None

    while t < t_max:
        prev_t = t
        prev_state = state.copy()

        state = rk4_step(state, dt, newton_rhs, params)
        t += dt

        t_vals.append(t)
        x_vals.append(float(state[0]))
        y_vals.append(float(state[1]))
        u_vals.append(float(state[2]))
        w_vals.append(float(state[3]))

        if prev_t > 0.0 and prev_state[1] >= 0.0 and state[1] <= 0.0:
            y_prev = prev_state[1]
            y_curr = state[1]
            if abs(y_prev - y_curr) < 1e-15:
                frac = 0.0
            else:
                frac = y_prev / (y_prev - y_curr)

            t_land = prev_t + frac * (t - prev_t)
            x_land = prev_state[0] + frac * (state[0] - prev_state[0])
            landed = True
            break

    if not landed:
        raise RuntimeError("Не удалось найти момент падения в пределах t_max.")

    # Добавляем интерполированную точку падения для аккуратной траектории.
    t_vals[-1] = float(t_land)
    x_vals[-1] = float(x_land)
    y_vals[-1] = 0.0

    return {
        "t": np.array(t_vals, dtype=float),
        "x": np.array(x_vals, dtype=float),
        "y": np.array(y_vals, dtype=float),
        "u": np.array(u_vals, dtype=float),
        "w": np.array(w_vals, dtype=float),
        "t_land": float(t_land),
        "x_land": float(x_land),
        "y_max": float(np.max(y_vals)),
    }


def build_comparison(galileo_res: dict, newton_res: dict) -> list:
    delta_x = newton_res["x_land"] - galileo_res["x_land"]
    return [
        {"metric": "x_land (m)", "galileo": galileo_res["x_land"], "newton": newton_res["x_land"]},
        {"metric": "t_land (s)", "galileo": galileo_res["t_land"], "newton": newton_res["t_land"]},
        {"metric": "y_max (m)", "galileo": galileo_res["y_max"], "newton": newton_res["y_max"]},
        {"metric": "delta_x = x_newton - x_galileo (m)", "galileo": 0.0, "newton": delta_x},
    ]


def save_comparison_csv(comparison_rows: list, output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "galileo", "newton"])
        writer.writeheader()
        writer.writerows(comparison_rows)


def save_plot(galileo_res: dict, newton_res: dict, output_path: Path) -> None:
    configure_matplotlib_for_cyrillic()
    plt.figure(figsize=(9, 5))
    plt.plot(galileo_res["x"], galileo_res["y"], label="Модель Галилея (без сопротивления)", linewidth=2.0)
    plt.plot(newton_res["x"], newton_res["y"], label="Модель Ньютона + сопротивление (RK4)", linewidth=2.0)

    plt.scatter([galileo_res["x_land"], newton_res["x_land"]], [0.0, 0.0], color=["C0", "C1"], s=40)
    plt.axhline(0.0, color="black", linewidth=1.0)
    plt.xlabel("x, м")
    plt.ylabel("y, м")
    plt.title("Сравнение траекторий: Галилей vs Ньютон с сопротивлением")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def print_comparison(comparison_rows: list) -> None:
    print("\nСравнение результатов")
    print("-" * 72)
    print(f"{'Метрика':42} | {'Галилей':12} | {'Ньютон':12}")
    print("-" * 72)
    for row in comparison_rows:
        print(f"{row['metric']:42} | {row['galileo']:12.6f} | {row['newton']:12.6f}")
    print("-" * 72)


def main() -> None:
    params = ModelParams()

    galileo_res = galileo_landing(
        alpha_rad=params.alpha_rad,
        v0=params.v0,
        g=params.g,
        x0=params.x0,
        y0=params.y0,
    )

    newton_res = simulate_newton_rk4(
        alpha_rad=params.alpha_rad,
        v0=params.v0,
        x0=params.x0,
        y0=params.y0,
        g=params.g,
        beta=params.beta,
        m=params.mass,
        dt=1e-3,
        t_max=10.0,
    )

    comparison_rows = build_comparison(galileo_res, newton_res)
    print_comparison(comparison_rows)

    csv_path = Path("comparison.csv")
    png_path = Path("trajectory_comparison.png")
    save_comparison_csv(comparison_rows, csv_path)
    save_plot(galileo_res, newton_res, png_path)

    print("\nПараметры модели Ньютона")
    print(f"beta = {params.beta:.6f} кг/м")
    print(f"m (чугунный шар) = {params.mass:.6f} кг")
    print(f"Файл таблицы: {csv_path.resolve()}")
    print(f"Файл графика: {png_path.resolve()}")


if __name__ == "__main__":
    main()
