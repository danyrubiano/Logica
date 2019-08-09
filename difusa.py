
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl



# antecedentes

servicio = ctrl.Antecedent(np.arange(0, 10, 1), 'servicio')
calidad  = ctrl.Antecedent(np.arange(0, 10, 1), 'calidad')

propina  = ctrl.Consequent(np.arange(0, 10, 1), 'propina')

# funciones de pertenencia automaticas
servicio.automf(3);

calidad['bajo'] = fuzz.trapmf(calidad.universe, [0,0, 1, 5])
calidad['medio'] = fuzz.trapmf(calidad.universe, [2, 3, 6, 7])
calidad['alto'] = fuzz.trapmf(calidad.universe, [5, 8, 10, 10])

# graficar las funciones de pertenencia
servicio.view()
calidad.view()

# consecuente
propina['bajo'] = fuzz.trapmf(calidad.universe, [0,0, 1, 5])
propina['medio'] = fuzz.trapmf(calidad.universe, [2, 3, 6, 7])
propina['alto'] = fuzz.trapmf(calidad.universe, [5, 8, 10, 10])

# graficar las funciones de pertenencia
propina.view()


# reglas


regla1 = ctrl.Rule(servicio['good'] | calidad['alto'], propina['alto'], 'regla1')
regla2 = ctrl.Rule(servicio['average'] , propina['medio'], 'regla2')
regla3 = ctrl.Rule(servicio['poor'] & calidad['bajo'], propina['bajo'], 'regla3')


# controlSystem
control = ctrl.ControlSystem([regla1, regla2, regla3])


# representa una circuntancia del controlSim
controlSim = ctrl.ControlSystemSimulation(control)


# entrada
controlSim.input['calidad'] = 6
controlSim.input['servicio'] = 8


controlSim.compute()


# salida
print(controlSim.output['propina'])

# muestra el grafico resultante
propina.view(sim=controlSim)



input()
