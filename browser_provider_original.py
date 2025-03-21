import os
import tempfile
import uuid
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import tempfile


class BrowserProvider:
    browser = None
    options = Options()

    def get_browser(self, args: list[str] = None, headless: bool = True, drive_path: str = None, download_dir: str = None):
        new_arg = args if args else self.default_args()

        # Configura as opções
        self.set_options(download_dir, new_arg)
        self.is_headless(headless)

        # Cria o serviço e inicializa o navegador
        if drive_path:
            service = Service(drive_path)
            self.browser = webdriver.Edge(service=service, options=self.options)
        else:
            self.browser = webdriver.Edge(options=self.options)

        return self.browser
    
    def set_options(self, download_dir, args):
        if args:
            for arg in args:
                self.options.add_argument(arg)
        
        if download_dir:
            prefs = {"download.default_directory": download_dir}
            self.options.add_experimental_option("prefs", prefs)

    def is_headless(self, headless: bool):
        n_headless = os.getenv("HEADLESS", "False").lower() == "true"
        if n_headless or headless:
            self.options.add_argument("--headless=new")
            
    def default_args(self):
        return [
            "--no-sandbox",
            "--disable-gpu",
            "--disable-setuid-sandbox",
            "--disable-web-security",
            "--disable-dev-shm-usage",
            "--memory-pressure-off",
            "--ignore-certificate-errors",
            "--disable-features=site-per-process",
            "--incognito",
            "--start-maximized",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-popup-blocking",
            "--disable-sync",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-application-cache",
            "--disable-logging",
            "--log-level=3",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
            "--enable-logging",  # Desabilita logging adicional
            "--v=0",  # Define o nível de verbosidade para 0
        ]