# tests/test_frontend.py
import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Caso esteja utilizando o ChromeDriver, certifique-se que ele esteja no PATH ou especifique o caminho
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

def test_frontend_load(driver):
    """
    Abre o arquivo index.html do frontend e verifica se ele contém a palavra 'GeoChain'.
    """
    file_path = "file://" + os.path.abspath(os.path.join("frontend", "index.html"))
    driver.get(file_path)
    # Aguarda alguns segundos para que os scripts carreguem
    time.sleep(2)
    assert "GeoChain" in driver.page_source, "O conteúdo esperado não foi encontrado na página do frontend"
