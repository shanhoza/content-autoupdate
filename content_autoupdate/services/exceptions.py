class CantGetPostsError(Exception):
    """Program can not get sources urls from the main source"""


class CantGetDownloadUrlsError(Exception):
    """Program can not get download urls on sources"""


class FilesDownloadError(Exception):
    """Something went wrong went while downloading files"""
