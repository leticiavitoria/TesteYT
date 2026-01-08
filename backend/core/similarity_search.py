"""
Sistema de Busca de Conteúdos Similares.
Pesquisa e analisa conteúdos similares para aprender o que funciona.
"""

import re
from typing import List, Dict, Optional
from collections import Counter
import numpy as np


class SimilaritySearchEngine:
    """
    Engine de busca que encontra e analisa conteúdos similares.
    Usa APIs e web scraping para aprender com canais de sucesso.
    """

    def __init__(self):
        self.search_cache = {}
        self.analyzed_content = []

    def search_similar_channels(self, channel_description: str, keywords: List[str]) -> Dict:
        """
        Busca canais similares baseado na descrição e palavras-chave.

        NOTA: Em produção, integrar com:
        - YouTube Data API v3
        - Web scraping de títulos populares
        - Análise de trending topics
        """
        # Por enquanto, simulamos a busca
        # Em produção, fazer requisições reais à API do YouTube

        search_query = self._build_search_query(channel_description, keywords)

        # Simula resultados (em produção, usar API real)
        similar_channels = {
            'search_query': search_query,
            'message': 'Busca simulada - integrar com YouTube API v3',
            'suggestions': [
                '1. Integrar YouTube Data API v3',
                '2. Usar google-api-python-client',
                '3. Analisar títulos de vídeos populares',
                '4. Extrair padrões de canais de sucesso'
            ],
            'api_setup_guide': self._get_api_setup_guide()
        }

        return similar_channels

    def _build_search_query(self, description: str, keywords: List[str]) -> str:
        """Constrói query de busca otimizada"""
        # Combina descrição e keywords
        query_parts = keywords[:3]  # Top 3 keywords

        return ' '.join(query_parts)

    def _get_api_setup_guide(self) -> Dict:
        """
        Guia para configurar YouTube API.
        """
        return {
            'steps': [
                '1. Acesse Google Cloud Console (console.cloud.google.com)',
                '2. Crie um novo projeto',
                '3. Habilite YouTube Data API v3',
                '4. Crie credenciais (API Key)',
                '5. Adicione a chave no arquivo .env como YOUTUBE_API_KEY'
            ],
            'code_example': '''
# Exemplo de uso da API:
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=API_KEY)

# Buscar vídeos
request = youtube.search().list(
    q='sua busca',
    part='snippet',
    type='video',
    maxResults=50,
    order='viewCount'
)
response = request.execute()
            '''
        }

    def analyze_successful_titles(self, titles: List[str]) -> Dict:
        """
        Analisa títulos de sucesso para identificar padrões.
        Aprende o que funciona organicamente.
        """
        if not titles:
            return {'error': 'Nenhum título fornecido'}

        analysis = {
            'total_analyzed': len(titles),
            'patterns': self._extract_title_patterns(titles),
            'structure': self._analyze_title_structures(titles),
            'keywords': self._extract_common_keywords(titles),
            'strategies': self._identify_strategies(titles)
        }

        # Armazena para aprendizado
        self.analyzed_content.extend(titles)

        return analysis

    def _extract_title_patterns(self, titles: List[str]) -> Dict:
        """Extrai padrões de títulos de sucesso"""
        patterns = {
            'with_numbers': sum(1 for t in titles if re.search(r'\d+', t)),
            'with_questions': sum(1 for t in titles if '?' in t),
            'with_exclamations': sum(1 for t in titles if '!' in t),
            'with_caps': sum(1 for t in titles if any(c.isupper() for c in t)),
            'with_emojis': sum(1 for t in titles if re.search(r'[\U0001F600-\U0001F64F]', t))
        }

        total = len(titles)
        percentages = {
            key: (value / total) * 100
            for key, value in patterns.items()
        }

        return {
            'counts': patterns,
            'percentages': percentages,
            'insights': self._generate_pattern_insights(percentages)
        }

    def _analyze_title_structures(self, titles: List[str]) -> Dict:
        """Analisa estruturas de títulos"""
        lengths = [len(t) for t in titles]
        word_counts = [len(t.split()) for t in titles]

        return {
            'length_stats': {
                'min': min(lengths),
                'max': max(lengths),
                'mean': np.mean(lengths),
                'median': np.median(lengths),
                'mode': Counter(lengths).most_common(1)[0][0] if lengths else 0
            },
            'word_count_stats': {
                'min': min(word_counts),
                'max': max(word_counts),
                'mean': np.mean(word_counts),
                'median': np.median(word_counts)
            },
            'optimal_ranges': {
                'length': (int(np.percentile(lengths, 25)), int(np.percentile(lengths, 75))),
                'words': (int(np.percentile(word_counts, 25)), int(np.percentile(word_counts, 75)))
            }
        }

    def _extract_common_keywords(self, titles: List[str]) -> Dict:
        """Extrai palavras-chave mais comuns"""
        # Extrai todas as palavras
        all_words = []
        for title in titles:
            words = re.findall(r'\b\w+\b', title.lower())
            all_words.extend(words)

        # Remove palavras muito curtas
        all_words = [w for w in all_words if len(w) > 2]

        word_freq = Counter(all_words)

        # Identifica power words (palavras que geram engajamento)
        power_words = [
            'como', 'melhor', 'pior', 'segredo', 'incrível', 'chocante',
            'você', 'nunca', 'sempre', 'tudo', 'nada', 'novo', 'primeiro',
            'último', 'único', 'completo', 'rápido', 'fácil', 'grátis'
        ]

        found_power_words = {
            word: word_freq[word]
            for word in power_words
            if word in word_freq
        }

        return {
            'top_words': word_freq.most_common(30),
            'power_words_found': found_power_words,
            'total_unique_words': len(word_freq),
            'vocabulary_diversity': len(word_freq) / len(all_words) if all_words else 0
        }

    def _identify_strategies(self, titles: List[str]) -> List[Dict]:
        """Identifica estratégias de títulos"""
        strategies = []

        # Estratégia 1: Uso de números/listas
        titles_with_numbers = [t for t in titles if re.search(r'\d+', t)]
        if len(titles_with_numbers) / len(titles) > 0.3:
            strategies.append({
                'strategy': 'Listas Numeradas',
                'frequency': f"{(len(titles_with_numbers) / len(titles)) * 100:.1f}%",
                'example': titles_with_numbers[0] if titles_with_numbers else '',
                'recommendation': 'Usar números e listas é efetivo (ex: "5 formas de...", "Top 10...")'
            })

        # Estratégia 2: Perguntas diretas
        titles_with_questions = [t for t in titles if '?' in t]
        if len(titles_with_questions) / len(titles) > 0.2:
            strategies.append({
                'strategy': 'Perguntas Diretas',
                'frequency': f"{(len(titles_with_questions) / len(titles)) * 100:.1f}%",
                'example': titles_with_questions[0] if titles_with_questions else '',
                'recommendation': 'Títulos em formato de pergunta geram curiosidade'
            })

        # Estratégia 3: How-to/Tutorial
        how_to_titles = [t for t in titles if re.search(r'\bcomo\b', t.lower())]
        if len(how_to_titles) / len(titles) > 0.2:
            strategies.append({
                'strategy': 'How-To/Tutorial',
                'frequency': f"{(len(how_to_titles) / len(titles)) * 100:.1f}%",
                'example': how_to_titles[0] if how_to_titles else '',
                'recommendation': 'Conteúdo educacional ("Como fazer...") funciona bem'
            })

        # Estratégia 4: Clickbait moderado
        clickbait_words = ['incrível', 'chocante', 'não vai acreditar', 'segredo', 'revelado']
        clickbait_titles = [
            t for t in titles
            if any(word in t.lower() for word in clickbait_words)
        ]
        if len(clickbait_titles) / len(titles) > 0.15:
            strategies.append({
                'strategy': 'Elementos de Curiosidade',
                'frequency': f"{(len(clickbait_titles) / len(titles)) * 100:.1f}%",
                'example': clickbait_titles[0] if clickbait_titles else '',
                'recommendation': 'Palavras que geram curiosidade podem aumentar CTR'
            })

        return strategies

    def _generate_pattern_insights(self, percentages: Dict) -> List[str]:
        """Gera insights baseados em padrões"""
        insights = []

        if percentages['with_numbers'] > 40:
            insights.append(f"✅ {percentages['with_numbers']:.0f}% dos títulos usam números - estratégia efetiva")

        if percentages['with_questions'] > 25:
            insights.append(f"✅ {percentages['with_questions']:.0f}% usam perguntas - gera curiosidade")

        if percentages['with_exclamations'] > 30:
            insights.append(f"⚠️ {percentages['with_exclamations']:.0f}% usam exclamações - pode ser excessivo")

        if percentages['with_emojis'] > 20:
            insights.append(f"✅ {percentages['with_emojis']:.0f}% usam emojis - aumenta visibilidade")

        return insights or ["Padrões ainda sendo identificados"]

    def generate_title_suggestions(
        self,
        channel_context: Dict,
        learned_patterns: Dict,
        topic: str
    ) -> List[str]:
        """
        Gera sugestões de títulos baseadas em padrões aprendidos.
        """
        suggestions = []

        # Obtém padrões aprendidos
        keywords = learned_patterns.get('keywords', {}).get('top_words', [])[:10]
        structures = learned_patterns.get('structure', {})

        # Template 1: Número + Verbo + Tópico
        if keywords:
            suggestions.append(f"5 {keywords[0][0] if keywords else 'formas de'} {topic}")

        # Template 2: Como fazer
        suggestions.append(f"Como {topic}: Guia Completo")

        # Template 3: Pergunta
        suggestions.append(f"O que você precisa saber sobre {topic}?")

        # Template 4: Revelação
        suggestions.append(f"A verdade sobre {topic} que ninguém conta")

        # Template 5: Comparação
        suggestions.append(f"{topic}: Tudo o que você precisa saber")

        return suggestions[:5]

    def evaluate_title_performance_potential(
        self,
        title: str,
        learned_patterns: Dict
    ) -> Dict:
        """
        Avalia o potencial de performance de um título
        baseado em padrões aprendidos.
        """
        score = 0
        factors = []

        # Verifica uso de números
        if re.search(r'\d+', title):
            score += 20
            factors.append("✅ Usa números (+20)")
        else:
            factors.append("💡 Considere adicionar números")

        # Verifica formato de pergunta
        if '?' in title:
            score += 15
            factors.append("✅ Formato de pergunta (+15)")

        # Verifica comprimento
        title_len = len(title)
        optimal_range = learned_patterns.get('structure', {}).get('optimal_ranges', {}).get('length', (40, 70))

        if optimal_range[0] <= title_len <= optimal_range[1]:
            score += 25
            factors.append(f"✅ Comprimento ideal (+25)")
        else:
            factors.append(f"⚠️ Comprimento fora do padrão (ideal: {optimal_range[0]}-{optimal_range[1]})")

        # Verifica palavras-chave
        top_keywords = [kw[0] for kw in learned_patterns.get('keywords', {}).get('top_words', [])[:20]]
        title_words = set(re.findall(r'\b\w+\b', title.lower()))
        keyword_matches = len(title_words & set(top_keywords))

        if keyword_matches > 0:
            keyword_score = min(keyword_matches * 10, 30)
            score += keyword_score
            factors.append(f"✅ {keyword_matches} palavras-chave reconhecidas (+{keyword_score})")

        # Verifica estratégias de sucesso
        strategies = learned_patterns.get('strategies', [])
        for strategy in strategies:
            if strategy['strategy'] == 'Listas Numeradas' and re.search(r'\d+', title):
                score += 10
                factors.append("✅ Usa estratégia de listas (+10)")

        # Normaliza score (0-100)
        final_score = min(score, 100)

        return {
            'score': final_score,
            'rating': self._get_rating(final_score),
            'factors': factors,
            'prediction': self._generate_prediction(final_score)
        }

    def _get_rating(self, score: float) -> str:
        """Retorna rating baseado no score"""
        if score >= 80:
            return "Excelente"
        elif score >= 60:
            return "Bom"
        elif score >= 40:
            return "Regular"
        else:
            return "Precisa melhorar"

    def _generate_prediction(self, score: float) -> str:
        """Gera predição de performance"""
        if score >= 80:
            return "Alto potencial de engajamento"
        elif score >= 60:
            return "Bom potencial de performance"
        elif score >= 40:
            return "Performance moderada esperada"
        else:
            return "Baixo potencial - recomenda-se ajustes"

    def compare_with_competitors(
        self,
        your_title: str,
        competitor_titles: List[str]
    ) -> Dict:
        """
        Compara seu título com títulos de competidores.
        """
        competitor_analysis = self.analyze_successful_titles(competitor_titles)

        your_analysis = {
            'length': len(your_title),
            'word_count': len(your_title.split()),
            'has_numbers': bool(re.search(r'\d+', your_title)),
            'has_question': '?' in your_title
        }

        competitor_stats = competitor_analysis['structure']

        comparison = {
            'your_title': your_analysis,
            'competitor_average': {
                'length': competitor_stats['length_stats']['mean'],
                'word_count': competitor_stats['word_count_stats']['mean']
            },
            'competitive_edge': [],
            'areas_to_improve': []
        }

        # Análise comparativa
        if your_analysis['length'] > competitor_stats['length_stats']['mean']:
            comparison['competitive_edge'].append("Título mais detalhado que a média")
        else:
            comparison['areas_to_improve'].append("Considere adicionar mais contexto")

        if your_analysis['has_numbers'] and competitor_analysis['patterns']['percentages']['with_numbers'] < 50:
            comparison['competitive_edge'].append("Uso estratégico de números se destaca")

        return comparison
