from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import requests
import re
import os
from typing import Iterable
from urllib.parse import urljoin

# --- CONFIGURAÇÃO DO SELENIUM ---
options = webdriver.FirefoxOptions()
# Caminho para o binário do Firefox (ajuste conforme seu ambiente)
options.binary_location = r"C:\Program Files\Firefox Developer Edition\firefox.exe"
service = Service(r".\geckodriver.exe")
driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 10)

# --- CONSTANTES (UTILIZE SUAS PRÓPRIAS URLS) ---
BASE_LIST_URL = "https://example.com/list?page={}"     # URL da página de listagem
BASE_READER_URL = "https://example.com/reader/{id}.html"  # URL base para leitura de galeria

# Cabeçalhos HTTP para requisições de download de imagens
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://example.com/"
}


def get_rendered_soup(url: str, css_selector: str) -> BeautifulSoup:
    """
    Abre a URL via Selenium, aguarda até que o elemento definido por CSS_SELECTOR
    esteja presente e retorna o conteúdo renderizado em um BeautifulSoup.
    """
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    return BeautifulSoup(driver.page_source, "html.parser")


def get_last_list_page() -> int:
    """
    Acessa a primeira página de listagem e retorna o maior número de página disponível.
    Útil para paginar automaticamente até o fim.
    """
    soup = get_rendered_soup(
        BASE_LIST_URL.format(1),
        "div.page-container ul.pagination li"
    )
    page_items = soup.select("div.page-container ul.pagination li")
    # Extrai apenas itens numéricos
    pages = [int(item.get_text()) for item in page_items if item.get_text().isdigit()]
    return max(pages) if pages else 1


def get_gallery_ids_from_list(page: int) -> list[str]:
    """
    Para uma página de listagem (page), retorna todos os IDs de galeria encontrados.
    IDs são extraídos de links como '/gallery/...-12345.html'.
    """
    url = BASE_LIST_URL.format(page)
    soup = get_rendered_soup(url, "div.gallery-item")
    gallery_divs = soup.select("div.gallery-item a.item-link")

    ids: list[str] = []
    pattern = re.compile(r"-([0-9]+)\.html$")
    for a in gallery_divs:
        href = a.get("href", "")
        match = pattern.search(href)
        if match:
            ids.append(match.group(1))
    return ids


def get_page_count_for_gallery(gallery_id: str) -> int:
    """
    Acessa a página do reader da galeria e conta quantas páginas ela possui
    (baseado no número de <option> dentro do <select> de escolha de páginas).
    """
    url = BASE_READER_URL.format(id=gallery_id)
    soup = get_rendered_soup(url, "select#page-select option")
    select = soup.find("select", id="page-select")
    return len(select.find_all("option")) if select else 0


def save_images(gallery_id: str, pages: Iterable[int]) -> int:
    """
    Para cada número de página em `pages`, acessa a URL de download, extrai o
    atributo src da <img class="page-image"> e salva o arquivo localmente
    dentro da pasta `gallery_id`. Retorna a quantidade de imagens baixadas.
    """
    # Headers específicos para download de imagens (pode incluir Accept)
    headers = DEFAULT_HEADERS.copy()
    headers["Accept"] = "image/*"

    session = requests.Session()
    session.headers.update(headers)

    os.makedirs(gallery_id, exist_ok=True)
    saved_count = 0

    for page in pages:
        reader_url = f"{BASE_READER_URL.format(id=gallery_id)}#page={page}"
        soup = get_rendered_soup(reader_url, "img.page-image")

        img = soup.find("img", class_="page-image")
        if not img or not img.get("src"):
            print(f"[Erro] Página {page}: imagem não encontrada.")
            continue

        src = img["src"]
        # Corrige URLs sem protocolo
        src = src if src.startswith("http") else urljoin(reader_url, src)

        resp = session.get(src)
        if resp.status_code == 200:
            ext = os.path.splitext(src)[1] or ".jpg"
            filename = f"{gallery_id}_{page}{ext}"
            path = os.path.join(gallery_id, filename)
            with open(path, "wb") as f:
                f.write(resp.content)
            print(f"[OK] Baixou página {page} → {path}")
            saved_count += 1
        else:
            print(f"[Falha] Página {page}: status {resp.status_code}")

    return saved_count


def main():
    """
    Exemplo de fluxo principal:
    1. Descobre quantas páginas de lista existem.
    2. Para cada página de lista, obtém os IDs de galeria.
    3. Para cada galeria, obtém contagem de páginas e baixa todas as imagens.
    """
    try:
        total_pages = get_last_list_page()
        print(f"Listagem detectada de 1 a {total_pages}.")

        for page in range(1, total_pages + 1):
            print(f"\n** Processando listagem {page} **")
            gallery_ids = get_gallery_ids_from_list(page)

            for gid in gallery_ids:
                page_count = get_page_count_for_gallery(gid)
                if page_count == 0:
                    print(f"Galeria {gid} sem páginas detectadas.")
                    continue
                print(f"Galeria {gid} → {page_count} páginas.")
                baixados = save_images(gid, range(1, page_count + 1))
                print(f"Total de imagens baixadas na galeria {gid}: {baixados}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
