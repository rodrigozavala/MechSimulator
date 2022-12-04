import sympy as sym
import numpy as np
t1,t2,t3,t4=sym.symbols("t_1 t_2 t_3 t_4")
w1,w2,w3=sym.symbols("w_1 w_2 w_3")
a1,a2,a3=sym.symbols("a_1 a_2 a_3")
l1=7.5
l2=15
l3=5
l4=10
theta1=3.1415*0.25
omega1=3.1415*0.3
alfa1=0
theta4=3.1415*0.75
#ec1=sym.Eq(t1**2+t1*2+t2**2+33,12)
#ec2=sym.Eq(-t2**2+t1**3,23)
#print(ec1.subs(t1,12))
ec1=sym.Eq(l1*sym.cos(t1)+l2*sym.cos(t2)+l3*sym.cos(t3)+l4*sym.cos(t4),0).subs(t4,theta4).subs(t1,theta1)
ec2=sym.Eq(l1*sym.sin(t1)+l2*sym.sin(t2)+l3*sym.sin(t3)+l4*sym.sin(t4),0).subs(t4,theta4).subs(t1,theta1)
ec3=sym.Eq(-l1*w1*sym.sin(t1)-l2*w2*sym.sin(t2)-l3*w3*sym.sin(t3),0).subs(t1,theta1).subs(w1,omega1)
ec4=sym.Eq(l1*w1*sym.cos(t1)+l2*w2*sym.cos(t2)+l3*w3*sym.cos(t3),0).subs(t1,theta1).subs(w1,omega1)
ec5=sym.Eq(-w1**2*l1*sym.cos(t1)-w2**2*l2*sym.cos(t2)-w3**2*l3*sym.cos(t3)-a1*l1*sym.sin(t1)-a2*l2*sym.sin(t2)-a3*l3*sym.sin(t3),0).subs(t1,theta1).subs(w1,omega1).subs(a1,alfa1)
ec6=sym.Eq(-w1**2*l1*sym.sin(t1)-w2**2*l2*sym.sin(t2)-w3**2*l3*sym.sin(t3)+a1*l1*sym.cos(t1)+a2*l2*sym.cos(t2)+a3*l3*sym.cos(t3),0).subs(t1,theta1).subs(w1,omega1).subs(a1,alfa1)
for e in [ec1,ec2,ec3,ec4,ec5,ec6]:
    print(e)
print(sym.nsolve([ec1,ec2,ec3,ec4,ec5,ec6],[t2,t3,w2,w3,a2,a3],[3.1415*2*0.6,3.1415*0.8,0,0,0,0]))
