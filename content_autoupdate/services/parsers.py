import httpx
from bs4 import BeautifulSoup

from content_autoupdate import config


def form_api_url(url: config.Url, domain_name: str) -> config.Url | None:
    """Form api url to get json containing source download url from source"""
    match domain_name:
        case 'wgmods.net':
            return f"{url[:18]}/api/mods{url[18:]}"
        case 'protanki.tv':
            return f"{url[:8]}api.{url[8:20]}v1/{url[20:]}/download/?format=json"


def parse_site(response: httpx.Response, domain_name: str) -> config.Url | None:
    parser_switch = {
        "wotsite.net": _parse_wotsite,     
        "wotspeak.org": _parse_wotspeak,
        "modxvm.com": _parse_modxvm,     
        "wgmods.net": _parse_wgmods,   
        "protanki.tv": _parse_protanki,
    }
    return parser_switch[domain_name](response)


def _parse_wotsite(response: httpx.Response) -> config.Url:
    soup = BeautifulSoup(response.text, "html.parser")
    if any(title in soup.title.string for title in ("Око Саурона", "Ведьмак")):
        return soup.find_all("a", class_="btn-download")[1].get("href")
    return soup.find("a", class_="btn-download").get("href")


def _parse_wotspeak(response: httpx.Response) -> config.Url:
    soup = BeautifulSoup(response.text, "html.parser")
    a = soup.find("a", class_="down_new")
    return a.get("href").split("?xf=")[1].split("&id=")[0]


def _parse_modxvm(response: httpx.Response) -> config.Url | None:
    soup = BeautifulSoup(response.text, "html.parser")
    mod_info = soup.find("table", class_="table table-hover border").findAll("tr")[2]
    if config.ACTUAL_WOT_VERSION in mod_info.text:
        return mod_info.find("a").get("href")


def _parse_wgmods(response: httpx.Response) -> config.Url | None:
    mod_info = response.json().get("versions")[0]
    if mod_info.get("game_version").get("version") == config.ACTUAL_WOT_VERSION:
        return mod_info.get("download_url")


def _parse_protanki(response: httpx.Response) -> config.Url:
    return response.json()

