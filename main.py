import pandas


def limpiar_columnas_consultas(consultas: pandas.DataFrame):
    # clean creation_date and update_date columns to datetime format
    limpiar_columna_fecha(consultas, 'creation_date')
    limpiar_columna_fecha(consultas, 'update_date')

def limpiar_columnas_consultas_en_legalitica(consultas: pandas.DataFrame):
    limpiar_columna_fecha(consultas, 'creation_date_in_legalitica')
    limpiar_columna_fecha(consultas, 'response_date')

def limpiar_columna_fecha(consultas: pandas.DataFrame, columna: str):
    consultas[columna] = pandas.to_datetime(
        consultas[columna].str[:19]
    )

def ordenar_por_fecha(consultas: pandas.DataFrame):
    consultas.sort_values(
        by='creation_date',
        ignore_index=True,
        inplace=True,
    )

def agregar_duplicados(consultas: pandas.DataFrame):
    """
    If a two rows have the same value in the 'input_national_id' or in the 'input_tax_id'
    and the difference between their 'creation_date' is less than 1 hour, then the second
    row is considered a duplicate.
    """
    
    consultas['duplicated'] = False
    
    for i in range(len(consultas)):
        previous_row = consultas.iloc[i - 1]
        current_row = consultas.iloc[i]
        
        is_duplicated = (
            current_row['creation_date'] and
            previous_row['creation_date'] and
            current_row['type'] == previous_row['type'] and
            (
                current_row['input_national_id'] == previous_row['input_national_id'] or
                current_row['input_tax_id'] == previous_row['input_tax_id']
            ) and
            current_row['creation_date'] - previous_row['creation_date'] < pandas.Timedelta(hours=1)
        )
        
        consultas.loc[i, 'duplicated'] = is_duplicated

if __name__ == '__main__':
    consultas = pandas.read_csv('../Truora_all.csv')
    
    consultas_en_legalitica = pandas.read_csv('../debida_diligencia_consultas_prod.csv')
    
    limpiar_columnas_consultas(consultas)
    
    limpiar_columnas_consultas_en_legalitica(consultas_en_legalitica)
    
    ordenar_por_fecha(consultas)
    
    agregar_duplicados(consultas)
    
    consultas.to_csv('../Truora_all_cleaned.csv', index=False)
    consultas_en_legalitica.to_csv(
        '../debida_diligencia_consultas_prod_cleaned.csv',
        index=False
    )
