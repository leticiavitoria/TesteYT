"""
Modelos de dados do sistema.
"""

from .channel import Channel, ChannelVector
from .video import Video, VideoContent
from .niche import NicheDatabase

__all__ = [
    'Channel',
    'ChannelVector',
    'Video',
    'VideoContent',
    'NicheDatabase'
]
