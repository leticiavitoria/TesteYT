"""
Sistema de Análise Vetorial Adaptativo usando Word2Vec.
Aprende com os dados fornecidos pelo usuário e evolui continuamente.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer
import re
from collections import defaultdict

try:
    from .text_processor import TextProcessor
except ImportError:
    # Fallback if module doesn't exist yet
    class TextProcessor:
        def tokenizar_para_word2vec(self, texto):
            return texto.lower().split()
        def extrair_palavras_chave(self, texto, **kwargs):
            return [w for w in texto.lower().split() if len(w) >= 3]


class AdaptiveVectorAnalyzer:
    """
    Analisador vetorial que aprende e se adapta ao canal específico.
    Não usa parâmetros fixos - descobre padrões automaticamente.
    """

    def __init__(self):
        # Modelo de embeddings semânticos (multilingual)
        self.sentence_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

        # Word2Vec que será treinado com os dados do canal
        self.word2vec_model: Optional[Word2Vec] = None

        # Histórico de vetores do canal
        self.channel_vectors = {
            'titles': [],
            'descriptions': [],
            'scripts': [],
            'tags': []
        }

        # Padrões descobertos automaticamente
        self.discovered_patterns = {
            'title_structure': [],
            'word_patterns': [],
            'length_patterns': [],
            'style_patterns': []
        }

        # Corpus para treinar Word2Vec
        self.training_corpus = []

        # Text processor with stopwords
        self.text_processor = TextProcessor()

    def add_training_data(self, text: str, content_type: str):
        """
        Adiciona dados para treinar o modelo.
        O modelo aprende com cada novo conteúdo.
        """
        # Preprocessa e tokeniza
        tokens = self._preprocess_text(text)
        self.training_corpus.append(tokens)

        # Cria embedding
        vector = self.sentence_model.encode(text)

        # Armazena no histórico
        if content_type in self.channel_vectors:
            self.channel_vectors[content_type].append({
                'text': text,
                'vector': vector,
                'tokens': tokens
            })

        # Re-treina Word2Vec se tivermos dados suficientes
        if len(self.training_corpus) >= 3:
            self._train_word2vec()

    def _preprocess_text(self, text: str) -> List[str]:
        """Preprocessa texto removendo stopwords e mantendo termos relevantes"""
        # Usa o processador de texto para tokenizar
        tokens = self.text_processor.tokenizar_para_word2vec(text)
        return tokens if tokens else text.lower().split()

    def _train_word2vec(self):
        """
        Treina/atualiza o modelo Word2Vec com os dados do canal.
        Modelo evolui com novos dados.
        """
        try:
            if self.word2vec_model is None:
                # Primeira vez: cria o modelo
                self.word2vec_model = Word2Vec(
                    sentences=self.training_corpus,
                    vector_size=100,
                    window=5,
                    min_count=1,
                    workers=4,
                    sg=1  # Skip-gram
                )
            else:
                # Atualiza modelo existente com novos dados
                self.word2vec_model.build_vocab(self.training_corpus, update=True)
                self.word2vec_model.train(
                    self.training_corpus,
                    total_examples=len(self.training_corpus),
                    epochs=10
                )
        except Exception as e:
            print(f"Erro ao treinar Word2Vec: {e}")

    def analyze_title(self, title: str, channel_context: Dict) -> Dict:
        """
        Analisa título baseado no APRENDIZADO do canal.
        Não usa métricas fixas - compara com padrões aprendidos.
        """
        title_vector = self.sentence_model.encode(title)
        title_tokens = self._preprocess_text(title)

        # Descobre padrões automaticamente
        analysis = {
            'vector': title_vector,
            'coherence_with_channel': self._calculate_channel_coherence(
                title_vector, 'titles'
            ),
            'discovered_structure': self._discover_structure(title, title_tokens),
            'pattern_match': self._match_learned_patterns(title_tokens),
            'semantic_analysis': self._analyze_semantics(title, channel_context),
            'risk_assessment': self._assess_risk_adaptive(title, title_vector),
            'recommendations': []
        }

        # Gera recomendações baseadas no aprendizado
        analysis['recommendations'] = self._generate_adaptive_recommendations(analysis)

        return analysis

    def _calculate_channel_coherence(self, vector: np.ndarray, content_type: str) -> Dict:
        """
        Calcula coerência com o vetor do canal.
        Compara com histórico aprendido.
        """
        if not self.channel_vectors[content_type]:
            return {
                'score': 0.5,
                'message': 'Primeiro conteúdo - criando baseline',
                'is_coherent': True
            }

        # Calcula similaridade com todos os vetores anteriores
        similarities = []
        for item in self.channel_vectors[content_type]:
            sim = self._cosine_similarity(vector, item['vector'])
            similarities.append(sim)

        avg_similarity = np.mean(similarities)
        std_similarity = np.std(similarities)

        # Define coerência baseado em padrões aprendidos
        is_coherent = avg_similarity > 0.4  # Adaptativo

        return {
            'score': float(avg_similarity),
            'std_dev': float(std_similarity),
            'is_coherent': is_coherent,
            'comparison_count': len(similarities),
            'message': self._generate_coherence_message(avg_similarity, is_coherent)
        }

    def _discover_structure(self, text: str, tokens: List[str]) -> Dict:
        """
        Descobre a estrutura do texto automaticamente.
        Aprende padrões sem regras pré-definidas.
        """
        structure = {
            'length': len(text),
            'word_count': len(tokens),
            'avg_word_length': np.mean([len(w) for w in tokens]) if tokens else 0,
            'capitalization_pattern': self._detect_capitalization_pattern(text),
            'punctuation_pattern': self._detect_punctuation_pattern(text),
            'number_usage': self._detect_number_usage(text),
            'question_form': '?' in text,
            'exclamation': '!' in text
        }

        # Compara com estruturas anteriores
        if self.discovered_patterns['title_structure']:
            structure['similarity_to_learned'] = self._compare_with_learned_structures(structure)

        return structure

    def _detect_capitalization_pattern(self, text: str) -> str:
        """Detecta padrão de capitalização"""
        if text.isupper():
            return 'all_caps'
        elif text.istitle():
            return 'title_case'
        elif text[0].isupper() if text else False:
            return 'sentence_case'
        else:
            return 'lowercase'

    def _detect_punctuation_pattern(self, text: str) -> Dict:
        """Detecta padrão de pontuação"""
        return {
            'exclamations': text.count('!'),
            'questions': text.count('?'),
            'dots': text.count('.'),
            'commas': text.count(','),
            'has_emoji': bool(re.search(r'[\U0001F600-\U0001F64F]', text))
        }

    def _detect_number_usage(self, text: str) -> Dict:
        """Detecta uso de números"""
        numbers = re.findall(r'\d+', text)
        return {
            'has_numbers': len(numbers) > 0,
            'count': len(numbers),
            'numbers': numbers
        }

    def _match_learned_patterns(self, tokens: List[str]) -> Dict:
        """
        Compara com padrões aprendidos de conteúdos anteriores.
        """
        if not self.word2vec_model or not self.discovered_patterns['word_patterns']:
            return {
                'matches': [],
                'score': 0.0,
                'learning_phase': True
            }

        # Busca palavras similares no vocabulário aprendido
        similar_words = []
        for token in tokens:
            try:
                if token in self.word2vec_model.wv:
                    most_similar = self.word2vec_model.wv.most_similar(token, topn=3)
                    similar_words.append({
                        'word': token,
                        'similar': most_similar
                    })
            except:
                continue

        return {
            'matches': similar_words,
            'score': len(similar_words) / len(tokens) if tokens else 0,
            'learning_phase': False
        }

    def _analyze_semantics(self, text: str, channel_context: Dict) -> Dict:
        """
        Análise semântica baseada no contexto do canal.
        Compara semanticamente com a descrição e objetivos do canal.
        """
        text_vector = self.sentence_model.encode(text)

        # Compara com descrição do canal
        channel_desc = channel_context.get('description', '')
        if channel_desc:
            desc_vector = self.sentence_model.encode(channel_desc)
            semantic_similarity = self._cosine_similarity(text_vector, desc_vector)
        else:
            semantic_similarity = 0.5

        return {
            'channel_alignment': float(semantic_similarity),
            'is_aligned': semantic_similarity > 0.3,
            'message': self._generate_semantic_message(semantic_similarity)
        }

    def _assess_risk_adaptive(self, text: str, vector: np.ndarray) -> Dict:
        """
        Avaliação de risco adaptativa.
        Aprende o que funciona para ESTE canal específico.
        """
        # Se temos histórico, compara com conteúdos de sucesso
        if len(self.channel_vectors['titles']) > 5:
            risk_score = self._calculate_risk_from_history(vector)
        else:
            # Fase de aprendizado - análise básica
            risk_score = 0.5

        return {
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'based_on': 'historical_data' if len(self.channel_vectors['titles']) > 5 else 'baseline',
            'confidence': min(len(self.channel_vectors['titles']) / 10, 1.0)
        }

    def _calculate_risk_from_history(self, vector: np.ndarray) -> float:
        """
        Calcula risco baseado em histórico.
        Quanto mais diferente do padrão estabelecido, maior o risco.
        """
        similarities = [
            self._cosine_similarity(vector, item['vector'])
            for item in self.channel_vectors['titles']
        ]

        avg_sim = np.mean(similarities)

        # Risco inversamente proporcional à similaridade
        risk = 1 - avg_sim
        return float(risk)

    def _get_risk_level(self, score: float) -> str:
        """Determina nível de risco"""
        if score < 0.3:
            return 'baixo'
        elif score < 0.6:
            return 'médio'
        else:
            return 'alto'

    def _generate_adaptive_recommendations(self, analysis: Dict) -> List[str]:
        """
        Gera recomendações baseadas no aprendizado.
        Não usa regras fixas.
        """
        recommendations = []

        coherence = analysis['coherence_with_channel']
        if not coherence['is_coherent'] and coherence['comparison_count'] > 0:
            recommendations.append(
                f"⚠️ Título desvia do padrão do canal (similaridade: {coherence['score']:.2%})"
            )

        semantic = analysis['semantic_analysis']
        if not semantic['is_aligned']:
            recommendations.append(
                f"💡 Alinhamento semântico baixo com o canal ({semantic['channel_alignment']:.2%})"
            )

        risk = analysis['risk_assessment']
        if risk['risk_level'] == 'alto':
            recommendations.append(
                f"🎯 Risco {risk['risk_level']} - Título muito diferente do padrão estabelecido"
            )
        elif risk['risk_level'] == 'baixo':
            recommendations.append(
                f"✅ Risco {risk['risk_level']} - Título alinhado com o padrão do canal"
            )

        if analysis['pattern_match']['learning_phase']:
            recommendations.append(
                "📚 Sistema em fase de aprendizado - adicione mais conteúdos para análise mais precisa"
            )

        return recommendations or ["✅ Título aprovado - dentro dos padrões aprendidos"]

    def _generate_coherence_message(self, similarity: float, is_coherent: bool) -> str:
        """Gera mensagem sobre coerência"""
        if similarity > 0.7:
            return "Altamente coerente com o canal"
        elif similarity > 0.5:
            return "Coerente com o canal"
        elif similarity > 0.3:
            return "Parcialmente coerente"
        else:
            return "Baixa coerência - conteúdo divergente"

    def _generate_semantic_message(self, similarity: float) -> str:
        """Gera mensagem sobre alinhamento semântico"""
        if similarity > 0.6:
            return "Fortemente alinhado semanticamente"
        elif similarity > 0.4:
            return "Alinhamento semântico adequado"
        else:
            return "Alinhamento semântico fraco"

    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calcula similaridade de cosseno"""
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    def _compare_with_learned_structures(self, structure: Dict) -> float:
        """Compara estrutura com padrões aprendidos"""
        if not self.discovered_patterns['title_structure']:
            return 0.5

        # Compara métricas numéricas
        similarities = []
        for learned in self.discovered_patterns['title_structure']:
            sim = 1 - abs(structure['word_count'] - learned.get('word_count', 0)) / max(structure['word_count'], 1)
            similarities.append(sim)

        return float(np.mean(similarities))

    def learn_from_feedback(self, content: str, content_type: str, was_successful: bool):
        """
        Aprende com feedback do usuário.
        Ajusta os modelos baseado no sucesso/fracasso.
        """
        if was_successful:
            # Adiciona aos padrões de sucesso
            self.add_training_data(content, content_type)

            # Atualiza padrões descobertos
            tokens = self._preprocess_text(content)
            structure = self._discover_structure(content, tokens)
            self.discovered_patterns['title_structure'].append(structure)

    def get_channel_embedding(self) -> Optional[np.ndarray]:
        """
        Retorna o embedding geral do canal.
        Calculado dinamicamente baseado em todo o histórico.
        """
        all_vectors = []

        for content_type, items in self.channel_vectors.items():
            for item in items:
                all_vectors.append(item['vector'])

        if not all_vectors:
            return None

        # Embedding do canal = média de todos os vetores
        return np.mean(all_vectors, axis=0)

    def suggest_similar_content(self, text: str, top_n: int = 5) -> List[Dict]:
        """
        Sugere conteúdos similares do histórico do canal.
        """
        text_vector = self.sentence_model.encode(text)

        similarities = []
        for content_type, items in self.channel_vectors.items():
            for item in items:
                sim = self._cosine_similarity(text_vector, item['vector'])
                similarities.append({
                    'text': item['text'],
                    'type': content_type,
                    'similarity': sim
                })

        # Ordena por similaridade
        similarities.sort(key=lambda x: x['similarity'], reverse=True)

        return similarities[:top_n]
