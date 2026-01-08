"""
Modelo de Vídeo com análise vetorial completa.
"""

from datetime import datetime
from typing import List, Dict, Optional
import numpy as np


class VideoContent:
    """Representa o conteúdo completo de um vídeo"""

    def __init__(self):
        self.title: str = ""
        self.script: str = ""
        self.description: str = ""
        self.tags: List[str] = []
        self.thumbnail_prompt: str = ""

        # Vetores do conteúdo
        self.title_vector: Optional[np.ndarray] = None
        self.script_vector: Optional[np.ndarray] = None
        self.description_vector: Optional[np.ndarray] = None
        self.tags_vector: Optional[np.ndarray] = None

    def get_content_embedding(self) -> Optional[np.ndarray]:
        """Calcula embedding do vídeo completo"""
        vectors = []
        weights = []

        if self.title_vector is not None:
            vectors.append(self.title_vector)
            weights.append(0.35)

        if self.script_vector is not None:
            vectors.append(self.script_vector)
            weights.append(0.40)

        if self.description_vector is not None:
            vectors.append(self.description_vector)
            weights.append(0.15)

        if self.tags_vector is not None:
            vectors.append(self.tags_vector)
            weights.append(0.10)

        if not vectors:
            return None

        weights = np.array(weights) / sum(weights)
        return np.average(vectors, axis=0, weights=weights)


class Video:
    """Modelo completo de um vídeo"""

    def __init__(self, video_id: Optional[str] = None):
        self.video_id = video_id or self._generate_id()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # Conteúdo
        self.content = VideoContent()

        # Análises
        self.analysis: Dict = {
            'title_analysis': {},
            'script_analysis': {},
            'coherence_score': 0.0,
            'risk_score': 0.0,
            'channel_alignment': 0.0,
            'approval_status': 'pending'  # pending, approved, rejected
        }

        # Prompts gerados
        self.generated_prompts: Dict = {
            'script_prompt': '',
            'thumbnail_prompt': '',
            'description_prompt': ''
        }

        # Histórico de versões
        self.versions: List[Dict] = []

    def _generate_id(self) -> str:
        """Gera ID único para o vídeo"""
        import uuid
        return f"VID_{uuid.uuid4().hex[:12]}"

    def update_content(self, **kwargs):
        """Atualiza o conteúdo do vídeo"""
        for key, value in kwargs.items():
            if hasattr(self.content, key):
                setattr(self.content, key, value)
        self.updated_at = datetime.now()

    def add_version(self, version_type: str, data: Dict):
        """Adiciona uma versão ao histórico"""
        version = {
            'type': version_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        self.versions.append(version)

    def update_analysis(self, analysis_data: Dict):
        """Atualiza as análises do vídeo"""
        self.analysis.update(analysis_data)
        self.updated_at = datetime.now()

    def approve(self):
        """Aprova o vídeo"""
        self.analysis['approval_status'] = 'approved'
        self.updated_at = datetime.now()

    def reject(self, reason: str = ""):
        """Rejeita o vídeo"""
        self.analysis['approval_status'] = 'rejected'
        self.analysis['rejection_reason'] = reason
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'video_id': self.video_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'content': {
                'title': self.content.title,
                'script': self.content.script,
                'description': self.content.description,
                'tags': self.content.tags,
                'thumbnail_prompt': self.content.thumbnail_prompt
            },
            'analysis': self.analysis,
            'generated_prompts': self.generated_prompts,
            'versions_count': len(self.versions)
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Video':
        """Cria vídeo a partir de dicionário"""
        video = cls(video_id=data.get('video_id'))

        if 'created_at' in data:
            video.created_at = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            video.updated_at = datetime.fromisoformat(data['updated_at'])

        content_data = data.get('content', {})
        video.content.title = content_data.get('title', '')
        video.content.script = content_data.get('script', '')
        video.content.description = content_data.get('description', '')
        video.content.tags = content_data.get('tags', [])
        video.content.thumbnail_prompt = content_data.get('thumbnail_prompt', '')

        video.analysis = data.get('analysis', video.analysis)
        video.generated_prompts = data.get('generated_prompts', video.generated_prompts)

        return video
