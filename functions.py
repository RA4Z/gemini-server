import datetime
import json

def ultimo_dia_util(data):
	data -= datetime.timedelta(days=1)
	while data.weekday() >= 5:
		data -= datetime.timedelta(days=1)
	return datetime.datetime.strftime(data,'%d/%m/%Y')


def input_history(name:str, input:str, output:str):
	indicadores = json.load(open('Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/documents/inputs_history.json', 'r', encoding='utf-8'))
	indicadores.append({"username":name, "input":input, "output":output, "time":str(datetime.datetime.now())})
	json.dump(indicadores, open('Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/documents/inputs_history.json', 'w', encoding='utf-8'), indent=4)
	