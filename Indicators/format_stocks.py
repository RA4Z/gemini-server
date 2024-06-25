import datetime
import json

target_year = int((datetime.date.today() - datetime.timedelta(days=datetime.date.today().day)).strftime("%Y"))
replace_list = json.load(open("replace_list.json", "r", encoding="utf-8"))

itens = ['JGSTotal']


def replace_strings(actual: str):
    for item in replace_list:
        if item["actual"] == actual:
            return item["new"]
    return None


def delete_months(item):
    del item['Jan']
    del item['Feb']
    del item['Mar']
    del item['Apr']
    del item['May']
    del item['Jun']
    del item['Jul']
    del item['Aug']
    del item['Sep']
    del item['Oct']
    del item['Nov']
    del item['Dec']


def formatar_json(data):
    formatted_data = []
    for item in data:
        for item_base in itens:
            if item['Concatenar'] == f"{item_base}{target_year}Inventory":  # Comparar com a chave "item"
                new = replace_strings(f"Stocks {item_base}")
                if new is not None:
                    item['Concatenar'] = new

                item['averages'] = []
                item['data'] = [item['Jan'], item['Feb'], item['Mar'], item['Apr'], item['May'], item['Jun'],
                                item['Jul'], item['Aug'], item['Sep'], item['Oct'], item['Nov'], item['Dec']]
                delete_months(item)

                for plus in data:
                    if plus['Concatenar'] == f"{item_base}{target_year - 2}Inventory":
                        item['averages'].append(plus['Annualized'])

                    if plus['Concatenar'] == f"{item_base}{target_year - 1}Inventory":
                        item['last'] = [plus['Jan'], plus['Feb'], plus['Mar'], plus['Apr'], plus['May'], plus['Jun'],
                                        plus['Jul'], plus['Aug'], plus['Sep'], plus['Oct'], plus['Nov'], plus['Dec']]
                        item['averages'].append(plus['Annualized'])

                    if plus['Concatenar'] == f"{item_base}{target_year}Inventory Target":
                        item['target'] = [plus['Jan'], plus['Feb'], plus['Mar'], plus['Apr'], plus['May'], plus['Jun'],
                                          plus['Jul'], plus['Aug'], plus['Sep'], plus['Oct'], plus['Nov'], plus['Dec']]

                item['averages'].append(item['Annualized'])
                formatted_data.append(item)
                break

    return formatted_data
