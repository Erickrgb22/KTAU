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
            case "Venta":
                run = validar_aplica()
                while run:
                    monto_decimales = testcase["Total"]
                    monto = monto_decimales.replace(",", "")
                    tip = testcase["Propina"]
                    currency = testcase["Moneda"]

                    dcc = False
                    if testcase["Franquicia"] != "AMEX":
                        if currency != "" and not dcc:
                            input(
                                "OJO DCC no Habilitado, activar, presione Enter para continuar"
                            )
                            dcc = True
                            print("DCC Activado")
                        if currency == "" and dcc:
                            input(
                                "OJO DCC HABILITADO, Desactivar, presione Enter para continuar"
                            )
                            dcc = False
                            print("DCC Desactivado")

                    ajust = testcase["Ajuste"]

                    void = False
                    if testcase["Anular"].lower() == "si":
                        void = True
                    print(
                        f"Enviando Venta {testcase['ID Prueba']} {testcase['Franquicia']} {testcase['Entrada']} {monto_decimales}"
                    )
                    venta(monto, tip, currency, ajust, void)
                    print("Venta enviada, verifique la mensajeria en el ISOHOST")
                    run = veredicto()
            case "Recarga":
                run = validar_aplica()
                while run:
                    monto_decimales = testcase["Total"]
                    monto = monto_decimales.replace(",", "")
                    print(
                        f"Enviando Recarga {testcase['ID Prueba']} {testcase['Franquicia']} {testcase['Entrada']} {testcase['Proveedor']} {testcase['Contrato']} {monto_decimales}"
                    )
                    recarga(monto, testcase["Contrato"], testcase["Proveedor"])
                    print("Recarga enviada, verifique la mensajeria en el ISOHOST")
                    run = veredicto()
            case "P.Servicio":
                run = validar_aplica()
                while run:
                    print(
                        f"Enviando P.Servicio {testcase['ID Prueba']} {testcase['Franquicia']} {testcase['Entrada']} {testcase['Proveedor']} {testcase['Contrato']}"
                    )
                    pago_servicio(testcase["Proveedor"], testcase["Contrato"], False)
                    print("P.Servicio enviado, verifique la mensajeria en el ISOHOST")
                    run = veredicto()
            case "Consulta Factura":
                run = validar_aplica()
                while run:
                    print(
                        f"Consultando Factura {testcase['Contrato']} {testcase['Proveedor']}"
                    )
                    pago_servicio(testcase["Proveedor"], testcase["Contrato"], True)
                    print("Consulta Enviada, verifique la mensajeria en el ISOHOST")
                    run = veredicto()
            case "Subsidio":
                init_time = time.time()
                run = validar_aplica()
                while run:
                    print(
                        f"Enviando Subsidio {testcase['ID Prueba']} {testcase['Franquicia']}  {testcase['Entrada']} {testcase['Tipo Subsidio']}"
                    )
                    monto_decimales = testcase["Total"]
                    monto = monto_decimales.replace(",", "")
                    subsidio(monto, testcase["Tipo Subsidio"])
                    print("Subsidio Enviado, verifique mensajeria en el ISOHOST")
                    run = veredicto()
                total_time = time.time() - init_time
                print(f"tiempo de ejecucion: {int(total_time)}s")
            case "Cierre":
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
