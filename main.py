import validar_csv


def main():
    csv_filename = 'dados_errado.csv'
    # csv_filename = 'dados_certo.csv'
    json_filename = 'template.json'
    validator_obj = validar_csv.ValidarCSV(csv_filename=csv_filename, json_filename=json_filename, delimiter=',')

    response, qtd_erros = validator_obj.validar()

    print(response)
    print(qtd_erros)


if __name__ == '__main__':
    main()
