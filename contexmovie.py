import sys
import xbmc, xbmcgui
from simpleplugin import Plugin


def log(msg: str):
    xbmc.log(f'contextmovie: {msg}')


def create_url() -> str:
    #path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    #if not path:
    li: xbmcgui.ListItem = sys.listitem # type: ignore
    path = li.getPath()
    log(f'path={path}')

    id: str = li.getUniqueID('tmdb')
    vit: xbmc.InfoTagVideo = li.getVideoInfoTag()

    plugin = Plugin()
    url = plugin.get_url(
        action='search',
        id=id,
        mod='torrent',
        query=vit.getTitle(),
        type='movie'
    )
    log(f'url={url}')
    return url


if __name__ == "__main__":
    url = create_url()
    if url:
        xbmc.executebuiltin('ActivateWindow(Videos,%s,return)' % url)
