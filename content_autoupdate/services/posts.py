from dataclasses import dataclass
import inspect

from content_autoupdate import config


@dataclass(slots=True)
class Post:
    title: str
    supported_wot_version: str
    slug_title: str
    source_url: config.Url
    source_download_url: config.Url | None = None
    main_source_download_url: config.Url | None = None
    file_name: str = ""
    
    @classmethod
    def from_dict(cls, env):
        """Write down only the data necessary for post"""
        return cls(
            **{k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters}
        )


