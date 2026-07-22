# Script para validar rangos de VLAN
vlan = int(input("Ingrese el número de VLAN: "))

if vlan >= 1 and vlan <= 1005:
    print("El número corresponde a un rango normal de VLAN.")
elif vlan >= 1006 and vlan <= 4094:
    print("El número corresponde a un rango extendido de VLAN.")
else:
    print("El número ingresado no corresponde a una VLAN respectiva.")