from nicegui import ui
import requests

customer = "sandbox"

match customer:
    case "sandbox":
        simpro_api_key = '64e597e92412aa3ffeffd814e7667f00cb9e7c03'
        simpro_company_url = f"https://enterprise-sandbox-uk.simprosuite.com/api/v1.0/companies"
        simpro_company_num = "211"
        simpro_link_builder = "https://enterprise-sandbox-uk.simprosuite.com/staff"
        GBP_tag = 167
        missed_call_tag = 166
        Decipher_lead_tag = 168
        company_name = "Sandbox"
        slack_channel = "C084TQ1DSSJ"#testing channel
        no_leads_tag = 86
        exclude_phone = "01709940088"
        leftVoicemailTag = 169
        class statusCodes:
            statusCode1A = 2506
            statusCode1B = 2507
            statusCode1C = 2747
            statusCode1D = 2748
            statusCode1E = 2749
            statusCode1F = 2750
            statusCode1G = 2751
            statusCode1H = 2752
    case "smartflow":
        simpro_api_key = '61672a13b57686bcd55e6fea65f914e41a69710a'#smartflow
        simpro_company_url = f"https://smartflowservices.simprosuite.com/api/v1.0/companies"
        simpro_company_num = "0"
        simpro_link_builder = "https://smartflowservices.simprosuite.com/staff"
        GBP_tag = 126
        missed_call_tag = 124
        Decipher_lead_tag = 125
        company_name = "Smart Flow Services"
        slack_channel = "C0427TUPSTD"#switchboardfree
        recent_age = 60
        no_leads_tag = 41
        exclude_phone = "01709940088"

simpro_headers = {'Authorization': f'Bearer {simpro_api_key}', 'Accept': 'application/json', 'Content-Type': 'application/json'}

def getLeads():
    url = f"{simpro_company_url}/{simpro_company_num}/leads/?Status.ID={statusCodes.statusCode1A}"
    data = requests.get(url, headers=simpro_headers).json()
    url = f"{simpro_company_url}/{simpro_company_num}/leads/?Status.ID={statusCodes.statusCode1C}"
    data = data + requests.get(url, headers=simpro_headers).json()
    url = f"{simpro_company_url}/{simpro_company_num}/leads/?Status.ID={statusCodes.statusCode1E}"
    data = data + requests.get(url, headers=simpro_headers).json()
    url = f"{simpro_company_url}/{simpro_company_num}/leads/?Status.ID={statusCodes.statusCode1G}"
    data = data + requests.get(url, headers=simpro_headers).json()
    return data

def getPhone(customerId):
    url = f"{simpro_company_url}/{simpro_company_num}/customers/?ID={customerId}&columns=Phone"
    data = requests.get(url, headers=simpro_headers).json()
    print(data)
    phone = data[0]["Phone"]
    return phone

def buildTable2(data):
    table2.rows = []
    print(data.args[1])
    phone = getPhone(data.args[1]["customerId"])
    table2.add_row({
        "leadId": data.args[1]["leadId"],
        "leadName": data.args[1]["leadName"],
        "phone": phone
    })

columnLabels = [
    {"name": "leadId",
    "label": "Lead ID",
    "field": "leadId",
    "align": "left"},
    {"name": "leadName",
    "label": "Name",
    "field": "leadName",
    "align": "left"},
    {"name": "customerId",
     "label": "Customer Number",
     "field": "customerId",
     "align": "left"}
]
leads = getLeads()
rowData = []
print(leads)
for i in leads:
    rowData.append({
        "leadId": i["ID"],
        "leadName": i["Customer"]["CompanyName"],
        "customerId": i["Customer"]["ID"]
    })

table1 = ui.table(columns=columnLabels, rows=rowData, row_key='leadId')
table1.on('rowClick', buildTable2, [[], ['leadId', 'leadName', 'customerId'], None])

columns2 = [
    {"name": "leadId",
    "label": "Lead ID",
    "field": "leadId",
    "align": "left"},
    {"name": "leadName",
    "label": "Name",
    "field": "leadName",
    "align": "left"},
    {"phone": "phone",
    "label": "phone",
    "field": "phone",
    "align": "left"}
]

rows2 = [
    {"leadId": "",
    "leadName": "",
    "phone": ""}
]
table2 = ui.table(columns=columns2, rows=rows2, row_key='leadId')
ui.run()

