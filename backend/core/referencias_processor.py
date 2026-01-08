"""
Processador de Referências para Criação de Canal

Implementa o sistema descrito na Parte 3 do documento:
- Função criar_canal() com referências obrigatórias
- Treinamento de Word2Vec exclusivamente com referências fornecidas
- Construção do DNA Semântico inicial baseado em referências

REGRA FUNDAMENTAL: Nenhum dado externo ou pre-definido é usado.
Tudo é inferido a partir das referências fornecidas pelo usuário.
"""

import re
import numpy as np
from typing import List, Dict, Optional, Tuple
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass


@dataclass
class Referencia:
    """Representa uma referência de vídeo de sucesso"""
    titulo: str
    descricao: Optional[str] = None
    transcricao: Optional[str] = None
    tags: Optional[List[str]] = None


class ProcessadorReferencias:
    """
    Processa referências de vídeos de sucesso para criar o universo semântico do canal.

    Este é o ponto de entrada OBRIGATÓRIO para criação de canais.
    Sem referências, não há como criar o modelo Word2Vec personalizado.
    """

    def __init__(self):
        # Modelo de embeddings semânticos (multilingual)
        self.sentence_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

        # Modelo Word2Vec (será treinado com referências)
        self.word2vec_model: Optional[Word2Vec] = None

        # Corpus construído a partir das referências
        self.corpus_referencias: List[List[str]] = []

        # Referências processadas
        self.referencias_virais: List[Dict] = []

    def processar_referencias(
        self,
        referencias: List[Referencia],
        subnicho: str,
        resumo_ideia: str
    ) -> Dict:
        """
        Processa referências e cria o universo semântico do canal.

        Args:
            referencias: Lista de vídeos de referência (títulos, descrições, transcrições)
            subnicho: Campo temático específico do canal
            resumo_ideia: Descrição do público-alvo, estilo e objetivos

        Returns:
            Dicionário com modelo Word2Vec, vetores iniciais e análise
        """

        if not referencias or len(referencias) == 0:
            raise ValueError(
                "❌ ERRO: Referências são OBRIGATÓRIAS para criar um canal.\n"
                "Forneça pelo menos 3-5 títulos de vídeos de sucesso no seu nicho."
            )

        # 1. Constrói o corpus a partir das referências
        self._construir_corpus_referencias(referencias, subnicho, resumo_ideia)

        # 2. Treina o Word2Vec EXCLUSIVAMENTE com este corpus
        self._treinar_word2vec()

        # 3. Gera embeddings para cada referência
        referencias_processadas = self._gerar_embeddings_referencias(referencias)

        # 4. Extrai vocabulário característico do nicho
        vocabulario_nicho = self._extrair_vocabulario_nicho()

        # 5. Identifica clusters de tópicos
        clusters_topicos = self._identificar_clusters_topicos()

        return {
            'word2vec_model': self.word2vec_model,
            'referencias_virais': referencias_processadas,
            'vocabulario_nicho': vocabulario_nicho,
            'clusters_topicos': clusters_topicos,
            'corpus_size': len(self.corpus_referencias),
            'vocab_size': len(self.word2vec_model.wv) if self.word2vec_model else 0,
            'analise_inicial': self._gerar_analise_inicial(
                referencias,
                subnicho,
                resumo_ideia
            )
        }

    def _construir_corpus_referencias(
        self,
        referencias: List[Referencia],
        subnicho: str,
        resumo_ideia: str
    ):
        """
        Constrói o corpus de treinamento a partir das referências.

        IMPORTANTE: Este é o ÚNICO corpus usado. Nada mais é adicionado.
        """
        self.corpus_referencias = []

        # Adiciona o subnicho e resumo como contexto base
        self.corpus_referencias.append(self._tokenizar(subnicho))
        self.corpus_referencias.append(self._tokenizar(resumo_ideia))

        # Processa cada referência
        for ref in referencias:
            # Título (sempre presente)
            if ref.titulo:
                self.corpus_referencias.append(self._tokenizar(ref.titulo))

            # Descrição (se disponível)
            if ref.descricao:
                # Divide em sentenças para melhor contexto
                sentencas = self._dividir_em_sentencas(ref.descricao)
                for sentenca in sentencas:
                    self.corpus_referencias.append(self._tokenizar(sentenca))

            # Transcrição (se disponível - mais importante)
            if ref.transcricao:
                # Divide em sentenças
                sentencas = self._dividir_em_sentencas(ref.transcricao)
                for sentenca in sentencas:
                    tokens = self._tokenizar(sentenca)
                    if len(tokens) > 3:  # Ignora sentenças muito curtas
                        self.corpus_referencias.append(tokens)

            # Tags (se disponíveis)
            if ref.tags:
                self.corpus_referencias.append([tag.lower() for tag in ref.tags])

    def _tokenizar(self, texto: str) -> List[str]:
        """
        Tokeniza texto mantendo contexto semântico.

        Não usa stopwords! O Word2Vec precisa de contexto completo.
        """
        # Lowercase
        texto = texto.lower()

        # Remove caracteres especiais mas mantém estrutura
        texto = re.sub(r'[^\w\s]', ' ', texto)

        # Tokeniza
        tokens = texto.split()

        # Remove tokens muito curtos (< 2 caracteres)
        tokens = [t for t in tokens if len(t) >= 2]

        return tokens

    def _dividir_em_sentencas(self, texto: str) -> List[str]:
        """Divide texto em sentenças"""
        # Divide por pontuação de fim de sentença
        sentencas = re.split(r'[.!?]+', texto)

        # Remove sentenças vazias
        sentencas = [s.strip() for s in sentencas if s.strip()]

        return sentencas

    def _treinar_word2vec(self):
        """
        Treina o modelo Word2Vec com o corpus de referências.

        Parâmetros otimizados para:
        - Capturar relações semânticas profundas
        - Funcionar bem com corpus pequeno/médio
        - Generalizar para conteúdo similar
        """
        if not self.corpus_referencias:
            raise ValueError("Corpus vazio - não é possível treinar Word2Vec")

        # Parâmetros do modelo
        self.word2vec_model = Word2Vec(
            sentences=self.corpus_referencias,
            vector_size=100,       # Dimensão dos vetores
            window=5,              # Janela de contexto
            min_count=1,           # Mantém palavras raras (corpus pequeno)
            workers=4,             # Processamento paralelo
            sg=1,                  # Skip-gram (melhor para corpus pequeno)
            hs=0,                  # Negative sampling
            negative=5,            # Número de amostras negativas
            epochs=20,             # Mais épocas para corpus pequeno
            alpha=0.025,           # Taxa de aprendizado inicial
            min_alpha=0.0001       # Taxa de aprendizado final
        )

    def _gerar_embeddings_referencias(
        self,
        referencias: List[Referencia]
    ) -> List[Dict]:
        """
        Gera embeddings para todas as referências usando sentence-transformers.

        Estes embeddings servirão como "padrões virais" para comparação.
        """
        referencias_processadas = []

        for ref in referencias:
            # Embedding do título
            vetor_titulo = self.sentence_model.encode(ref.titulo)

            item = {
                'titulo': ref.titulo,
                'vetor_titulo': vetor_titulo,
                'descricao': ref.descricao,
                'tags': ref.tags
            }

            # Embedding da descrição (se disponível)
            if ref.descricao:
                item['vetor_descricao'] = self.sentence_model.encode(ref.descricao)

            # Embedding da transcrição (se disponível)
            if ref.transcricao:
                # Para transcrições longas, pega os primeiros 500 caracteres
                # (sentence-transformers tem limite de tokens)
                transcricao_resumida = ref.transcricao[:500]
                item['vetor_transcricao'] = self.sentence_model.encode(transcricao_resumida)

            referencias_processadas.append(item)

        self.referencias_virais = referencias_processadas
        return referencias_processadas

    def _extrair_vocabulario_nicho(self, top_n: int = 50) -> List[Dict]:
        """
        Extrai as palavras mais características do nicho.

        Usa frequência + centralidade no grafo semântico do Word2Vec.
        """
        if not self.word2vec_model:
            return []

        # Conta frequência de cada palavra no corpus
        from collections import Counter
        todas_palavras = []
        for sentenca in self.corpus_referencias:
            todas_palavras.extend(sentenca)

        freq_palavras = Counter(todas_palavras)

        # Para cada palavra frequente, calcula sua centralidade semântica
        vocabulario = []

        for palavra, freq in freq_palavras.most_common(top_n * 2):
            if palavra not in self.word2vec_model.wv:
                continue

            try:
                # Palavras semanticamente relacionadas
                similares = self.word2vec_model.wv.most_similar(palavra, topn=10)

                # Centralidade = média da similaridade com palavras próximas
                centralidade = np.mean([sim for _, sim in similares])

                vocabulario.append({
                    'palavra': palavra,
                    'frequencia': freq,
                    'centralidade': float(centralidade),
                    'score': freq * centralidade,  # Score combinado
                    'palavras_relacionadas': [p for p, _ in similares[:5]]
                })
            except:
                continue

        # Ordena por score combinado
        vocabulario.sort(key=lambda x: x['score'], reverse=True)

        return vocabulario[:top_n]

    def _identificar_clusters_topicos(self) -> List[Dict]:
        """
        Identifica clusters de tópicos no corpus de referências.

        Usa Word2Vec para agrupar palavras semanticamente relacionadas.
        """
        if not self.word2vec_model:
            return []

        # Pega palavras mais frequentes
        vocabulario = self._extrair_vocabulario_nicho(top_n=30)

        if not vocabulario:
            return []

        # Agrupa palavras em clusters usando similaridade
        from sklearn.cluster import AgglomerativeClustering

        # Extrai vetores das palavras
        palavras = [item['palavra'] for item in vocabulario]
        vetores = [self.word2vec_model.wv[p] for p in palavras]

        # Clustering hierárquico
        n_clusters = min(5, len(palavras) // 3)  # Máximo 5 clusters

        if n_clusters < 2:
            return [{
                'cluster_id': 0,
                'topico': 'Geral',
                'palavras_chave': palavras[:10]
            }]

        clustering = AgglomerativeClustering(
            n_clusters=n_clusters,
            linkage='average'
        )

        labels = clustering.fit_predict(vetores)

        # Organiza clusters
        clusters = []
        for cluster_id in range(n_clusters):
            palavras_cluster = [
                palavras[i] for i in range(len(palavras))
                if labels[i] == cluster_id
            ]

            if palavras_cluster:
                clusters.append({
                    'cluster_id': cluster_id,
                    'topico': self._nomear_cluster(palavras_cluster),
                    'palavras_chave': palavras_cluster[:10]
                })

        return clusters

    def _nomear_cluster(self, palavras: List[str]) -> str:
        """Tenta nomear o cluster baseado nas palavras principais"""
        # Pega as 3 primeiras palavras como nome do tópico
        return ' | '.join(palavras[:3])

    def _gerar_analise_inicial(
        self,
        referencias: List[Referencia],
        subnicho: str,
        resumo_ideia: str
    ) -> Dict:
        """
        Gera análise inicial do canal baseada nas referências.
        """
        vocabulario = self._extrair_vocabulario_nicho(top_n=20)
        clusters = self._identificar_clusters_topicos()

        # Extrai padrões de título das referências
        padroes_titulo = self._analisar_padroes_titulos(referencias)

        return {
            'subnicho_identificado': subnicho,
            'total_referencias': len(referencias),
            'corpus_size': len(self.corpus_referencias),
            'vocabulario_core': [v['palavra'] for v in vocabulario[:10]],
            'topicos_principais': [c['topico'] for c in clusters],
            'padroes_titulo': padroes_titulo,
            'recomendacoes_iniciais': self._gerar_recomendacoes_iniciais(
                vocabulario,
                clusters,
                padroes_titulo
            )
        }

    def _analisar_padroes_titulos(
        self,
        referencias: List[Referencia]
    ) -> Dict:
        """Analisa padrões estruturais nos títulos de referência"""
        titulos = [ref.titulo for ref in referencias]

        # Comprimento médio
        comprimentos = [len(t) for t in titulos]
        comprimento_medio = np.mean(comprimentos)

        # Contagem de palavras
        palavras = [len(t.split()) for t in titulos]
        palavras_medio = np.mean(palavras)

        # Uso de números
        usa_numeros = sum(1 for t in titulos if re.search(r'\d+', t))

        # Uso de perguntas
        usa_pergunta = sum(1 for t in titulos if '?' in t)

        # Capitalização
        usa_title_case = sum(1 for t in titulos if t.istitle())

        return {
            'comprimento_medio_caracteres': int(comprimento_medio),
            'palavras_medio': int(palavras_medio),
            'uso_numeros_percent': int(usa_numeros / len(titulos) * 100),
            'uso_pergunta_percent': int(usa_pergunta / len(titulos) * 100),
            'usa_title_case_percent': int(usa_title_case / len(titulos) * 100)
        }

    def _gerar_recomendacoes_iniciais(
        self,
        vocabulario: List[Dict],
        clusters: List[Dict],
        padroes: Dict
    ) -> List[str]:
        """Gera recomendações iniciais baseadas na análise"""
        recs = []

        recs.append(
            f"✅ Canal configurado com {len(vocabulario)} palavras-chave principais do nicho"
        )

        if clusters:
            recs.append(
                f"📊 Identificados {len(clusters)} tópicos principais: "
                f"{', '.join([c['topico'] for c in clusters[:3]])}"
            )

        recs.append(
            f"📏 Títulos de referência têm em média {padroes['comprimento_medio_caracteres']} "
            f"caracteres e {padroes['palavras_medio']} palavras"
        )

        if padroes['uso_numeros_percent'] > 50:
            recs.append(
                f"🔢 {padroes['uso_numeros_percent']}% dos títulos usam números - "
                "considere usar em seus títulos"
            )

        return recs
