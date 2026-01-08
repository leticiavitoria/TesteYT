"""
Sistema de persistência de dados.
Salva canais e todo o histórico de aprendizado.
"""

import json
import os
from typing import Dict, List, Optional
import numpy as np


class ChannelStorage:
    """Gerencia persistência de canais e dados de aprendizado"""

    def __init__(self, storage_dir: str = "data/channels"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_channel(self, channel_data: Dict, learning_data: Dict) -> bool:
        """
        Salva canal e dados de aprendizado.
        """
        channel_id = channel_data.get('channel_id')
        if not channel_id:
            return False

        channel_file = os.path.join(self.storage_dir, f"{channel_id}.json")

        # Prepara dados para salvar (converte numpy arrays para listas)
        save_data = {
            'channel': channel_data,
            'learning': self._serialize_learning_data(learning_data)
        }

        try:
            with open(channel_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar canal: {e}")
            return False

    def load_channel(self, channel_id: str) -> Optional[Dict]:
        """Carrega canal e dados de aprendizado"""
        channel_file = os.path.join(self.storage_dir, f"{channel_id}.json")

        if not os.path.exists(channel_file):
            return None

        try:
            with open(channel_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Erro ao carregar canal: {e}")
            return None

    def list_channels(self) -> List[Dict]:
        """Lista todos os canais salvos"""
        channels = []

        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                channel_id = filename[:-5]
                data = self.load_channel(channel_id)
                if data:
                    channels.append({
                        'channel_id': channel_id,
                        'name': data['channel'].get('name', 'Sem nome'),
                        'sub_niche': data['channel'].get('sub_niche', ''),
                        'created_at': data['channel'].get('created_at', ''),
                        'videos_count': len(data['channel'].get('videos', []))
                    })

        return channels

    def delete_channel(self, channel_id: str) -> bool:
        """Deleta um canal"""
        channel_file = os.path.join(self.storage_dir, f"{channel_id}.json")

        if os.path.exists(channel_file):
            try:
                os.remove(channel_file)
                return True
            except Exception as e:
                print(f"Erro ao deletar canal: {e}")
                return False

        return False

    def _serialize_learning_data(self, learning_data: Dict) -> Dict:
        """Serializa dados de aprendizado (converte numpy para JSON)"""
        serialized = {}

        for key, value in learning_data.items():
            if isinstance(value, np.ndarray):
                serialized[key] = value.tolist()
            elif isinstance(value, dict):
                serialized[key] = self._serialize_learning_data(value)
            elif isinstance(value, list):
                serialized[key] = [
                    item.tolist() if isinstance(item, np.ndarray) else item
                    for item in value
                ]
            else:
                serialized[key] = value

        return serialized
