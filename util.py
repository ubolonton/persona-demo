from warp.runtime import config

def with_base(url):
    base = config.get("baseUrl", "")
    return base + url
