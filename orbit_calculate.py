import math as mt

pi = mt.pi

M_EARTH = 5.9722e24          # Масса Земли, кг
G = 6.67430e-11              # Гравитационная постоянная
GM = (M_EARTH * G) / 1e9     # Гравитационный параметр, км^3/с^2
R_EARTH = 6378.1             # Радиус Земли, км


def object_coordinates(mean_motion, e, i, W, w, M0, dt):
    n = mean_motion * 2 * pi / 86400
    a = (GM / n**2) ** (1/3)
    
    T = (2*pi)/n
    M = M0 + mt.degrees(n) * dt

    M_rad = mt.radians(M)

    E_rad = M_rad
    for _ in range(10):
        E_rad = M_rad + e * mt.sin(E_rad)
    E = mt.degrees(E_rad)

    sin_nu = (mt.sqrt(1 - e**2) * mt.sin(E_rad)) / (1 - e * mt.cos(E_rad))
    cos_nu = (mt.cos(E_rad) - e) / (1 - e * mt.cos(E_rad))
    nu = mt.atan2(sin_nu, cos_nu)
    if nu < 0:
        nu += 2 * mt.pi

    r = a * (1 - e * mt.cos(E_rad))

    x = r * mt.cos(nu)
    y = r * mt.sin(nu)

    v2 = GM * (2/r - 1/a) # v^2

    i_rad = mt.radians(i)
    W_rad = mt.radians(W)
    w_rad = mt.radians(w)

    u = w_rad + nu 

    X = r * (mt.cos(W_rad) * mt.cos(u) - mt.sin(W_rad) * mt.sin(u) * mt.cos(i_rad))
    Y = r * (mt.sin(W_rad) * mt.cos(u) + mt.cos(W_rad) * mt.sin(u) * mt.cos(i_rad))
    Z = r * (mt.sin(u) * mt.sin(i_rad))

    return X, Y, Z, r, mt.sqrt(v2)



X, Y, Z, r, v = object_coordinates(
    mean_motion=15.49256954,
    e=0.0007219,
    i=51.6320,
    W=307.5621,
    w=1.6306,
    M0=358.4705,
    dt=0,
)
print(f"X: {X:.2f}, Y: {Y:.2f}, Z: {Z:.2f}")
print(f"r: {r:.2f} км, высота: {r - R_EARTH:.2f} км, v: {v:.3f} км/с")


distance_check = mt.sqrt(X**2 + Y**2 + Z**2)
print(f"{distance_check:.2f} км (r = {r:.2f})")