from testruns import testrun

serial = "A80ERICK"
user = "egilmore"
pwd = "csi.ERGB.00"
print("Iniciando testrun")

# print("RUN VENTAS SIN IMPUESTO")
# testrun("./tc_venta_sin_impuesto.json", "./results_venta_sin_impuesto.json")

# print("RUM RECARGAS")
# testrun("./tc_recargas.json", "./results_recargas.json")

# print("RUN P.SERVICIOS")
# testrun("./tc_pservicios.json", "./results_tc_pservicios")

#print("RUN SUBSIDIOS")
#testrun("./tc_sub.json", "./results_tc_sub.json")

print("FIRE RUN")
testrun("./Portal/FIRE_TEST.json", "./Portal/FIRE_TEST.json")
