import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression

def cargar_datos(ruta):
    """Carga el archivo CSV y retorna DataFrame"""
    return pd.read_csv(ruta)

def convertir_rango_ingreso(valor):
    """Convierte rango tipo '$5,001-$10,000' a promedio numérico"""
    try:
        if isinstance(valor, str):
            partes = valor.replace("$", "").replace(",", "").split("-")
            nums = [float(p.strip()) for p in partes if p.strip().replace('.', '', 1).isdigit()]
            if len(nums) == 2:
                return sum(nums) / 2
            elif len(nums) == 1:
                return nums[0]
        else:
            return float(valor)
    except:
        return None

def predecir_ingreso_tipo(df, edad, sexo, nivel_estudios, horas, tipo_trabajo):
    data = df[['Edad', 'Sexo', 'Nivel_Ingresos', 'Nivel_Estudios', 'Tipo_Empleo', 'Jornada']].dropna()
    data['Edad'] = pd.to_numeric(data['Edad'], errors='coerce')
    data['Nivel_Ingresos'] = data['Nivel_Ingresos'].apply(convertir_rango_ingreso)
    data = data.dropna()

    data['Tipo_Trabajo_Formal'] = data['Jornada'].str.lower().str.contains('formal').astype(int)

    X = pd.get_dummies(data[['Edad', 'Sexo', 'Nivel_Estudios']], drop_first=True)
    X['Horas_Deseadas'] = horas
    X['Tipo_Trabajo_Formal'] = data['Tipo_Trabajo_Formal']

    y_reg = data['Nivel_Ingresos']
    y_clas = data['Tipo_Empleo']

    reg = LinearRegression().fit(X, y_reg)
    clas = LogisticRegression(max_iter=1000).fit(X, y_clas)

    columnas_ordenadas = X.columns

    input_row = pd.DataFrame(0, index=[0], columns=columnas_ordenadas)

    input_row.at[0, 'Edad'] = edad
    input_row.at[0, 'Horas_Deseadas'] = horas
    input_row.at[0, 'Tipo_Trabajo_Formal'] = 1 if tipo_trabajo.lower() == 'formal' else 0

    for col in columnas_ordenadas:
        if col.startswith('Sexo_') and col == f'Sexo_{sexo}':
            input_row.at[0, col] = 1
        if col.startswith('Nivel_Estudios_') and col == f'Nivel_Estudios_{nivel_estudios}':
            input_row.at[0, col] = 1

    ingreso_pred = reg.predict(input_row)[0]
    tipo_pred = clas.predict(input_row)[0]

    return ingreso_pred, tipo_pred
