from extract import Dados
from rotinas import run_all
import json
import os

run_all()

data = Dados()
path_daily = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/ppc_secretary/daily'
path_weekly = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/ppc_secretary/weekly'
path_monthly = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/ppc_secretary/monthly'
path_rules = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/rules'
path_procedures = 'Q:/GROUPS/BR_SC_JGS_WM_LOGISTICA/PCP/PPC_AI_Procedures/general_procedures'

agendaPCP = json.load(open('agenda.json', 'r', encoding='utf-8'))

paths = [path_daily, path_weekly, path_monthly, path_procedures]
historico = []


#INSERIR INFORMAÇÕES DA AGENDA DO PCP, CRIADA PELA MARGUIT
for seq in agendaPCP:
    historico.append({
        "role": "user",
        "parts": [
            f"Agenda PCP Sequência {seq['SEQ']}:"
        ]
    })
    historico.append({
        "role": "model",
        "parts": [
            f"\nSequência: {seq['SEQ']}\n{seq['REFERÊNCIA']}\nDescrição: {seq['DESCRIÇÃO']}\nUtilidade: {seq['UTILIDADE']}"+ 
            (f"\nDetalhes: {seq['DETALHES']}" if 'DETALHES' in seq else "")
        ]
    })

#NORMAS TRANSCRITAS
for filename in os.listdir(path_rules):
    if filename.endswith(".docx"):
        historico.append({
            "role": "user",
            "parts": [
                f"Texto em extenso para a Norma {filename.replace('.docx','')}"
            ]
        })
        historico.append({
            "role": "model",
            "parts": [
                data.extrair_procedimento(f'{path_rules}/{filename}'),
            ]
        })

#INSERIR PROCEDIMENTOS E DOCUMENTOS WORD
for path in paths:
    for filename in os.listdir(path):
        if filename.endswith(".docx"):
            historico.append({
                "role": "user",
                "parts": [
                    f"Procedimento em extenso para {filename.replace('.docx','')}"
                ]
            })
            historico.append({
                "role": "model",
                "parts": [
                    data.extrair_procedimento(f'{path}/{filename}'),
                ]
            })

