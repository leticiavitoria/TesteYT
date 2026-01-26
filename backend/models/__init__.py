"""
Modelos de dados do sistema.
"""

from .channel import Channel, ChannelVector
from .video import Video, VideoContent
# from .niche import NicheDatabase  # Not implemented yet

__all__ = [
    'Channel',
    'ChannelVector',
    'Video',
    'VideoContent',
    # 'NicheDatabase'  # Not implemented yet
]
