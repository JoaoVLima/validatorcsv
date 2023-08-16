import csv
import json
import datetime


class ValidarCSV:
    def __init__(self, csv_filename: str, json_filename: str, delimiter: str = ','):
        self.csv_filename = csv_filename
        self.json_filename = json_filename
        self.delimiter = delimiter
        self.header = None
        self.dicionario_template = None
        self.lista_dicionario = None

        self.carregar_csv()
        self.carregar_json()

    def carregar_csv(self):
        with open(self.csv_filename, mode='r') as csv_file:
            lista_csv = csv_file.readlines()

            lista_csv = [line[:-1].split(self.delimiter) for line in lista_csv]
            self.header = lista_csv.pop(0)

            self.lista_dicionario = [{chave: valor for chave, valor in zip(self.header, line)} for line in lista_csv]

    def carregar_json(self):
        with open(self.json_filename, mode='r') as json_file:
            self.dicionario_template = json.load(json_file)

    def validar(self):
        dict_erros = {}
        cont_erros = 0
        for coluna in self.header:
            if coluna not in self.dicionario_template:
                dict_erros[coluna] = f'Coluna {coluna}, não encontrada no template'
                cont_erros += 1
                continue

            dict_erros[coluna] = {}

            for index, linha in enumerate(self.lista_dicionario):
                try:
                    self.verificar(linha[coluna], self.dicionario_template[coluna])
                except Exception as e:
                    dict_erros[coluna][index] = str(e)
                    cont_erros += 1

        return dict_erros, cont_erros

    def verificar(self, valor: str, template: dict):
        if template['is_required'] and not valor:
            raise Exception('Valor obrigatório')
        elif not template['is_required'] and not valor:
            return True

        if template['type'] == 'int':
            if valor.isdigit():
                return True
        elif template['type'] == 'float':
            try:
                float(valor)
                return True
            except Exception as e:
                pass

        elif template['type'] in ['date', 'timestamp']:
            try:
                datetime.datetime.strptime(valor, template['format'])
                return True
            except Exception as e:
                pass

        elif template['type'] == 'bool':
            if valor in ['true', 'false']:
                return True

        else:
            return True

        raise Exception(f'O valor "{valor}" deveria ser {template["type"]}')

        # elif template['type'] == 'string':
        #     raise Exception(f'Valor deveria ser {template["type"]}')

