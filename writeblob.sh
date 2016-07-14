sqlite3 art-2016.sqlite "SELECT quote(thumbnail) FROM images WHERE thumbnail_url = 'http://galleries.burningman.org/include/../filestore/tmp/api_resource_cache/82889_bbe3408f7c71e6bcc6dc11bb9c5e3695.jpg'" \
| cut -d\' -f2                                                   \
| xxd -r -p                                                      \
> testimage.jpg
