from typing import Any, Dict
import re

import xbmc

from vdlib.kodi.jsonrpc_requests import VideoLibrary
from simpleplugin import Plugin


def get_item_params() -> Dict[str, int]:
    folderPath = xbmc.getInfoLabel("ListItem.FolderPath")
    return get_item_params_path(folderPath)

def get_item_params_path(path: str) -> Dict[str, int]:
    m = re.search(r"season_number=(\d+)&tvshowid=(\d+)", path)
    if m:
        return {"season_number": int(m.group(1)), "tvshowid": int(m.group(2))}

    m = re.search(r'videodb://tvshows/titles/(\d+)/(\d+)/', path)
    if m:
        return {"season_number": int(m.group(2)), "tvshowid": int(m.group(1))}
    return {}


def get_tvshow_details(tvshow_id: int) -> Dict[str, Any]:
    result: Any = VideoLibrary.GetTVShowDetails(
        tvshowid=tvshow_id,
        properties=["originaltitle", "uniqueid"],
    )
    return result.get("tvshowdetails", {})


def create_url(params: Dict[str, int]):
    if not params:
        return

    details = get_tvshow_details(params["tvshowid"])
    if not details:
        return

    tmdbid = details["uniqueid"]["tmdb"]
    query = details["originaltitle"]
    season_number = params["season_number"]

    plugin = Plugin()
    url = plugin.get_url(
        action="search",
        id=tmdbid,
        mod="torrent",
        query=query,
        selSeason=season_number,
        type="tvshow",
    )
    return url


if __name__ == "__main__":
    params = get_item_params()

    url = create_url(params)
    if url:
        xbmc.executebuiltin("Container.Update(%s)" % url)
