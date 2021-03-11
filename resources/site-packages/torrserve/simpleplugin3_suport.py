import sys
import xbmc
import xbmcplugin
import xbmcgui

def create_list_item(item):
    """
    Create an :class:`xbmcgui.ListItem` instance from an item dict
    :param item: a dict of ListItem properties
    :type item: dict
    :return: ListItem instance
    :rtype: xbmcgui.ListItem
    """
    major_version = xbmc.getInfoLabel('System.BuildVersion')[:2]
    if major_version >= '18':
        list_item = xbmcgui.ListItem(label=item.get('label', ''),
                                        label2=item.get('label2', ''),
                                        path=item.get('path', ''),
                                        offscreen=item.get('offscreen', False))
    else:
        list_item = xbmcgui.ListItem(label=item.get('label', ''),
                                        label2=item.get('label2', ''),
                                        path=item.get('path', ''))
    if major_version >= '16':
        art = item.get('art', {})
        art['thumb'] = item.get('thumb', '')
        art['icon'] = item.get('icon', '')
        art['fanart'] = item.get('fanart', '')
        item['art'] = art
        cont_look = item.get('content_lookup')
        if cont_look is not None:
            list_item.setContentLookup(cont_look)
    else:
        list_item.setThumbnailImage(item.get('thumb', ''))
        list_item.setIconImage(item.get('icon', ''))
        list_item.setProperty('fanart_image', item.get('fanart', ''))
    if item.get('art'):
        list_item.setArt(item['art'])
    if item.get('stream_info'):
        for stream, stream_info in item['stream_info'].items():
            list_item.addStreamInfo(stream, stream_info)
    if item.get('info'):
        for media, info in item['info'].items():
            list_item.setInfo(media, info)
    if item.get('context_menu') is not None:
        list_item.addContextMenuItems(item['context_menu'])
    if item.get('subtitles'):
        list_item.setSubtitles(item['subtitles'])
    if item.get('mime'):
        list_item.setMimeType(item['mime'])
    if item.get('properties'):
        for key, value in item['properties'].items():
            list_item.setProperty(key, value)
    if major_version >= '17':
        cast = item.get('cast')
        if cast is not None:
            list_item.setCast(cast)
        db_ids = item.get('online_db_ids')
        if db_ids is not None:
            list_item.setUniqueIDs(db_ids)
        ratings = item.get('ratings')
        if ratings is not None:
            for rating in ratings:
                list_item.setRating(**rating)
    return list_item


def create_listing(listing, succeeded=True, update_listing=False, cache_to_disk=False, sort_methods=None,
                       view_mode=None, content=None, category=None):
    """
    Create a virtual folder listing
    :param context: context object
    :type context: ListContext
    :raises SimplePluginError: if sort_methods parameter is not int, tuple or list
    """
    _handle = int(sys.argv[1])

    if category is not None:
        xbmcplugin.setPluginCategory(_handle, category)
    if content is not None:
        xbmcplugin.setContent(_handle, content)  # This must be at the beginning
    for item in listing:
        is_folder = item.get('is_folder', True)
        if item.get('list_item') is not None:
            list_item = item['list_item']
        else:
            list_item = create_list_item(item)
            if item.get('is_playable'):
                list_item.setProperty('IsPlayable', 'true')
                is_folder = False
        xbmcplugin.addDirectoryItem(_handle, item['url'], list_item, is_folder)
    if sort_methods is not None:
        if isinstance(sort_methods, (int, dict)):
            sort_methods = [sort_methods]
        elif isinstance(sort_methods, (tuple, list)):
            sort_methods = sort_methods
        else:
            raise TypeError(
                'sort_methods parameter must be of int, dict, tuple or list type!')
        for method in sort_methods:
            if isinstance(method, int):
                xbmcplugin.addSortMethod(_handle, method)
            elif isinstance(method, dict):
                xbmcplugin.addSortMethod(_handle, **method)
            else:
                raise TypeError(
                    'method parameter must be of int or dict type!')
                
    xbmcplugin.endOfDirectory(_handle,
                                succeeded,
                                update_listing,
                                cache_to_disk)
    if view_mode is not None:
        xbmc.executebuiltin('Container.SetViewMode({0})'.format(view_mode))
