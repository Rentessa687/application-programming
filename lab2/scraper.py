import os
import re
import time
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://sound-effects.ru/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36"
    )
}
TIMEOUT = 30
DELAY = 1.0
AUDIO_EXTENSIONS = (".mp3", ".wav", ".ogg")


def fetch_html(url: str) -> str:
    """
    Загрузка HTML-страницы.
    :param url: адрес страницы
    :return: текст страницы
    """
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    time.sleep(DELAY)
    return response.text


def get_categories(html: str) -> dict[str, str]:
    """
    Поиск всех категорий на странице.
    :param html: текст страницы
    :return: словарь "название в нижнем регистре -> адрес категории"
    """
    soup = BeautifulSoup(html, "html.parser")
    categories = {}
    for link in soup.find_all("a", href=re.compile(r"/category/")):
        name = link.get_text(strip=True).lower()
        if name:
            categories.setdefault(name, urljoin(BASE_URL, link["href"]))
    return categories


def find_category_url(categories: dict[str, str], name: str) -> str:
    """
    Поиск адреса категории по названию без учёта регистра.
    :param categories: словарь категорий
    :param name: название категории
    :return: адрес категории
    """
    url = categories.get(name.strip().lower())
    if url is None:
        raise ValueError(f"Category not found: {name}")
    return url


def get_download_links(html: str) -> list[str]:
    """
    Поиск ссылок "Скачать звук" на странице.
    :param html: текст страницы
    :return: список уникальных ссылок в порядке появления
    """
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for link in soup.find_all("a", href=re.compile(r"download-sound\.php")):
        url = urljoin(BASE_URL, link["href"])
        if url not in links:
            links.append(url)
    return links


def collect_links(category_url: str, count: int) -> list[str]:
    """
    Сбор ссылок на звуки категории с учётом пагинации.
    :param category_url: адрес категории
    :param count: сколько ссылок нужно
    :return: список ссылок (может быть короче, если звуков мало)
    """
    links: list[str] = []
    page = 1
    while len(links) < count:
        url = category_url if page == 1 else f"{category_url}page/{page}/"
        try:
            html = fetch_html(url)
        except requests.HTTPError:
            break
        new_links = [x for x in get_download_links(html) if x not in links]
        if not new_links:
            break
        links.extend(new_links)
        page += 1
    return links[:count]


def get_sound_id(url: str) -> str:
    """
    Получение идентификатора звука из ссылки на скачивание.
    :param url: ссылка вида download-sound.php?post_id=123
    :return: идентификатор звука
    """
    query = parse_qs(urlparse(url).query)
    return query.get("post_id", ["unknown"])[0]


def find_audio_url(html: str, page_url: str) -> str | None:
    """
    Поиск прямой ссылки на аудиофайл в HTML-странице.
    :param html: текст страницы
    :param page_url: адрес страницы
    :return: ссылка на файл или None
    """
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["a", "source", "audio"]):
        href = tag.get("href") or tag.get("src") or ""
        if href.lower().split("?")[0].endswith(AUDIO_EXTENSIONS):
            return urljoin(page_url, href)
    return None


EXTENSIONS = {
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/ogg": ".ogg",
}


def get_filename(response: requests.Response, sound_id: str) -> str:
    """
    Выбор имени файла по ответу сервера.
    :param response: ответ на запрос скачивания
    :param sound_id: идентификатор звука
    :return: имя файла с расширением
    """
    disposition = response.headers.get("Content-Disposition", "")
    match = re.search(r"filename\*?=(?:UTF-8'')?\"?([^\";]+)", disposition)
    if match:
        extension = os.path.splitext(unquote(match.group(1)))[1]
        if extension:
            return f"{sound_id}{extension}"
    content_type = response.headers.get("Content-Type", "").split(";")[0]
    return f"{sound_id}{EXTENSIONS.get(content_type, '.mp3')}"


def download_file(url: str, folder: str) -> str:
    """
    Скачивание одного звука.
    :param url: ссылка на скачивание
    :param folder: папка для сохранения
    :return: абсолютный путь к сохранённому файлу
    """
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    if "text/html" in response.headers.get("Content-Type", ""):
        audio_url = find_audio_url(response.text, response.url)
        if audio_url is None:
            raise ValueError(f"No audio file found at {url}")
        response = requests.get(audio_url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, get_filename(response, get_sound_id(url)))
    with open(path, "wb") as file:
        file.write(response.content)
    time.sleep(DELAY)
    return os.path.abspath(path)
