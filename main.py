import pandas


def limpiar_columnas(consultas: pandas.DataFrame):
    consultas['creation_date'] = pandas.to_datetime(
        consultas['creation_date'].str[:-10]
    )
    consultas['update_date'] = pandas.to_datetime(
        consultas['update_date'].str[:-10]
    )

if __name__ == '__main__':
    consultas = pandas.read_csv('../Truora_all.csv')
    
    limpiar_columnas(consultas)
