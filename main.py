from browser import Browser
from form_filler import LogzzFormFiller

# Dados simulados (substitua por dados reais ou dinâmicos)
dados_cliente = {
    "nome": "João da Silva",
    "telefone": "11999999999",
    "endereco": {
        "cep": "04001-000",
        "logradouro": "Rua das Flores",
        "numero": "123",
        "complemento": "Apto 101",
        "bairro": "Bairro das Flores",
    }
}

# Iniciar navegador
browser = Browser(headless=False)  # Coloque True para rodar sem abrir janela
driver = browser.start()

# Preencher formulário
filler = LogzzFormFiller(browser)
sucesso = filler.fill_stage_one(dados_cliente)
sucesso = filler.fill_stage_two(dados_cliente)

if sucesso:
    print("Formulário preenchido com sucesso.")
else:
    print("Erro ao preencher o formulário.")

# Encerrar navegador
driver.quit()
