from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

class Browser:
    """
    Classe para gerenciar o navegador usando Selenium.
    """
    def __init__(self, headless=True):  
        """
        Inicializa o gerenciador de navegador.
        
        Args:
            headless (bool): Se True, o navegador rodará em modo headless (sem interface gráfica).
                             Se False, o navegador será visível durante a execução.
        """
        self.headless = headless
        self.driver = None
        
    def start(self):
        """
        Inicia o navegador e configura as opções.
        
        Returns:
            WebDriver: Instância do WebDriver do Selenium
        """
        logging.info("Iniciando o navegador")
        
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless=new')
        
        # Configurações básicas
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Configurações adicionais para melhorar o desempenho
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--window-size=1920,1080')  # Tamanho da janela padrão
        
        # Adicionar uma política de mesma origem menos restritiva, pode ajudar com iframes
        options.add_argument('--disable-web-security')
        
        # Desativar logs de automação para reduzir ruído no console
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Inicializa o WebDriver com o ChromeDriverManager para baixar automaticamente o driver
        try:
            # Configuração para ambiente de nuvem sem GUI
            chrome_prefs = {}
            options.experimental_options["prefs"] = chrome_prefs
            chrome_prefs["profile.default_content_settings"] = {"images": 2}  # Desabilitar carregar imagens
            chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
            
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            logging.info("Driver do Chrome iniciado com sucesso")
        except Exception as e:
            logging.error(f"Erro ao iniciar o driver do Chrome: {str(e)}")
            raise
        
        # Configura um timeout implícito mais longo
        self.driver.implicitly_wait(15)
        
        # Maximizar janela para telas maiores
        if not self.headless:
            self.driver.maximize_window()
            logging.info("Janela do navegador maximizada")
        
        return self.driver
        
    def close(self):
        """
        Fecha o navegador e libera os recursos.
        """
        logging.info("Fechando o navegador")
        if self.driver:
            self.driver.quit()
