import os
import random
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class BrowserProvider:
    def __init__(self):
        self.browser = None
        self.options = Options()

    def get_browser(self, args: list[str] = None, headless: bool = False, driver_path: str = None, download_dir: str = None):
        new_args = args if args else self.default_args()

        # Configura as opções do navegador
        self.set_options(download_dir, new_args)
        self.is_headless(headless)

        # Inicializa o navegador
        if driver_path:
            service = Service(driver_path)
            self.browser = webdriver.Edge(service=service, options=self.options)
        else:
            self.browser = webdriver.Edge(options=self.options)

        # Aplica técnicas contra detecção
        self._bypass_bot_detection()

        return self.browser

    def set_options(self, download_dir, args):
        if args:
            for arg in args:
                self.options.add_argument(arg)

        if download_dir:
            prefs = {"download.default_directory": download_dir}
            self.options.add_experimental_option("prefs", prefs)

        # Remove sinais de automação
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)

        # Usa um perfil de usuário real
        user_data_dir = os.path.join(os.getcwd(), "edge_profile")
        self.options.add_argument(f"--user-data-dir={user_data_dir}")

        # Define um User-Agent aleatório
        self.options.add_argument(f"--user-agent={self._random_user_agent()}")

    def is_headless(self, headless: bool):
        n_headless = os.getenv("HEADLESS", "False").lower() == "true"
        if n_headless or headless:
            self.options.add_argument("--headless=new")

    def _bypass_bot_detection(self):
        """Remove sinais de automação no navegador após inicializar."""
        if self.browser:
            self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.browser.delete_all_cookies()
            self.browser.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")

    def default_args(self):
        """Argumentos padrão para melhorar performance e evitar bloqueios."""
        return [
            "--no-sandbox",
            "--disable-gpu",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--ignore-certificate-errors",
            "--disable-popup-blocking",
            "--disable-sync",
            "--start-maximized",
            "--disable-logging",
            "--log-level=3",
            "--inprivate"
        ]

    def _random_user_agent(self):
        """Seleciona um User-Agent aleatório para evitar detecção."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        ]
        return random.choice(user_agents)

    def human_delay(self, min_time=0.5, max_time=2.0):
        """Simula um atraso humano aleatório."""
        time.sleep(random.uniform(min_time, max_time))

    def human_click(self, element):
        """Realiza um clique humano no elemento."""
        ActionChains(self.browser).move_to_element(element).click().perform()
        self.human_delay()


# Exemplo de uso: