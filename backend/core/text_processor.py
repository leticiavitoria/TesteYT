"""
Processador de Texto Agnóstico de Idioma

Usa análise estatística (TF-IDF) e semântica para identificar termos importantes
automaticamente, SEM listas fixas de stopwords.

Funciona para QUALQUER idioma.
"""

from typing import List, Dict, Tuple
import re
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer


class ProcessadorTexto:
    """
    Processa texto extraindo termos relevantes usando análise estatística.

    **AGNÓSTICO DE IDIOMA** - Funciona com inglês, português, espanhol, etc.

    Usa:
    - TF-IDF para identificar termos importantes
    - Análise de frequência contextual
    - Heurísticas estatísticas (comprimento, variância, etc)
    """

    def __init__(self):
        """
        Inicializa processador sem stopwords fixas.
        Tudo é descoberto estatisticamente.
        """
        self.tfidf_vectorizer = None
        self.corpus_cache = []

    def extrair_palavras_chave(
        self,
        texto: str,
        min_length: int = 3,
        max_palavras: int = 50,
        corpus_contexto: List[str] = None
    ) -> List[str]:
        """
        Extrai palavras-chave usando análise estatística (TF-IDF).

        **AGNÓSTICO DE IDIOMA** - Não usa stopwords fixas.

        Args:
            texto: Texto a processar
            min_length: Comprimento mínimo das palavras
            max_palavras: Número máximo de palavras a retornar
            corpus_contexto: Corpus adicional para TF-IDF (opcional)

        Returns:
            Lista de palavras-chave ordenadas por importância
        """
        # Tokeniza
        tokens = self._tokenizar_basico(texto)

        # Filtra por critérios universais (não dependem de idioma)
        tokens_filtrados = []
        for token in tokens:
            # Remove se:
            # - muito curta (< min_length)
            # - apenas números
            # - apenas caracteres repetidos ('aaa', 'xxx')
            # - caracteres únicos (< 60% de diversidade)
            if (len(token) >= min_length and
                not token.isdigit() and
                len(set(token)) / len(token) >= 0.6 and  # Diversidade mínima
                not self._e_palavra_muito_comum(token, tokens)):  # Frequência local

                tokens_filtrados.append(token)

        # Se temos corpus, usa TF-IDF para ranquear
        if corpus_contexto and len(corpus_contexto) > 1:
            tokens_ranqueados = self._ranquear_por_tfidf(
                texto,
                tokens_filtrados,
                corpus_contexto
            )
        else:
            # Sem corpus, usa heurísticas simples
            tokens_ranqueados = self._ranquear_por_heuristica(tokens_filtrados, tokens)

        # Remove duplicatas mantendo ordem
        palavras_unicas = []
        vistos = set()
        for palavra in tokens_ranqueados:
            if palavra not in vistos:
                palavras_unicas.append(palavra)
                vistos.add(palavra)

        return palavras_unicas[:max_palavras]

    def _tokenizar_basico(self, texto: str) -> List[str]:
        """Tokenização básica agnóstica de idioma"""
        # Lowercase
        texto = texto.lower()

        # Remove pontuação mas mantém estrutura
        texto = re.sub(r'[^\w\s]', ' ', texto)

        # Tokeniza
        tokens = texto.split()

        return tokens

    def _e_palavra_muito_comum(self, palavra: str, todas_palavras: List[str]) -> bool:
        """
        Verifica se palavra é muito comum no texto local (possível stopword).

        Palavras que aparecem > 30% do tempo são consideradas muito comuns.
        """
        frequencia = todas_palavras.count(palavra) / len(todas_palavras)
        return frequencia > 0.3

    def _ranquear_por_heuristica(
        self,
        palavras: List[str],
        todas_palavras: List[str]
    ) -> List[str]:
        """
        Ranqueia palavras por heurísticas estatísticas simples.

        Prioriza:
        - Palavras mais longas (geralmente mais específicas)
        - Palavras menos frequentes (mais raras = mais importantes)
        - Palavras com boa diversidade de caracteres
        """
        scores = []
        counter = Counter(todas_palavras)

        for palavra in palavras:
            # Score baseado em:
            # 1. Comprimento (palavras longas são mais específicas)
            score_comprimento = len(palavra) / 15  # Normaliza para ~1.0

            # 2. Raridade (palavras raras são mais importantes)
            freq = counter[palavra]
            score_raridade = 1 / (1 + freq)

            # 3. Diversidade de caracteres
            score_diversidade = len(set(palavra)) / len(palavra)

            # Score final
            score_total = (
                score_comprimento * 0.3 +
                score_raridade * 0.5 +
                score_diversidade * 0.2
            )

            scores.append((palavra, score_total))

        # Ordena por score (maior primeiro)
        scores.sort(key=lambda x: x[1], reverse=True)

        return [palavra for palavra, _ in scores]

    def _ranquear_por_tfidf(
        self,
        texto: str,
        palavras: List[str],
        corpus: List[str]
    ) -> List[str]:
        """
        Ranqueia palavras usando TF-IDF.

        TF-IDF identifica termos que são:
        - Frequentes no documento (TF alto)
        - Raros no corpus geral (IDF alto)
        """
        try:
            # Prepara corpus (documento atual + contexto)
            documentos = [texto] + corpus

            # Cria vectorizer TF-IDF
            vectorizer = TfidfVectorizer(
                lowercase=True,
                token_pattern=r'\b\w+\b',
                min_df=1,
                max_df=0.8,  # Ignora termos em > 80% dos docs (muito comuns)
                norm='l2'
            )

            # Calcula TF-IDF
            tfidf_matrix = vectorizer.fit_transform(documentos)

            # Pega scores do primeiro documento (nosso texto)
            feature_names = vectorizer.get_feature_names_out()
            scores_doc = tfidf_matrix[0].toarray()[0]

            # Cria dicionário palavra -> score
            word_scores = dict(zip(feature_names, scores_doc))

            # Ranqueia as palavras filtradas por seus scores TF-IDF
            palavras_com_score = [
                (palavra, word_scores.get(palavra, 0))
                for palavra in palavras
            ]

            # Ordena por score (maior primeiro)
            palavras_com_score.sort(key=lambda x: x[1], reverse=True)

            return [palavra for palavra, _ in palavras_com_score]

        except Exception as e:
            # Fallback: usa heurística simples
            return self._ranquear_por_heuristica(palavras, texto.split())

    def tokenizar_para_word2vec(self, texto: str) -> List[str]:
        """
        Tokeniza texto para treinamento do Word2Vec.

        **AGNÓSTICO DE IDIOMA**

        Para Word2Vec, mantemos mais palavras (incluindo algumas "comuns")
        para preservar contexto. Apenas remove palavras MUITO genéricas
        usando análise estatística local.
        """
        # Tokenização básica
        tokens = self._tokenizar_basico(texto)

        # Filtra apenas:
        # - Palavras muito curtas (< 2 caracteres)
        # - Apenas números
        # - Caracteres repetidos
        # - Palavras EXTREMAMENTE comuns (> 40% do texto)
        tokens_filtrados = []
        for token in tokens:
            if (len(token) >= 2 and
                not token.isdigit() and
                len(set(token)) / len(token) >= 0.5 and  # Diversidade mínima
                not self._e_palavra_extremamente_comum(token, tokens)):

                tokens_filtrados.append(token)

        # Se filtrou tudo, retorna original
        return tokens_filtrados if len(tokens_filtrados) > 0 else tokens

    def _e_palavra_extremamente_comum(self, palavra: str, todas_palavras: List[str]) -> bool:
        """
        Verifica se palavra é EXTREMAMENTE comum (> 40% do texto).

        Threshold mais alto que _e_palavra_muito_comum para Word2Vec.
        """
        if len(todas_palavras) == 0:
            return False

        frequencia = todas_palavras.count(palavra) / len(todas_palavras)
        return frequencia > 0.4

    def extrair_termos_compostos(
        self,
        texto: str,
        n_min: int = 2,
        n_max: int = 3
    ) -> List[str]:
        """
        Extrai termos compostos (n-grams) relevantes.

        **AGNÓSTICO DE IDIOMA**

        Exemplos: "machine learning", "análise técnica", "deep learning"

        Args:
            texto: Texto a processar
            n_min: Tamanho mínimo do n-gram
            n_max: Tamanho máximo do n-gram

        Returns:
            Lista de termos compostos
        """
        # Tokeniza
        tokens = self._tokenizar_basico(texto)

        # Filtra tokens muito curtos ou numéricos
        tokens_filtrados = [
            t for t in tokens
            if len(t) >= 3 and not t.isdigit()
        ]

        # Extrai n-grams
        ngrams = []
        for n in range(n_min, n_max + 1):
            for i in range(len(tokens_filtrados) - n + 1):
                ngram = ' '.join(tokens_filtrados[i:i+n])
                ngrams.append(ngram)

        return ngrams

    def calcular_relevancia_termo(
        self,
        termo: str,
        corpus: List[str],
        frequencia_minima: int = 2
    ) -> float:
        """
        Calcula relevância de um termo baseado em TF-IDF simplificado.

        **AGNÓSTICO DE IDIOMA**

        Termos que aparecem em muitos documentos são menos relevantes.

        Args:
            termo: Termo a avaliar
            corpus: Lista de documentos
            frequencia_minima: Mínimo de documentos onde deve aparecer

        Returns:
            Score de relevância (0-1)
        """
        if not corpus:
            return 0.0

        # Conta em quantos documentos o termo aparece
        doc_count = sum(1 for doc in corpus if termo.lower() in doc.lower())

        if doc_count < frequencia_minima:
            return 0.0

        # TF-IDF simplificado
        tf = doc_count / len(corpus)  # Frequência nos docs
        idf = np.log(len(corpus) / (1 + doc_count))  # Inverso da frequência

        return float(tf * idf)
