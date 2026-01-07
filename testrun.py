# Modulo para controlar el Testrun
from nocodb.nocodb import NocoDBProject, APIToken, JWTAuthToken
from nocodb.filters import LikeFilter, EqFilter, And
from nocodb.infra.requests_client import NocoDBRequestsClient
from tabulate import tabulate

from loggerman import loggerman

# Initialize logger
logger = loggerman(__name__)

client = NocoDBRequestsClient(
    # Your API Token retrieved from NocoDB conf
    APIToken("YZaBEJL1rypr286-fv5SiHvDTDN_U-NkArE0Gr3b"),
    # Your nocodb root path
    "https://nocodb.bizz.lat",
)

project = NocoDBProject(
    "noco",  # org name. noco by default
    "KINPOS_QA",  # project name. Case sensitive!!
)

table_name = "VENTA_TEST"


def define_result(testcase):
    result = input("Test Result [Success/Fail/Repeat]: ")
    if result.lower() in ["success", "s"]:
        return "Aprobada"
    elif result.lower() in ["fail", "f"]:
        return "Rechazada"
    elif result.lower() in ["repeat", "r"]:
        return "Repeat"
    else:
        print("Invalid input. Please enter Success, Fail, or Repeat.")
        return define_result(testcase)


table_rows = client.table_row_list(project, table_name, params={"limit": 1000})
data = table_rows["list"]
# print(client.table_row_detail(project, table_name, 1))
for w in data:
    row = w["Id"]  # Row number obtained
    testcaseID = w["ID Prueba"]  # Testcase ID obtained
    status = w["Estado"]  # Status obtained
    print(f"Row: {row} - Testcase ID: {testcaseID} - Status: {status}")
    if status == "PorEjecutar":
        new_status = define_result(testcaseID)
        row_data = {"Estado": new_status}
        client.table_row_update(project, table_name, row, row_data)
    elif status == "N/A":
        print(f"Skipping Testcase ID: {testcaseID} with status N/A")
