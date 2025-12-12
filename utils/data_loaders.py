import pandas as pd

# Mapeamento das abas esperadas no Excel
SHEETS = {
    'orcamento_geral': 'ORCAMENTO_GERAL',
    'planejamento_aquisicoes': 'PLANEJAMENTO_AQUISICOES',
    'planejamento_servicos_existente': 'PLANEJAMENTO_SERVICOS_EXISTENTE',
    'planejamento_novos_servicos': 'PLANEJAMENTO_NOVOS_SERVICOS',
    'ordens_de_compra': 'ORDENS_DE_COMPRA',
    'nf_de_servico': 'NF_DE_SERVICO',
    'nf_de_aquisicao': 'NF_DE_AQUISICAO',
    'aquisicao_mensal': 'AQUISICAO_MENSAL',
    'servico_mensal': 'SERVICO_MENSAL',
    'proposta_orcamentaria': 'PROPOSTA_ORCAMENTARIA',
    'nao_planejado': 'NAO_PLANEJADO'
}


def load_excel_data(file_path):
    """
    Carrega as abas do Excel definidas no dicionário SHEETS.
    Caso alguma aba falte, continua o processamento e retorna DF vazio.
    """
    data = {}

    for key, sheet in SHEETS.items():
        try:
            df = pd.read_excel(file_path, sheet_name=sheet)
            data[key] = df
        except Exception:
            data[key] = pd.DataFrame()  # Aba ausente -> DataFrame vazio

    return data


def aplicar_filtros(df, coluna_diretoria, diretorias_selecionadas):
    """
    Aplica filtros por diretoria. Se a coluna não existir, retorna o DF original.
    """
    if df.empty:
        return df

    if coluna_diretoria not in df.columns:
        return df

    return df[df[coluna_diretoria].isin(diretorias_selecionadas)]


def get_diretorias_from_data(data):
    """
    Retorna a lista de diretorias encontradas na aba ORCAMENTO_GERAL.
    Caso a coluna não exista, retorna valores padrão.
    """
    diretorias_padrao = ['PR', 'DE', 'DG', 'DO', 'DC']

    df = data.get('orcamento_geral', pd.DataFrame())

    if not df.empty and 'diretoria' in df.columns:
        diretorias = df['diretoria'].dropna().unique().tolist()
        if diretorias:
            return diretorias

    return diretorias_padrao
