# Modulo para controlar el Testrun
import json
import time
from operaciones import venta, cierre, recarga, pago_servicio, subsidio


def testrun(tests_json, results_json):
    with open(tests_json, "r") as testcasesfile:
        tc = json.load(testcasesfile)
    results = []

    def veredicto():
        result = input("Veredicto? [A]probar/[R]echazar/[RE]petir: ").upper()
        if result == "A":
            append_result = {
                tck[0]: testcase[tck[0]],
                "Resultado": "Aprobado",
            }
            results.append(append_result)
            run = False
            return run
        elif result == "R":
            append_result = {
                tck[0]: testcase[tck[0]],
                "Resultado": "Rechazado",
                "N/A": "",
            }
            results.append(append_result)
            run = False
            return run
        elif result == "RE":
            print(f"Repitiendo {testcase[tck[0]]}")
            run = True
            return run

    def validar_aplica():
        if testcase["NA"] == "NA":
            print(f'Caso {testcase[tck[0]]} "{testcase[tck[1]]}" no aplica')
            append_result = {
                tck[0]: testcase[tck[0]],
                "Resultado": "",
                "NA": "NA",
            }
            results.append(append_result)
            run = False
            return run
        else:
            run = True
            return run

    for testcase in tc:
        tck = list(testcase.keys())
        print(f"Ejecutando {testcase[tck[0]]}")
        test = testcase[tck[1]]
        match test:
            case "Realizar una venta":
                run = validar_aplica()
                while run:
                    monto_decimales = testcase[tck[8]]
                    monto = monto_decimales.replace(",", "")
                    print(
                        f"Enviando Venta {testcase[tck[2]]} {testcase[tck[4]]} {monto_decimales}"
                    )
                    venta(monto, "0%", "", "", "", False)
                    print("Venta enviada, verifique la mensajeria en el ISOHOST")
                    run = veredicto()
            case "Realizar una Recarga":
                run = validar_aplica()
                while run:
                    monto_decimales = testcase["Total"]
                    monto = monto_decimales.replace(",", "")
                    print(
                        f"Enviando Recarga {testcase[tck[2]]} {testcase[tck[4]]} {testcase["Proveedor"]} {testcase["Numero"]} {monto_decimales}"
                    )
                    recarga(monto, testcase["Numero"], testcase["Proveedor"])
                    print("Recarga enviada, verifique la mensajeria en el ISOHOST")
                    run = veredicto()
            case "Realizar un P.Servicio":
                run = validar_aplica()
                while run:
                    print(
                        f"Enviando P.Servicio {testcase[tck[2]]} {testcase[tck[4]]} {testcase["Proveedor"]} {testcase["Numero de Contrato"]}"
                    )
                    pago_servicio(
                        testcase["Proveedor"], testcase["Numero de Contrato"], False
                    )
                    print("P.Servicio enviado, verifique la mensajeria en el ISOHOST")
                    run = veredicto()
            case "Realizar una consulta de Factura":
                run = validar_aplica()
                while run:
                    print(
                        f'Consultando Factura {testcase["Numero de Contrato"]} {testcase["Proveedor"]}'
                    )
                    pago_servicio(
                        testcase["Proveedor"], testcase["Numero de Contrato"], True
                    )
                    print("Consulta Enviada, verifique la mensajeria en el ISOHOST")
                    run = veredicto()
            case "Realizar una Venta por Subsidio":
                init_time = time.time()
                run = validar_aplica()
                while run:
                    print(
                        f'Enviando Subsidio {testcase[tck[2]]} {testcase[tck[4]]} {testcase["Tipo Subsidio"]}'
                    )
                    monto_decimales = testcase["Total"]
                    monto = monto_decimales.replace(",", "")
                    subsidio(monto, testcase["Tipo Subsidio"])
                    print("Subsidio Enviado, verifique mensajeria en el ISOHOST")
                    run = veredicto()
                total_time = time.time() - init_time
                print(f"tiempo de ejecucion: {int(total_time)}s")
            case "Realizar Cierre":
                run = validar_aplica()
                while run:
                    print("Enviando Cierre")
                    cierre()
                    print("Cierre enviado")
                    run = veredicto()
            case _:
                validar_aplica()
    print("Test Run completado exportando resultados")
    with open(results_json, "w") as archivo_resultados:
        json.dump(results, archivo_resultados, indent=4)
    print("Resultados exportados correctamente")
