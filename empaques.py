"""
Trabajo Logica Difusa PEP III
Logica y Teoria de la Computacion
Dany Rubiano Jimenez
22.250.855-k
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


############################################# Antecedentes #############################################

####### Factores de empaquetadura:
# Nivel esfuerzo empaque (incluye factores como cantidad de productos, cantidad de bolsas, entre otros)
# Tiempo (Tiempo que demora en terminar una vez el cliente esta listo)

esfuerzo = ctrl.Antecedent(np.arange(0, 8, 0.1), 'Nivel de esfuerzo del empaque') #
tiempo_empaque = ctrl.Antecedent(np.arange(0, 10, 0.1), 'Tiempo de empaque') # Tiempo que demora el empaque en terminar, despues que termina de pagar el cliente


####### Factores externos:
# Nivel de atención cajera (como una nota de 1 a 7, que mide factores de tiempo, amabilidad y otros)
# Tiempo de espera en fila (medido en minutos)

atencion_cajera = ctrl.Antecedent(np.arange(0, 7, 0.1), 'Nivel de atencion cajera')
tiempo_espera = ctrl.Antecedent(np.arange(0,30, 0.1), 'Tiempo de espera en fila') # Cuanto tiempo se esta en la fila esperando atencion


####### Factores internos:
# Nivel de efectivo en el momento (en pesos)
# Nivel de estado de animo (en escala de 1 a 7)

efectivo = ctrl.Antecedent(np.arange(0, 50000, 10), 'Nivel de efectivo') # Disponible en efectivo entre monedas y billetes
estado_animo =ctrl.Antecedent(np.arange(0, 7, 0.1), 'Estado de animo') # Estado de animo se refiere a algo asi como la disponibilidad para dar 


esfuerzo['Bajo'] = fuzz.trapmf(esfuerzo.universe, [0,0,2,3.8])
esfuerzo['Medio'] = fuzz.trapmf(esfuerzo.universe, [3.5,4,4.5,5.4])
esfuerzo['Alto'] = fuzz.trapmf(esfuerzo.universe, [5,5.5,7,7])
#esfuerzo.view()

## Se elimina, porque es muiy variable esta medida, y depende de la cantidad de productos que se empaquen
"""
tiempo_empaque['Bueno'] = fuzz.trapmf(tiempo_empaque.universe, [0,0,1,3])
tiempo_empaque['Medio'] = fuzz.trapmf(tiempo_empaque.universe, [2.5,3.5,4.5,5])
tiempo_empaque['Malo'] = fuzz.trapmf(tiempo_empaque.universe, [4.8,5,8,10])
#tiempo_empaque.view()
"""

atencion_cajera['Bajo'] = fuzz.trapmf(atencion_cajera.universe, [0,0,2,3.8])
atencion_cajera['Medio'] = fuzz.trapmf(atencion_cajera.universe, [3.5,4,4.5,5.4])
atencion_cajera['Alto'] = fuzz.trapmf(atencion_cajera.universe, [5,5.5,7,7])
#atencion_cajera.view()

tiempo_espera['Bueno'] = fuzz.trapmf(tiempo_espera.universe, [0,0,4,5.2])
tiempo_espera['Medio'] = fuzz.trapmf(tiempo_espera.universe, [5,6,9,10])
tiempo_espera['Malo'] = fuzz.trapmf(tiempo_espera.universe, [9,10,30,60])
#tiempo_espera.view()

# En terminos de empaque y la disponibilidad para dar.
efectivo['Nada'] = fuzz.trapmf(efectivo.universe, [0,0,0,0])
efectivo['Muy Bajo'] = fuzz.trapmf(efectivo.universe, [0,250,350,500])
efectivo['Bajo'] = fuzz.trapmf(efectivo.universe, [450,600,800,1000])
efectivo['Medio'] = fuzz.trapmf(efectivo.universe, [900,1200,1800,2000])
efectivo['Alto'] = fuzz.trapmf(efectivo.universe, [1900,2200,10000,10000])
#efectivo.view()

estado_animo['Bajo'] = fuzz.trapmf(estado_animo.universe, [0,0,2,3.8])
estado_animo['Medio'] = fuzz.trapmf(estado_animo.universe, [3.5,4,5,5.4])
estado_animo['Alto'] = fuzz.trapmf(estado_animo.universe, [5,5.5,7,7])
#estado_animo.view()

############################################## Consecuente ##############################################

propina  = ctrl.Consequent(np.arange(0, 5000, 10), 'Propina')

propina['Nada'] = fuzz.trapmf(propina.universe, [0,0,0,0])
propina['Muy Baja'] = fuzz.trapmf(propina.universe, [0,20, 50, 100])
propina['Baja'] = fuzz.trapmf(propina.universe, [80,100, 150, 200])
propina['Media'] = fuzz.trapmf(propina.universe, [150, 200, 400, 600])
propina['Alta'] = fuzz.trapmf(propina.universe, [500, 700, 900, 1000])
propina['Muy Alta'] = fuzz.trapmf(propina.universe, [950, 1100, 10000, 10000])
#propina.view()


################################################# Reglas ################################################

# Las reglas originan los posibles consecuentes de propina, considerando los cinco factores que se nombro antreriormente
# Es una combinación entre lo que se esperaria segun los niveles de cada antecedente y en combinacion de varios de los casos
# En todas se considera el nivel de efectivo y el estado de animo (disponibilidad para dar) ya que son las variables mas importantes.

### Reglas para no dar propina

r1 = ctrl.Rule(efectivo['Nada'], propina['Nada'], 'r1')
r2 = ctrl.Rule(efectivo['Muy Bajo'] & estado_animo['Bajo'], propina['Nada'], 'r2')
r3 = ctrl.Rule(esfuerzo['Bajo'] & estado_animo['Bajo'], propina['Nada'], 'r3')
r4 = ctrl.Rule(atencion_cajera['Bajo'] & estado_animo['Bajo'], propina['Nada'], 'r4')
r5 = ctrl.Rule(tiempo_espera['Malo'] & estado_animo['Bajo'], propina['Nada'], 'r5')
r6 = ctrl.Rule(esfuerzo['Bajo'] & atencion_cajera['Bajo'], propina['Nada'], 'r6')
r7 = ctrl.Rule(esfuerzo['Bajo'] & tiempo_espera['Malo'], propina['Nada'], 'r7')
r8 = ctrl.Rule(atencion_cajera['Bajo'] & tiempo_espera['Malo'] & estado_animo['Bajo'], propina['Nada'], 'r8')
r9 = ctrl.Rule(esfuerzo['Bajo'] & atencion_cajera['Bajo'] & tiempo_espera['Malo'], propina['Nada'], 'r9')
r10 = ctrl.Rule(esfuerzo['Bajo'] & atencion_cajera['Bajo'] & tiempo_espera['Malo'] & estado_animo['Bajo'], propina['Nada'], 'r10')


### Reglas para propina muy baja, deben incluir algun nivel de efectivo que no sea nada.

r11 = ctrl.Rule(efectivo['Bajo'] & estado_animo['Bajo'], propina['Muy Baja'], 'r11')
r12 = ctrl.Rule(efectivo['Muy Bajo'] & (estado_animo['Medio'] | estado_animo['Alto']), propina['Muy Baja'], 'r12')
r13 = ctrl.Rule(esfuerzo['Bajo'] & efectivo['Bajo'], propina['Muy Baja'], 'r13')
r14 = ctrl.Rule(esfuerzo['Bajo'] & estado_animo['Medio'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Muy Baja'], 'r14')
r15 = ctrl.Rule(atencion_cajera['Bajo'] & estado_animo['Medio'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Muy Baja'], 'r15')
r16 = ctrl.Rule(tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Muy Baja'], 'r16')
r17 = ctrl.Rule(atencion_cajera['Bajo'] & tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Muy Baja'], 'r17')
r18 = ctrl.Rule(esfuerzo['Bajo'] & tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Muy Baja'], 'r18')
r19 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Bajo'] & estado_animo['Medio'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Muy Baja'], 'r19')
r20 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Bajo'] & tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Muy Baja'], 'r20')


### Reglas para propina baja, deben incluir algun nivel de efectivo que no sea nada.

r21 = ctrl.Rule((efectivo['Muy Bajo'] | efectivo['Bajo']) & (estado_animo['Medio'] | estado_animo['Alto']), propina['Baja'], 'r21')
r22 = ctrl.Rule(esfuerzo['Bajo'] & efectivo['Medio'], propina['Baja'], 'r22')
r23 = ctrl.Rule(esfuerzo['Bajo'] & estado_animo['Alto'] & (efectivo['Muy Bajo'] | efectivo['Bajo']), propina['Baja'], 'r23')
r24 = ctrl.Rule(atencion_cajera['Bajo'] & estado_animo['Alto'] & (efectivo['Muy Bajo'] | efectivo['Bajo']), propina['Baja'], 'r24')
r25 = ctrl.Rule(tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Muy Bajo'] | efectivo['Bajo']), propina['Baja'], 'r25')
r26 = ctrl.Rule(atencion_cajera['Bajo'] & tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Muy Bajo'] | efectivo['Bajo']), propina['Baja'], 'r26')
r27 = ctrl.Rule(esfuerzo['Bajo'] & tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Muy Bajo'] | efectivo['Bajo']), propina['Baja'], 'r27')
r28 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Bajo'] & estado_animo['Alto'] & (efectivo['Muy Bajo'] | efectivo['Bajo']), propina['Baja'], 'r28')
r29 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Bajo'] & tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Muy Bajo'] | efectivo['Bajo']), propina['Baja'], 'r29')
r30 = ctrl.Rule(esfuerzo['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r30')
r31 = ctrl.Rule(esfuerzo['Medio'] & tiempo_espera['Malo'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r31')
r32 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r32')
r33 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Medio'] & tiempo_espera['Malo'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r33')
r34 = ctrl.Rule(atencion_cajera['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r34')
r35 = ctrl.Rule(atencion_cajera['Medio'] & tiempo_espera['Malo'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r35')
r36 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Bajo'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r36')
r37 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Bajo'] & tiempo_espera['Malo'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r37')
r38 = ctrl.Rule(tiempo_espera['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r38')
r39 = ctrl.Rule(atencion_cajera['Bajo'] & tiempo_espera['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r39')
r40 = ctrl.Rule(esfuerzo['Bajo'] & tiempo_espera['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r40')
r41 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Bajo'] & tiempo_espera['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r41')
r42 = ctrl.Rule(atencion_cajera['Medio'] & tiempo_espera['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r42')
r43 = ctrl.Rule(esfuerzo['Medio'] & tiempo_espera['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r43')
r44 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r44')
r45 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Medio'] & tiempo_espera['Medio'] & estado_animo['Bajo'] & (efectivo['Muy Bajo'] | efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Baja'], 'r45')


### Reglas para propina media, deben incluir algun nivel de efectivo que no sea nada o muy bajo.

r46 = ctrl.Rule(efectivo['Bajo'] & estado_animo['Alto'], propina['Media'], 'r46')
r47 = ctrl.Rule(esfuerzo['Medio'] & efectivo['Medio'], propina['Media'], 'r47')
r48 = ctrl.Rule(esfuerzo['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r48')
r49 = ctrl.Rule(esfuerzo['Medio'] & tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r49')
r50 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r50')
r51 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Medio'] & tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r51')
r52 = ctrl.Rule(atencion_cajera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r52')
r53 = ctrl.Rule(atencion_cajera['Medio'] & tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r53')
r54 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Bajo'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r54')
r55 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Bajo'] & tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r55')
r56 = ctrl.Rule(tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r56')
r57 = ctrl.Rule(atencion_cajera['Bajo'] & tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r57')
r58 = ctrl.Rule(esfuerzo['Bajo'] & tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r58')
r59 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Bajo'] & tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r59')
r60 = ctrl.Rule(atencion_cajera['Medio'] & tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r60')
r61 = ctrl.Rule(esfuerzo['Medio'] & tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r61')
r62 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r62')
r63 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Medio'] & tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r63')
r64 = ctrl.Rule(esfuerzo['Alto'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r64')
r65 = ctrl.Rule(esfuerzo['Alto'] & tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r65')
r66 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Alto'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r66')
r67 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Alto'] & tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r67')
r68 = ctrl.Rule(esfuerzo['Alto'] & tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r68')
r69 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Alto'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r69')
r70 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Alto'] & tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r70')
r71 = ctrl.Rule(esfuerzo['Medio'] & tiempo_espera['Bueno'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r71')
r72 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Medio'] & tiempo_espera['Bueno'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r72')
r73 = ctrl.Rule(atencion_cajera['Medio'] & tiempo_espera['Bueno'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r73')
r74 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Bajo'] & tiempo_espera['Bueno'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r74')
r75 = ctrl.Rule(atencion_cajera['Alto'] & esfuerzo['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r75')
r76 = ctrl.Rule(atencion_cajera['Alto'] & esfuerzo['Medio'] & tiempo_espera['Malo'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r76')
r77 = ctrl.Rule(atencion_cajera['Alto'] & tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r77')
r78 = ctrl.Rule(atencion_cajera['Alto'] & esfuerzo['Bajo'] & tiempo_espera['Medio'] & estado_animo['Medio'] & (efectivo['Bajo'] | efectivo['Medio'] | efectivo['Alto']), propina['Media'], 'r78')


### Reglas para propina alta, deben incluir algun nivel de efectivo que no sea nada, muy bajo o bajo.

r79 = ctrl.Rule(efectivo['Medio'] & estado_animo['Alto'], propina['Alta'], 'r79')
r80 = ctrl.Rule(esfuerzo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r80')
r81 = ctrl.Rule(esfuerzo['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r81')
r82 = ctrl.Rule(esfuerzo['Medio'] & tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r82')
r83 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r83')
r84 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Medio'] & tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r84')
r85 = ctrl.Rule(atencion_cajera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r85')
r86 = ctrl.Rule(atencion_cajera['Medio'] & tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r86')
r87 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Bajo'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r87')
r88 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Bajo'] & tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r88')
r89 = ctrl.Rule(tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r89')
r90 = ctrl.Rule(atencion_cajera['Bajo'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r90')
r91 = ctrl.Rule(esfuerzo['Bajo'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r91')
r92 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Bajo'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r92')
r93 = ctrl.Rule(atencion_cajera['Medio'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r93')
r94 = ctrl.Rule(esfuerzo['Medio'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r94')
r95 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r95')
r96 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Medio'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r96')
r97 = ctrl.Rule(esfuerzo['Alto'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r97')
r98 = ctrl.Rule(esfuerzo['Alto'] & tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r98')
r99 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Alto'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r99')
r100 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Alto'] & tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r100')
r101 = ctrl.Rule(esfuerzo['Alto'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r101')
r102 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Alto'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r102')
r103 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Alto'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r103')
r104 = ctrl.Rule(esfuerzo['Medio'] & tiempo_espera['Bueno'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r104')
r105 = ctrl.Rule(atencion_cajera['Bajo'] & esfuerzo['Medio'] & tiempo_espera['Bueno'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r105')
r106 = ctrl.Rule(atencion_cajera['Medio'] & tiempo_espera['Bueno'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r106')
r107 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Bajo'] & tiempo_espera['Bueno'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r107')
r108 = ctrl.Rule(atencion_cajera['Alto'] & esfuerzo['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r108')
r109 = ctrl.Rule(atencion_cajera['Alto'] & esfuerzo['Medio'] & tiempo_espera['Malo'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r109')
r110 = ctrl.Rule(atencion_cajera['Alto'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r110')
r111 = ctrl.Rule(atencion_cajera['Alto'] & esfuerzo['Bajo'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r111')
r112 = ctrl.Rule(esfuerzo['Alto'] & tiempo_espera['Bueno'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r112')
r113 = ctrl.Rule(atencion_cajera['Alto'] & esfuerzo['Alto'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r113')
r114 = ctrl.Rule(atencion_cajera['Alto'] & esfuerzo['Alto'] & tiempo_espera['Bueno'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r114')
r115 = ctrl.Rule(atencion_cajera['Medio'] & esfuerzo['Alto'] & tiempo_espera['Bueno'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r115')
r116 = ctrl.Rule(atencion_cajera['Alto'] & esfuerzo['Medio'] & tiempo_espera['Bueno'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r116')
r117 = ctrl.Rule(atencion_cajera['Alto'] & esfuerzo['Alto'] & tiempo_espera['Medio'] & estado_animo['Alto'] & (efectivo['Medio'] | efectivo['Alto']), propina['Alta'], 'r117')


### Reglas para propina muy alta, deben incluir algun nivel de efectivo que no sea nada, muy bajo, bajo o medio.

r118 = ctrl.Rule(efectivo['Alto'] & esfuerzo['Alto'] & atencion_cajera['Alto'] & tiempo_espera['Bueno'] & estado_animo['Alto'] & efectivo['Alto'], propina['Muy Alta'], 'r118') 


# controlSystem
control = ctrl.ControlSystem([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17,r18,r19,r20,r21,r22,r23,r24,r25,r26,r27,r28,r29,r30,r31,r32,r33,r34,r35,r36,r37,r38,r39,r40,r41,r42,r43,r44,r45,r46,r47,r48,r49,r50,r51,r52,r53,r54,r55,r56,r57,r58,r59,r60,r61,r62,r63,r64,r65,r66,r67,r68,r69,r70,r71,r72,r73,r74,r75,r76,r77,r78,r79,r80,r81,r82,r83,r84,r85,r86,r87,r88,r89,r90,r91,r92,r93,r94,r95,r96,r97,r98,r99,r100,r101,r102,r103,r104,r105,r106,r107,r108,r109,r110,r111,r112,r113,r114,r115,r116,r117,r118])


# representa una circuntancia del controlSim
controlSim = ctrl.ControlSystemSimulation(control)


# entrada
"""
controlSim.input['Nivel de esfuerzo del empaque'] = 5
controlSim.input['Nivel de atencion cajera'] = 6
controlSim.input['Tiempo de espera en fila'] = 3
controlSim.input['Nivel de efectivo'] = 2500
controlSim.input['Estado de animo'] = 4
"""

controlSim.input['Nivel de esfuerzo del empaque'] = int(input("Ingrese el Nivel del esfuerzo del empaque [0-7]: "))
controlSim.input['Nivel de atencion cajera'] = int(input("Ingrese el Nivel de atencion de la cajera [0-7]: "))
controlSim.input['Tiempo de espera en fila'] = int(input("Ingrese el Tiempo de espera en fila [0-60]: "))
controlSim.input['Nivel de efectivo'] = int(input("Ingrese el Nivel de efectivo [0-10000]: "))
controlSim.input['Estado de animo'] = int(input("Ingrese el Estado de animo [0-7]: "))


controlSim.compute()


# salida
print("\nLa propina es $ " + str(np.around(controlSim.output['Propina'],decimals=-1)) + " (Real $" + str(controlSim.output['Propina']) + ")")

# muestra el grafico resultante
propina.view(sim=controlSim)



input("\nPresione Enter para continuar ...")
