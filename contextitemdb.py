from typing import Dict
import contextitem
import xbmc

def get_item_params() -> Dict[str, int]:
    season = xbmc.getInfoLabel("ListItem.Season")
    tvshowid = xbmc.getInfoLabel("ListItem.TvShowDBID")

    return {"season_number": int(season), "tvshowid": int(tvshowid)}

contextitem.get_item_params = get_item_params

if __name__ == "__main__":
    url = contextitem.create_url()
    if url:
        xbmc.executebuiltin("Container.Update(%s)" % url)
