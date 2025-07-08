import logging
import time
from typing import Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

class LogzzFormFiller:
    """
    Classe para preencher o formulário do site Logzz.
    """
    def __init__(self, browser):
        """
        Inicializa o preenchedor de formulário.
        
        Args:
            browser: Instância da classe Browser
        """
        self.browser = browser
        self.driver = browser.driver
        #self.url = "https://entrega.logzz.com.br/pay/oferta-padrao"
        self.url = "https://entrega.logzz.com.br/pay/QYSLBC/ohcky-1-unidade-escova-alisadora"
        
    def fill_stage_one(self, data: Dict[str, Any]) -> bool:
        """
        Preenche a primeira etapa do formulário (nome e telefone).
        
        Args:
            data: Dicionário contendo os dados do cliente
            
        Returns:
            bool: True se o preenchimento foi bem-sucedido, False caso contrário
        """
        try:
            logging.info("Preenchendo a primeira etapa do formulário")
            
            # Navegar para o site
            logging.info(f"Acessando o site: {self.url}")
            self.driver.get(self.url)
            
            # Aguardar carregamento completo da página
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Esperar um momento para o site carregar completamente
            time.sleep(3)
            
            # Preencher nome - usando o seletor ID que é mais confiável
            logging.info(f"Preenchendo nome: {data['nome']}")
            name_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="order_name"]'))
            )
            name_field.clear()
            name_field.send_keys(data["nome"])
            logging.info("Campo de nome preenchido com sucesso")
            
            # Preencher telefone - usando o seletor XPath completo
            logging.info(f"Preenchendo telefone: {data['telefone']}")
            phone_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="information"]/div[2]/div/div[1]/div[2]/div/input'))
            )
            phone_field.clear()
            phone_field.send_keys(data["telefone"])
            logging.info("Campo de telefone preenchido com sucesso")
            
            # Tirar screenshot para verificação
            logging.info("Capturando screenshot após preenchimento dos campos")
            self.driver.save_screenshot("form_preenchido.png")
            
            # Clicar no botão continuar - usando o seletor XPath fornecido
            logging.info("Clicando no botão continuar")
            continue_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="information"]/div[2]/div/div[2]/button'))
            )
            continue_button.click()
            logging.info("Botão de continuar clicado")
            
            # Aguardar carregamento da próxima etapa
            time.sleep(3)
            
            # Verificar se avançou para a próxima etapa (verificando se elementos da etapa 2 estão presentes)
            try:
                # Verificar se há um elemento que indica a próxima etapa (como o título "Endereço e entrega")
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Endereço e entrega')]"))
                )
                is_success = True
                logging.info("Primeira etapa preenchida com sucesso - Passou para a etapa de endereço")
                # Tirar screenshot para verificar que avançou
                self.driver.save_screenshot("etapa2_carregada.png")
            except (TimeoutException, NoSuchElementException) as e:
                is_success = False
                logging.error(f"Falha ao preencher a primeira etapa: {str(e)}")
                # Capturar screenshot em caso de erro
                self.driver.save_screenshot("erro_etapa1.png")
                
            return is_success
            
        except Exception as e:
            logging.error(f"Erro ao preencher a primeira etapa: {str(e)}")
            # Capturar screenshot em caso de erro
            self.driver.save_screenshot("erro_etapa1.png")
            return False
    
    def fill_stage_two(self, data: Dict[str, Any]) -> bool:
        """
        Preenche a segunda etapa do formulário (endereço).
        
        Args:
            data: Dicionário contendo os dados do endereço
            
        Returns:
            bool: True se o preenchimento foi bem-sucedido, False caso contrário
        """
        try:
            logging.info("Preenchendo a segunda etapa do formulário (endereço)")
            
            # Verificar se estamos na etapa correta
            try:
                address_title = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Endereço e entrega')]"))
                )
                logging.info("Etapa de endereço carregada, prosseguindo com o preenchimento")
            except (TimeoutException, NoSuchElementException) as e:
                logging.error(f"Não estamos na etapa de endereço: {str(e)}")
                return False
            
            # Capturar screenshot antes de começar o preenchimento
            self.driver.save_screenshot("antes_preenchimento_endereco.png")
            
            # Aguardar para garantir que os elementos estão visíveis
            time.sleep(2)
            
            # Capturar o HTML da página atual para depuração
            page_source = self.driver.page_source
            with open("endereco_page_source.html", "w", encoding="utf-8") as f:
                f.write(page_source)
            logging.info("Código fonte da página salvo para depuração")
            
            # Não vamos mais procurar ou clicar no botão "Editar", pois isso nos levaria de volta à primeira etapa
            logging.info("Iniciando o preenchimento direto dos campos de endereço")
            
            # Tentar encontrar o campo de CEP com múltiplas abordagens
            logging.info(f"Tentando encontrar e preencher o campo de CEP: {data['endereco']['cep']}")
            try:
                # Tentar encontrar o campo de CEP com o XPath específico fornecido
                logging.info("Tentando encontrar o campo de CEP com XPath específico")
                cep_field = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="order_zipcode"]'))
                )
                logging.info("Campo de CEP encontrado com XPath específico")
            except (TimeoutException, NoSuchElementException) as e:
                logging.warning(f"Não foi possível encontrar o campo de CEP com XPath específico: {str(e)}")
                try:
                    # Tentar encontrar o campo de CEP de outras formas
                    logging.info("Tentando encontrar o campo de CEP por ID 'cep'")
                    cep_field = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "cep"))
                    )
                    logging.info("Campo de CEP encontrado por ID")
                except (TimeoutException, NoSuchElementException) as e:
                    logging.warning(f"Não foi possível encontrar o campo de CEP por ID: {str(e)}")
                    try:
                        logging.info("Tentando encontrar o campo de CEP por placeholder")
                        cep_field = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='CEP']"))
                        )
                        logging.info("Campo de CEP encontrado por placeholder")
                    except (TimeoutException, NoSuchElementException) as e:
                        logging.error(f"Não foi possível encontrar o campo de CEP: {str(e)}")
                        self.driver.save_screenshot("erro_campo_cep_nao_encontrado.png")
                        return False
            
            # Limpar e preencher o campo de CEP
            cep_field.click()
            cep_field.clear()
            cep_field.send_keys(data['endereco']['cep'])
            # Pressionar Tab para sair do campo e acionar busca de CEP
            cep_field.send_keys(Keys.TAB)
            logging.info("Campo CEP preenchido e Tab pressionado")
            
            # Aguardar o autopreenchimento dos campos de endereço
            logging.info("Aguardando autopreenchimento dos campos de endereço")
            time.sleep(5)
            self.driver.save_screenshot("apos_preencher_cep.png")
            
            # Preencher número usando o XPath específico fornecido
            logging.info(f"Tentando preencher o campo de número: {data['endereco']['numero']}")
            try:
                number_field = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="address"]/div[2]/div/div[4]/div[1]/input'))
                )
                logging.info("Campo de número encontrado")
                number_field.clear()
                number_field.send_keys(data['endereco']['numero'])
                logging.info("Campo número preenchido")
            except (TimeoutException, NoSuchElementException) as e:
                logging.error(f"Não foi possível encontrar o campo de número: {str(e)}")
                self.driver.save_screenshot("erro_campo_numero_nao_encontrado.png")
                
                # Tentar outras abordagens para encontrar o campo de número
                try:
                    logging.info("Tentando encontrar o campo de número por ID ou placeholder")
                    number_field = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Número' or @id='number']"))
                    )
                    number_field.clear()
                    number_field.send_keys(data['endereco']['numero'])
                    logging.info("Campo número preenchido com abordagem alternativa")
                except (TimeoutException, NoSuchElementException) as e:
                    logging.error(f"Todas as tentativas de encontrar o campo de número falharam: {str(e)}")
                    # Continuamos mesmo sem preencher o número, para tentar avançar o máximo possível
            
            # Preencher complemento (se fornecido) usando o XPath específico fornecido
            if 'complemento' in data['endereco'] and data['endereco']['complemento']:
                logging.info(f"Tentando preencher o campo de complemento: {data['endereco']['complemento']}")
                try:
                    complement_field = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="order_address_complement"]'))
                    )
                    complement_field.clear()
                    complement_field.send_keys(data['endereco']['complemento'])
                    logging.info("Campo complemento preenchido")
                except (TimeoutException, NoSuchElementException) as e:
                    logging.warning(f"Não foi possível encontrar o campo de complemento: {str(e)}")
                    # Não é crítico, continuamos sem o complemento
            
            # Preencher informações adicionais (se fornecido) usando o XPath específico fornecido
            if 'informacoes_adicionais' in data['endereco'] and data['endereco']['informacoes_adicionais']:
                logging.info(f"Tentando preencher o campo de informações adicionais: {data['endereco']['informacoes_adicionais']}")
                try:
                    additional_info_field = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="address"]/div[2]/div/div[5]/div/textarea'))
                    )
                    additional_info_field.clear()
                    additional_info_field.send_keys(data['endereco']['informacoes_adicionais'])
                    logging.info("Campo informações adicionais preenchido")
                except (TimeoutException, NoSuchElementException) as e:
                    logging.warning(f"Não foi possível encontrar o campo de informações adicionais: {str(e)}")
                    # Não é crítico, continuamos sem as informações adicionais
            
            # Capturar screenshot após preenchimento
            logging.info("Capturando screenshot após preenchimento do endereço")
            self.driver.save_screenshot("endereco_preenchido.png")
            
            # Clicar no botão confirmar endereço usando o XPath específico fornecido
            logging.info("Tentando clicar no botão confirmar endereço")
            try:
                continue_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="address"]/div[2]/div/div[7]/button'))
                )
                logging.info("Botão confirmar endereço encontrado")
                continue_button.click()
                logging.info("Botão de confirmar endereço clicado")
            except (TimeoutException, NoSuchElementException) as e:
                logging.error(f"Não foi possível encontrar o botão de confirmar endereço: {str(e)}")
                self.driver.save_screenshot("erro_botao_confirmar_nao_encontrado.png")
                
                # Tentar outras abordagens para encontrar o botão
                try:
                    logging.info("Tentando encontrar o botão por texto 'Continuar' ou 'Salvar'")
                    continue_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar') or contains(text(), 'Salvar') or contains(text(), 'Próximo')]"))
                    )
                    continue_button.click()
                    logging.info("Botão alternativo encontrado e clicado")
                except (TimeoutException, NoSuchElementException) as e:
                    logging.error(f"Todas as tentativas de encontrar o botão falharam: {str(e)}")
                    return False
            
            # Aguardar carregamento da próxima etapa
            time.sleep(4)
            self.driver.save_screenshot("apos_clicar_confirmar.png")
            
            # Verificar se avançou para a próxima etapa (etapa 3 - escolha do dia para receber o entregador)
            try:
                # Verificar se há um elemento que indica a próxima etapa
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Escolha o dia para receber o entregador')]"))
                )
                is_success = True
                logging.info("Segunda etapa preenchida com sucesso - Passou para a etapa de escolha da data")
                # Tirar screenshot para verificar que avançou
                self.driver.save_screenshot("etapa3_carregada.png")
            except (TimeoutException, NoSuchElementException) as e:
                is_success = False
                logging.error(f"Falha ao preencher a segunda etapa: {str(e)}")
                # Capturar screenshot em caso de erro
                self.driver.save_screenshot("erro_etapa2.png")
                
            return is_success
            
        except Exception as e:
            logging.error(f"Erro ao preencher a segunda etapa: {str(e)}")
            # Capturar screenshot em caso de erro
            self.driver.save_screenshot("erro_etapa2.png")
            return False

    def fill_stage_three(self, data: Dict[str, Any]) -> bool:
        """
        Preenche a terceira etapa do formulário (escolha da data de entrega).
        
        Args:
            data: Dicionário contendo os dados para escolha da data
            
        Returns:
            bool: True se o preenchimento foi bem-sucedido, False caso contrário
        """
        try:
            logging.info("Preenchendo a terceira etapa do formulário (escolha da data)")
            
            # Verificar se estamos na etapa correta
            try:
                scheduling_title = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Escolha o dia para receber o entregador')]"))
                )
                logging.info("Etapa de escolha da data carregada, prosseguindo com o preenchimento")
            except (TimeoutException, NoSuchElementException) as e:
                logging.error(f"Não estamos na etapa de escolha da data: {str(e)}")
                return False
            
            # Capturar screenshot antes de começar a seleção
            self.driver.save_screenshot("antes_selecao_data.png")
            
            # Aguardar para garantir que os elementos estão visíveis
            time.sleep(2)
            
            # Determinar qual data selecionar (padrão: primeira data disponível, ou personalizada se especificada)
            date_index = 0  # valor padrão: primeira data (index 0)
            if 'data_index' in data:
                date_index = data['data_index']
                logging.info(f"Selecionando data personalizada com índice: {date_index}")
            else:
                logging.info("Usando data padrão (primeira disponível)")
            
            # Tentar selecionar a data com o índice especificado
            try:
                date_id = f"day-{date_index}"
                logging.info(f"Tentando selecionar a data com ID: {date_id}")
                
                # Clicar no input radio button
                date_radio = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, date_id))
                )
                date_radio.click()
                logging.info(f"Data selecionada: {date_id}")
                
                # Capturar o valor da data selecionada para o log
                date_value = date_radio.get_attribute("value")
                logging.info(f"Valor da data selecionada: {date_value}")
                
                # Tirar screenshot após a seleção da data
                self.driver.save_screenshot("data_selecionada.png")
            except (TimeoutException, NoSuchElementException) as e:
                logging.error(f"Não foi possível selecionar a data com ID {date_id}: {str(e)}")
                
                # Tentar uma abordagem alternativa - clicar no card inteiro
                try:
                    logging.info(f"Tentando abordagem alternativa: clicando no card da data")
                    date_card = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'card-day-{date_index}')]"))
                    )
                    date_card.click()
                    logging.info("Card da data clicado com sucesso")
                    self.driver.save_screenshot("data_selecionada_alternativa.png")
                except (TimeoutException, NoSuchElementException) as e:
                    logging.error(f"Todas as tentativas de selecionar a data falharam: {str(e)}")
                    self.driver.save_screenshot("erro_selecao_data.png")
                    return False
            
            # Clicar no botão de confirmação da data
            logging.info("Tentando clicar no botão de confirmação de data")
            try:
                confirm_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="scheduling"]/div[2]/div/div[3]/button'))
                )
                logging.info("Botão de confirmação de data encontrado")
                confirm_button.click()
                logging.info("Botão de confirmação de data clicado")
            except (TimeoutException, NoSuchElementException) as e:
                logging.error(f"Não foi possível encontrar o botão de confirmação de data: {str(e)}")
                self.driver.save_screenshot("erro_botao_confirmar_data_nao_encontrado.png")
                
                # Tentar abordagens alternativas para encontrar o botão
                try:
                    logging.info("Tentando encontrar o botão por texto")
                    confirm_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Finalizar') or contains(text(), 'Continuar') or contains(text(), 'Próximo')]"))
                    )
                    confirm_button.click()
                    logging.info("Botão alternativo encontrado e clicado")
                except (TimeoutException, NoSuchElementException) as e:
                    logging.error(f"Todas as tentativas de encontrar o botão falharam: {str(e)}")
                    return False
            
            # Aguardar carregamento da próxima etapa
            time.sleep(4)
            self.driver.save_screenshot("apos_confirmar_data.png")
            
            # Verificar se avançou para a próxima etapa ou se concluiu o processo
            # Uma vez que não conhecemos detalhes exatos do site após essa etapa,
            # vamos tentar detectar elementos genéricos de sucesso ou próxima etapa
            try:
                # Verificar primeiro por um possível sucesso/conclusão
                try:
                    success_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'sucesso') or contains(text(), 'confirmad') or contains(text(), 'Pagamento')]"))
                    )
                    is_success = True
                    logging.info("Terceira etapa preenchida com sucesso - Processo concluído ou passou para etapa de pagamento")
                    self.driver.save_screenshot("processo_concluido.png")
                except (TimeoutException, NoSuchElementException):
                    # Se não encontrou confirmação de sucesso, verificar se foi para outra etapa
                    next_step_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Pagamento') or contains(text(), 'Cartão') or contains(text(), 'Finalizar')]"))
                    )
                    is_success = True
                    logging.info("Terceira etapa preenchida com sucesso - Passou para a próxima etapa")
                    self.driver.save_screenshot("proxima_etapa_carregada.png")
            except (TimeoutException, NoSuchElementException) as e:
                is_success = False
                logging.error(f"Falha ao verificar conclusão da terceira etapa: {str(e)}")
                # Capturar screenshot em caso de erro
                self.driver.save_screenshot("erro_verificacao_etapa3.png")
            
            return is_success
            
        except Exception as e:
            logging.error(f"Erro ao preencher a terceira etapa: {str(e)}")
            # Capturar screenshot em caso de erro
            self.driver.save_screenshot("erro_etapa3.png")
            return False
