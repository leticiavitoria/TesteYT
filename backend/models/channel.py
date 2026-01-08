"""
Modelo de Canal do YouTube com sistema de embeddings vetoriais.
"""

from datetime import datetime
from typing import List, Dict, Optional
import numpy as np


class ChannelVector:
    """
    Representa o vetor Y do canal, composto por sub-vetores:
    - T (Títulos)
    - V (Vídeos/Transcrições)
    - D (Descrições)
    - H (Hashtags)
    - U (Thumbnails)
    """

    def __init__(self):
        self.title_vectors: List[np.ndarray] = []  # T
        self.video_vectors: List[np.ndarray] = []  # V
        self.description_vectors: List[np.ndarray] = []  # D
        self.hashtag_vectors: List[np.ndarray] = []  # H
        self.thumbnail_vectors: List[np.ndarray] = []  # U

    def add_title_vector(self, vector: np.ndarray):
        """Adiciona um vetor de título"""
        self.title_vectors.append(vector)

    def add_video_vector(self, vector: np.ndarray):
        """Adiciona um vetor de transcrição"""
        self.video_vectors.append(vector)

    def add_description_vector(self, vector: np.ndarray):
        """Adiciona um vetor de descrição"""
        self.description_vectors.append(vector)

    def add_hashtag_vector(self, vector: np.ndarray):
        """Adiciona um vetor de hashtags"""
        self.hashtag_vectors.append(vector)

    def add_thumbnail_vector(self, vector: np.ndarray):
        """Adiciona um vetor de thumbnail"""
        self.thumbnail_vectors.append(vector)

    def get_channel_embedding(self) -> Optional[np.ndarray]:
        """
        Calcula o embedding Y do canal como média ponderada dos sub-vetores.
        Peso maior para títulos e vídeos pois são mais importantes.
        """
        vectors = []
        weights = []

        if self.title_vectors:
            vectors.append(np.mean(self.title_vectors, axis=0))
            weights.append(0.30)  # 30% peso para títulos

        if self.video_vectors:
            vectors.append(np.mean(self.video_vectors, axis=0))
            weights.append(0.30)  # 30% peso para conteúdo do vídeo

        if self.description_vectors:
            vectors.append(np.mean(self.description_vectors, axis=0))
            weights.append(0.20)  # 20% peso para descrições

        if self.hashtag_vectors:
            vectors.append(np.mean(self.hashtag_vectors, axis=0))
            weights.append(0.15)  # 15% peso para hashtags

        if self.thumbnail_vectors:
            vectors.append(np.mean(self.thumbnail_vectors, axis=0))
            weights.append(0.05)  # 5% peso para thumbnails

        if not vectors:
            return None

        # Normaliza os pesos
        weights = np.array(weights) / sum(weights)

        # Calcula média ponderada
        channel_embedding = np.average(vectors, axis=0, weights=weights)

        return channel_embedding


class Channel:
    """Modelo completo de um canal do YouTube"""

    def __init__(
        self,
        name: str,
        niche: str,
        sub_niche: str,
        description: str,
        channel_id: Optional[str] = None
    ):
        self.channel_id = channel_id or self._generate_id()
        self.name = name
        self.niche = niche
        self.sub_niche = sub_niche
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # Sistema de vetores
        self.vector = ChannelVector()

        # Dados do canal
        self.keywords: List[str] = []
        self.target_audience: Dict = {}
        self.content_strategy: Dict = {}
        self.videos: List[Dict] = []

        # Métricas e análises
        self.performance_metrics: Dict = {
            'consistency_score': 0.0,  # Coerência vetorial
            'niche_alignment': 0.0,    # Alinhamento com nicho
            'avg_risk_score': 0.0,     # Risco médio dos títulos
            'content_quality': 0.0     # Qualidade do conteúdo
        }

    def _generate_id(self) -> str:
        """Gera ID único para o canal"""
        import uuid
        return f"CH_{uuid.uuid4().hex[:12]}"

    def add_video(self, video_data: Dict):
        """Adiciona um vídeo ao histórico do canal"""
        video_data['added_at'] = datetime.now().isoformat()
        self.videos.append(video_data)
        self.updated_at = datetime.now()

    def update_metrics(self, metrics: Dict):
        """Atualiza as métricas de performance"""
        self.performance_metrics.update(metrics)
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict:
        """Converte o canal para dicionário para serialização"""
        return {
            'channel_id': self.channel_id,
            'name': self.name,
            'niche': self.niche,
            'sub_niche': self.sub_niche,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'keywords': self.keywords,
            'target_audience': self.target_audience,
            'content_strategy': self.content_strategy,
            'videos': self.videos,
            'performance_metrics': self.performance_metrics,
            'vector_stats': {
                'title_vectors_count': len(self.vector.title_vectors),
                'video_vectors_count': len(self.vector.video_vectors),
                'description_vectors_count': len(self.vector.description_vectors),
                'hashtag_vectors_count': len(self.vector.hashtag_vectors),
                'thumbnail_vectors_count': len(self.vector.thumbnail_vectors)
            }
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Channel':
        """Cria um canal a partir de um dicionário"""
        channel = cls(
            name=data['name'],
            niche=data['niche'],
            sub_niche=data['sub_niche'],
            description=data['description'],
            channel_id=data.get('channel_id')
        )

        if 'created_at' in data:
            channel.created_at = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            channel.updated_at = datetime.fromisoformat(data['updated_at'])

        channel.keywords = data.get('keywords', [])
        channel.target_audience = data.get('target_audience', {})
        channel.content_strategy = data.get('content_strategy', {})
        channel.videos = data.get('videos', [])
        channel.performance_metrics = data.get('performance_metrics', channel.performance_metrics)

        return channel
