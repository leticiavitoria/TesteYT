"""
DNA Semântico do Canal - Implementação do Vetor Y

Este módulo implementa o conceito central descrito no paper:
Y = w_T * T + w_V * V + w_D * D + w_H * H + w_U * U

Onde:
- T (Títulos): Centroide dos vetores de títulos
- V (Vídeos/Transcrições): Centroide dos vetores de roteiros/transcrições
- D (Descrições): Centroide dos vetores de descrições
- H (Hashtags): Centroide dos vetores de tags/hashtags
- U (Thumbnails): Centroide dos vetores de prompts de thumbnail

O DNA Semântico representa a identidade vetorial do canal e evolui
com cada novo conteúdo aprovado.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import json


@dataclass
class VectorComponent:
    """
    Represents a Semantic DNA component (T, V, D, H or U).
    Stores all individual vectors and calculates the centroid.
    """
    nome: str
    vetores: List[np.ndarray] = field(default_factory=list)
    textos: List[str] = field(default_factory=list)
    peso: float = 0.0

    def adicionar_vetor(self, vetor: np.ndarray, texto: str):
        """Adiciona um novo vetor ao componente"""
        self.vetores.append(vetor)
        self.textos.append(texto)

    def calcular_centroide(self) -> Optional[np.ndarray]:
        """
        Calcula o centroide (média vetorial) de todos os vetores.
        Representa o vetor característico deste componente.
        """
        if not self.vetores:
            return None
        return np.mean(self.vetores, axis=0)

    def calcular_densidade_semantica(self) -> float:
        """
        Calcula a densidade semântica do cluster.
        Clusters densos = alta coerência interna.
        """
        if len(self.vetores) < 2:
            return 0.0

        centroide = self.calcular_centroide()
        if centroide is None:
            return 0.0

        # Distâncias de cada vetor ao centroide
        distancias = [
            np.linalg.norm(v - centroide)
            for v in self.vetores
        ]

        # Densidade = inverso da dispersão média
        dispersao_media = np.mean(distancias)
        if dispersao_media == 0:
            return 1.0

        densidade = 1 / (1 + dispersao_media)
        return float(densidade)

    def contar_vetores(self) -> int:
        """Retorna o número de vetores no componente"""
        return len(self.vetores)

    def to_dict(self) -> Dict:
        """Serializa para dicionário (sem os vetores numpy)"""
        return {
            'nome': self.nome,
            'peso': self.peso,
            'quantidade_vetores': len(self.vetores),
            'densidade_semantica': self.calcular_densidade_semantica(),
            'textos': self.textos
        }


class ChannelSemanticDNA:
    """
    Implements the Channel Semantic DNA as specified in the technical document.

    The DNA is composed of 5 vector components, each representing
    an aspect of the channel's metadata and content:

    Y = w_T * T + w_V * V + w_D * D + w_H * H + w_U * U

    Vector coherence between components determines the DNA's "strength".
    """

    def __init__(self, pesos: Optional[Dict[str, float]] = None):
        """
        Inicializa o DNA Semântico com pesos opcionais.

        Args:
            pesos: Dicionário com pesos para cada componente.
                   Se None, usa pesos padrão baseados no documento.
        """
        # Vector components
        self.T = VectorComponent(nome='Títulos', peso=0.30)
        self.V = VectorComponent(nome='Vídeos/Roteiros', peso=0.30)
        self.D = VectorComponent(nome='Descrições', peso=0.20)
        self.H = VectorComponent(nome='Hashtags/Tags', peso=0.15)
        self.U = VectorComponent(nome='Thumbnails', peso=0.05)

        # Aplica pesos personalizados se fornecidos
        if pesos:
            self._aplicar_pesos(pesos)

        # Cache do vetor Y (recalculado quando necessário)
        self._vetor_y_cache: Optional[np.ndarray] = None
        self._cache_valido = False

    def _aplicar_pesos(self, pesos: Dict[str, float]):
        """Aplica pesos personalizados aos componentes"""
        if 'T' in pesos:
            self.T.peso = pesos['T']
        if 'V' in pesos:
            self.V.peso = pesos['V']
        if 'D' in pesos:
            self.D.peso = pesos['D']
        if 'H' in pesos:
            self.H.peso = pesos['H']
        if 'U' in pesos:
            self.U.peso = pesos['U']

        # Normaliza pesos para somarem 1.0
        soma_pesos = self.T.peso + self.V.peso + self.D.peso + self.H.peso + self.U.peso
        if soma_pesos > 0:
            self.T.peso /= soma_pesos
            self.V.peso /= soma_pesos
            self.D.peso /= soma_pesos
            self.H.peso /= soma_pesos
            self.U.peso /= soma_pesos

    def adicionar_titulo(self, vetor: np.ndarray, texto: str):
        """Adiciona um vetor de título ao DNA"""
        self.T.adicionar_vetor(vetor, texto)
        self._cache_valido = False

    def adicionar_video(self, vetor: np.ndarray, texto: str):
        """Adiciona um vetor de roteiro/transcrição ao DNA"""
        self.V.adicionar_vetor(vetor, texto)
        self._cache_valido = False

    def adicionar_descricao(self, vetor: np.ndarray, texto: str):
        """Adiciona um vetor de descrição ao DNA"""
        self.D.adicionar_vetor(vetor, texto)
        self._cache_valido = False

    def adicionar_hashtag(self, vetor: np.ndarray, texto: str):
        """Adiciona um vetor de hashtags ao DNA"""
        self.H.adicionar_vetor(vetor, texto)
        self._cache_valido = False

    def adicionar_thumbnail(self, vetor: np.ndarray, texto: str):
        """Adiciona um vetor de prompt de thumbnail ao DNA"""
        self.U.adicionar_vetor(vetor, texto)
        self._cache_valido = False

    def calcular_vetor_y(self, forcar_recalculo: bool = False) -> Optional[np.ndarray]:
        """
        Calcula o vetor Y do canal como média ponderada dos centroides.

        Y = w_T * T + w_V * V + w_D * D + w_H * H + w_U * U

        Args:
            forcar_recalculo: Se True, recalcula mesmo se o cache for válido

        Returns:
            Vetor Y do canal ou None se não houver dados suficientes
        """
        if self._cache_valido and not forcar_recalculo and self._vetor_y_cache is not None:
            return self._vetor_y_cache

        # Coleta centroides disponíveis com seus pesos
        centroides_ponderados = []
        pesos_efetivos = []

        # T - Títulos
        t_centroide = self.T.calcular_centroide()
        if t_centroide is not None:
            centroides_ponderados.append(t_centroide * self.T.peso)
            pesos_efetivos.append(self.T.peso)

        # V - Vídeos/Roteiros
        v_centroide = self.V.calcular_centroide()
        if v_centroide is not None:
            centroides_ponderados.append(v_centroide * self.V.peso)
            pesos_efetivos.append(self.V.peso)

        # D - Descrições
        d_centroide = self.D.calcular_centroide()
        if d_centroide is not None:
            centroides_ponderados.append(d_centroide * self.D.peso)
            pesos_efetivos.append(self.D.peso)

        # H - Hashtags
        h_centroide = self.H.calcular_centroide()
        if h_centroide is not None:
            centroides_ponderados.append(h_centroide * self.H.peso)
            pesos_efetivos.append(self.H.peso)

        # U - Thumbnails
        u_centroide = self.U.calcular_centroide()
        if u_centroide is not None:
            centroides_ponderados.append(u_centroide * self.U.peso)
            pesos_efetivos.append(self.U.peso)

        if not centroides_ponderados:
            return None

        # Normaliza pelos pesos efetivamente usados
        soma_pesos_efetivos = sum(pesos_efetivos)
        vetor_y = sum(centroides_ponderados) / soma_pesos_efetivos

        # Atualiza cache
        self._vetor_y_cache = vetor_y
        self._cache_valido = True

        return vetor_y

    def calcular_coerencia_vetorial(self) -> Dict[str, float]:
        """
        Calcula a coerência vetorial entre todos os componentes.

        A coerência é medida pela similaridade de cosseno entre
        todos os pares de centroides. Alta coerência = DNA forte.

        Returns:
            Dicionário com similaridades entre pares e coerência média
        """
        centroides = {}

        # Coleta todos os centroides disponíveis
        if self.T.calcular_centroide() is not None:
            centroides['T'] = self.T.calcular_centroide()
        if self.V.calcular_centroide() is not None:
            centroides['V'] = self.V.calcular_centroide()
        if self.D.calcular_centroide() is not None:
            centroides['D'] = self.D.calcular_centroide()
        if self.H.calcular_centroide() is not None:
            centroides['H'] = self.H.calcular_centroide()
        if self.U.calcular_centroide() is not None:
            centroides['U'] = self.U.calcular_centroide()

        if len(centroides) < 2:
            return {
                'coerencia_media': 0.0,
                'pares': {},
                'status': 'dados_insuficientes'
            }

        # Calcula similaridade para todos os pares
        similaridades = {}
        todas_sims = []

        nomes = list(centroides.keys())
        for i, nome1 in enumerate(nomes):
            for nome2 in nomes[i+1:]:
                sim = self._cosine_similarity(centroides[nome1], centroides[nome2])
                chave = f"{nome1}-{nome2}"
                similaridades[chave] = float(sim)
                todas_sims.append(sim)

        coerencia_media = np.mean(todas_sims) if todas_sims else 0.0

        return {
            'coerencia_media': float(coerencia_media),
            'desvio_padrao': float(np.std(todas_sims)) if todas_sims else 0.0,
            'pares': similaridades,
            'status': self._classificar_coerencia(coerencia_media)
        }

    def _classificar_coerencia(self, coerencia: float) -> str:
        """Classifica o nível de coerência do DNA"""
        if coerencia >= 0.7:
            return 'excelente'
        elif coerencia >= 0.5:
            return 'boa'
        elif coerencia >= 0.3:
            return 'moderada'
        else:
            return 'baixa'

    def calcular_ruido_semantico(self) -> float:
        """
        Calcula o ruído semântico do canal.

        Ruído = 1 - Coerência

        Alto ruído indica que os componentes estão "puxando" o DNA
        em direções diferentes, enfraquecendo a identidade do canal.

        Returns:
            Score de ruído (0 = sem ruído, 1 = máximo ruído)
        """
        coerencia = self.calcular_coerencia_vetorial()
        return 1.0 - coerencia['coerencia_media']

    def calcular_magnitude_dna(self) -> float:
        """
        Calcula a magnitude (força) do vetor Y.

        Um DNA coerente terá maior magnitude.
        Vetores que se anulam (baixa coerência) resultam em baixa magnitude.
        """
        vetor_y = self.calcular_vetor_y()
        if vetor_y is None:
            return 0.0
        return float(np.linalg.norm(vetor_y))

    def simular_adicao(
        self,
        vetor: np.ndarray,
        componente: str
    ) -> Dict[str, any]:
        """
        Simula a adição de um novo vetor ao DNA sem efetivamente adicioná-lo.

        Retorna análise do impacto que essa adição teria:
        - Nova coerência vetorial
        - Nova magnitude do DNA
        - Deslocamento do centroide
        - Diluição ou fortalecimento

        Args:
            vetor: O vetor a ser simulado
            componente: 'T', 'V', 'D', 'H' ou 'U'

        Returns:
            Dicionário com análise do impacto
        """
        # Estado atual
        y_atual = self.calcular_vetor_y()
        coerencia_atual = self.calcular_coerencia_vetorial()
        magnitude_atual = self.calcular_magnitude_dna()

        # Simula adição
        componente_obj = getattr(self, componente)
        vetores_backup = componente_obj.vetores.copy()

        componente_obj.vetores.append(vetor)
        self._cache_valido = False

        # Novo estado
        y_novo = self.calcular_vetor_y()
        coerencia_nova = self.calcular_coerencia_vetorial()
        magnitude_nova = self.calcular_magnitude_dna()

        # Restaura estado original
        componente_obj.vetores = vetores_backup
        self._cache_valido = False

        # Calcula impactos
        if y_atual is not None and y_novo is not None:
            deslocamento = np.linalg.norm(y_novo - y_atual)
            angulo_deslocamento = np.arccos(
                np.clip(
                    np.dot(y_atual, y_novo) / (np.linalg.norm(y_atual) * np.linalg.norm(y_novo)),
                    -1.0, 1.0
                )
            )
            angulo_graus = np.degrees(angulo_deslocamento)
        else:
            deslocamento = 0.0
            angulo_graus = 0.0

        delta_coerencia = coerencia_nova['coerencia_media'] - coerencia_atual['coerencia_media']
        delta_magnitude = magnitude_nova - magnitude_atual

        efeito = 'fortalecimento' if delta_magnitude > 0 else 'diluição'

        return {
            'impacto_coerencia': {
                'atual': coerencia_atual['coerencia_media'],
                'nova': coerencia_nova['coerencia_media'],
                'delta': delta_coerencia,
                'percentual': (delta_coerencia / coerencia_atual['coerencia_media'] * 100)
                    if coerencia_atual['coerencia_media'] > 0 else 0
            },
            'impacto_magnitude': {
                'atual': magnitude_atual,
                'nova': magnitude_nova,
                'delta': delta_magnitude,
                'percentual': (delta_magnitude / magnitude_atual * 100)
                    if magnitude_atual > 0 else 0
            },
            'deslocamento_vetor': {
                'distancia': float(deslocamento),
                'angulo_graus': float(angulo_graus)
            },
            'efeito_geral': efeito,
            'recomendacao': self._gerar_recomendacao_simulacao(
                delta_coerencia, delta_magnitude, angulo_graus
            )
        }

    def _gerar_recomendacao_simulacao(
        self,
        delta_coerencia: float,
        delta_magnitude: float,
        angulo: float
    ) -> str:
        """Gera recomendação baseada na simulação"""
        if delta_magnitude > 0 and delta_coerencia > 0:
            return "✅ RECOMENDADO - Fortalece e alinha o DNA do canal"
        elif delta_magnitude > 0 and delta_coerencia >= -0.05:
            return "✅ APROVADO - Fortalece o DNA com impacto neutro na coerência"
        elif delta_magnitude >= 0 and angulo < 15:
            return "⚠️ NEUTRO - Mantém o DNA sem mudanças significativas"
        elif delta_magnitude < 0 and delta_coerencia < 0:
            return "❌ NÃO RECOMENDADO - Dilui e desalinha o DNA do canal"
        else:
            return "⚠️ REVISAR - Impacto misto, avaliar estratégia"

    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calcula similaridade de cosseno entre dois vetores"""
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        return float(dot_product / (norm_v1 * norm_v2))

    def get_estatisticas_completas(self) -> Dict:
        """
        Retorna estatísticas completas do DNA do canal.
        """
        vetor_y = self.calcular_vetor_y()
        coerencia = self.calcular_coerencia_vetorial()

        return {
            'vetor_y_disponivel': vetor_y is not None,
            'magnitude_dna': self.calcular_magnitude_dna(),
            'coerencia_vetorial': coerencia,
            'ruido_semantico': self.calcular_ruido_semantico(),
            'componentes': {
                'T': self.T.to_dict(),
                'V': self.V.to_dict(),
                'D': self.D.to_dict(),
                'H': self.H.to_dict(),
                'U': self.U.to_dict()
            },
            'pesos': {
                'T': self.T.peso,
                'V': self.V.peso,
                'D': self.D.peso,
                'H': self.H.peso,
                'U': self.U.peso
            },
            'analise_forca': self._analisar_forca_dna()
        }

    def _analisar_forca_dna(self) -> Dict:
        """Analisa a força geral do DNA do canal"""
        coerencia = self.calcular_coerencia_vetorial()
        magnitude = self.calcular_magnitude_dna()

        # Critérios de força
        coerencia_score = coerencia['coerencia_media']

        # Quantidade de componentes com dados
        componentes_com_dados = sum([
            1 if self.T.contar_vetores() > 0 else 0,
            1 if self.V.contar_vetores() > 0 else 0,
            1 if self.D.contar_vetores() > 0 else 0,
            1 if self.H.contar_vetores() > 0 else 0,
            1 if self.U.contar_vetores() > 0 else 0
        ])

        completude = componentes_com_dados / 5.0

        # Score geral de força (média ponderada)
        forca_geral = (
            coerencia_score * 0.4 +
            (magnitude / 100) * 0.3 +  # Normaliza magnitude
            completude * 0.3
        )

        if forca_geral >= 0.7:
            classificacao = 'DNA Forte'
            descricao = 'Canal com identidade bem definida e coesa'
        elif forca_geral >= 0.5:
            classificacao = 'DNA Moderado'
            descricao = 'Canal em desenvolvimento, pode melhorar coerência'
        elif forca_geral >= 0.3:
            classificacao = 'DNA Fraco'
            descricao = 'Canal precisa de mais conteúdo consistente'
        else:
            classificacao = 'DNA Inicial'
            descricao = 'Canal em fase inicial, adicione mais conteúdo'

        return {
            'score_forca': float(forca_geral),
            'classificacao': classificacao,
            'descricao': descricao,
            'componentes_ativos': componentes_com_dados,
            'completude': float(completude)
        }
