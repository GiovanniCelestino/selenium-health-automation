from selenium.webdriver.edge.options import Options
import os
import json


# Captura de retorno padrão: config_edge, pasta_download = ativa_impressao()
# Caminho a ser importado: from scripts.imprime_arquivos.config_impressao import *

# CONFIGURAÇÃO DE IMPRESSÃO (Obrigatório vir antes de iniciar o Chrome)
# PREFERENCIA NAVEGADOR
    #chrome_options = Options()
    #chrome_options.add_argument('--kiosk-printing') # Ativa a impressão sem perguntas

# Configura o destino como "Salvar como PDF" e cria pasta "download_principal" nas pasta "dados" caso não exista
def ativa_impressao():
    edge_options = Options()
    edge_options.add_argument("--kiosk-printing")

    pasta_download = os.path.join(os.getcwd(), "dados","download_principal")
    os.makedirs(pasta_download, exist_ok=True)

    prefs = {
        "printing.print_preview_sticky_settings.appState": json.dumps({
            "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }),
        "savefile.default_directory": pasta_download
    }
    # Preferencia de navegador
    edge_options.add_experimental_option('prefs', prefs)
    #chrome_options.add_experimental_option('prefs', prefs)
    return edge_options, pasta_download
    
    
    