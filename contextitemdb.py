from typing import Dict
import contextitem
import xbmc

def log(msg: str):
    xbmc.log(f'contextitemdb: {msg}')

def get_item_params() -> Dict[str, int]:
    season = xbmc.getInfoLabel("ListItem.Season")
    tvshowid = xbmc.getInfoLabel("ListItem.TvShowDBID")

    log(f'season={season}, tvshowid={tvshowid}')

    if not season and not tvshowid:
        return {}

    try:
        return {"season_number": int(season), "tvshowid": int(tvshowid)}
    except ValueError:
         # folderPath = 'videodb://tvshows/titles/86/2/?tvshowid=86'
         return {}


def get_item_params2() -> Dict[str, int]:
    path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    # li: xbmcgui.ListItem = sys.listitem # type: ignore
    # dbpath = li.getPath()
    log(f'path={path}')

    return contextitem.get_item_params_path(path)


if __name__ == "__main__":
    params = get_item_params()
    if not params:
        params = get_item_params2()

    url = contextitem.create_url(params)
    if url:
        xbmc.executebuiltin("Container.Update(%s)" % url)
