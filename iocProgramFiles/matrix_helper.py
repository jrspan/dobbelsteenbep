import sympy as sp
import numpy as np

px, py, pz, vx, vy, vz, q0, q1, q2, q3 = sp.symbols('px py pz vx vy vz q0 q1 q2 q3')
ax, ay, az, ox, oy, oz, T = sp.symbols('ax ay az ox oy oz T')
pex, pey, pez, vex, vey, vez, omex, omey, omez = sp.symbols('pex pey pez vex vey vez ex, ey, ez')

def expq_sp(vec):
    x, y, z = vec
    absq = (x ** 2 + y ** 2 + z ** 2) ** 0.5
    out = sp.Matrix([
        [sp.cos(absq)],
        [x * sp.sin(absq) / absq],
        [y * sp.sin(absq) / absq],
        [z * sp.sin(absq) / absq]
    ])
    return out

def quat_mul_sp(p, q):
    p0 = p[0]
    q0 = q[0]
    pv = sp.Matrix(p[1:])
    qv = sp.Matrix(q[1:])
    out0 = p0 * q0 - pv.dot(qv)
    outv = p0 * qv + q0 * pv + pv.cross(qv)
    out = sp.Matrix([
        [out0],
        [outv]
    ])
    return out

def left_quat_mul_sp(q):
    q0, q1, q2, q3 = q
    lqm = sp.Matrix([
        [q0, -q1, -q2, -q3],
        [q1, q0, -q3, q2],
        [q2, q3, q0, -q1],
        [q3, -q2, q1, q0]
    ])
    return lqm


R = sp.Matrix([
    [2*q0**2 + 2*q1**2 - 1, 2*q1*q2 - 2*q0*q3, 2*q1*q3 + 2*q0*q2],
    [2*q1*q2 + 2*q0*q3, 2*q0**2 + 2*q2**2 - 1, 2*q2*q3 - 2*q0*q1],
    [2*q1*q3 - 2*q0*q2, 2*q2*q3 + 2*q0*q1, 2*q0**2 + 2*q3**2 - 1]
])

q = sp.Matrix([
    [q0],
    [q1],
    [q2],
    [q3]
])

y_acc = sp.Matrix([
    [ax],
    [ay],
    [az]
])

y_omega = sp.Matrix([
    [ox],
    [oy],
    [oz]
])

p = sp.Matrix([
    [px],
    [py],
    [pz]
])

v = sp.Matrix([
    [vx],
    [vy],
    [vz]
])

gn_sp = sp.Matrix([
    [0],
    [0],
    [1]
])

ep = sp.Matrix([
    [pex],
    [pey],
    [pez]
])

ev = sp.Matrix([
    [vex],
    [vey],
    [vez]
])

eom = sp.Matrix([
    [omex],
    [omey],
    [omez]
])
dqdeom = sp.Matrix([
    [0,0,0],
    [1,0,0],
    [0,1,0],
    [0,0,1]
])



f = sp.Matrix([
    [p + T * v + 0.5 * T**2 * (R * y_acc - gn_sp)],
    [v + T * (R * y_acc - gn_sp)],
    [quat_mul_sp(q, 0.5 * T * expq_sp(y_omega))]
])
F = f.jacobian([px, py, pz, vx, vy, vz, q0, q1, q2, q3])
F_numeric = sp.lambdify([px, py, pz, vx, vy, vz, q0, q1, q2, q3, ax, ay, az, ox, oy, oz, T], F, 'numpy')



T_omega = -0.5 * T * left_quat_mul_sp(q) * dqdeom
pv = sp.Matrix([
    [p + T * v + 0.5 * T**2 * (R * y_acc - gn_sp + ep)],
    [v + T * (R * y_acc - gn_sp + ev)]
])
values = {pex: 0, pey: 0, pez: 0, vex: 0, vey: 0, vez: 0, omex: 0, omey: 0, omez: 0}
dpvde = pv.jacobian([pex, pey, pez, vex, vey, vez, omex, omey, omez])
dpvde = dpvde.subs(values)
G = sp.Matrix([
    [dpvde],
    [sp.zeros(4, 6),T_omega]
])
G_numeric = sp.lambdify([px, py, pz, vx, vy, vz, q0, q1, q2, q3, T], G, 'numpy')


large_H_upperleft = sp.Matrix([[pz], [vx], [vy], [vz]]).jacobian([px, py, pz, vx, vy, vz])
H_lowerright = 2 * sp.Matrix([
    [-q2, q3, -q0, q1],
    [q1, q0, q3, q2],
    [2 * q0, 0, 0, 2 * q3]
])
large_H = sp.Matrix([
    [large_H_upperleft, sp.zeros(4,4)],
    [sp.zeros(3,6), H_lowerright]
])
large_H_numeric = sp.lambdify([px, py, pz, vx, vy, vz, q0, q1, q2, q3], large_H, 'numpy')
small_H = sp.Matrix([[sp.zeros(3,6), H_lowerright]])
small_H_numeric = sp.lambdify([px, py, pz, vx, vy, vz, q0, q1, q2, q3], small_H, 'numpy')



def calculate_F(state, y_omega, y_acc, dt):
    pxnum, pynum, pznum, vxnum, vynum, vznum, q0num, q1num, q2num, q3num = state
    ax_num, ay_num, az_num = y_acc
    ox_num, oy_num, oz_num = y_omega
    return F_numeric(pxnum, pynum, pznum, vxnum, vynum, vznum, q0num, q1num, q2num, q3num, ax_num, ay_num, az_num, ox_num, oy_num, oz_num, dt)

def calculate_G(state, dt):
    pxnum, pynum, pznum, vxnum, vynum, vznum, q0num, q1num, q2num, q3num = state
    return G_numeric(pxnum, pynum, pznum, vxnum, vynum, vznum, q0num, q1num, q2num, q3num, dt)

def calculate_small_H(state):
    pxnum, pynum, pznum, vxnum, vynum, vznum, q0num, q1num, q2num, q3num = state
    return small_H_numeric(pxnum, pynum, pznum, vxnum, vynum, vznum, q0num, q1num, q2num, q3num)

def calculate_large_H(state):
    pxnum, pynum, pznum, vxnum, vynum, vznum, q0num, q1num, q2num, q3num = state
    return large_H_numeric(pxnum, pynum, pznum, vxnum, vynum, vznum, q0num, q1num, q2num, q3num)