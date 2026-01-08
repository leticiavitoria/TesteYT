"""
Sistema de Descoberta Automática de Padrões.
Identifica o que funciona sem regras pré-definidas.
"""

import numpy as np
from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
import re


class PatternDiscoveryEngine:
    """
    Engine que descobre padrões automaticamente analisando conteúdos.
    Aprende estruturas, estilos e características sem regras fixas.
    """

    def __init__(self):
        self.discovered_patterns = {
            'structures': [],  # Padrões estruturais
            'vocabulary': Counter(),  # Vocabulário aprendido
            'phrases': Counter(),  # Frases comuns
            'styles': [],  # Estilos identificados
            'formats': []  # Formatos descobertos
        }

        self.learning_history = []

    def analyze_content_batch(self, contents: List[str]) -> Dict:
        """
        Analisa um lote de conteúdos e descobre padrões.
        Quanto mais conteúdo, mais preciso o aprendizado.
        """
        if not contents:
            return {'error': 'Nenhum conteúdo fornecido'}

        # Descobre padrões em múltiplas dimensões
        patterns = {
            'structural': self._discover_structural_patterns(contents),
            'linguistic': self._discover_linguistic_patterns(contents),
            'stylistic': self._discover_stylistic_patterns(contents),
            'format': self._discover_format_patterns(contents),
            'vocabulary': self._build_vocabulary_profile(contents)
        }

        # Atualiza conhecimento
        self._update_knowledge_base(patterns)

        return patterns

    def _discover_structural_patterns(self, contents: List[str]) -> Dict:
        """
        Descobre padrões estruturais: comprimento, organização, etc.
        """
        lengths = [len(c) for c in contents]
        word_counts = [len(c.split()) for c in contents]

        # Descobre ranges ideais baseado nos dados
        length_pattern = {
            'min': int(np.min(lengths)),
            'max': int(np.max(lengths)),
            'mean': float(np.mean(lengths)),
            'median': float(np.median(lengths)),
            'std': float(np.std(lengths)),
            'optimal_range': (
                int(np.percentile(lengths, 25)),
                int(np.percentile(lengths, 75))
            )
        }

        word_pattern = {
            'min_words': int(np.min(word_counts)),
            'max_words': int(np.max(word_counts)),
            'mean_words': float(np.mean(word_counts)),
            'optimal_word_range': (
                int(np.percentile(word_counts, 25)),
                int(np.percentile(word_counts, 75))
            )
        }

        return {
            'length': length_pattern,
            'words': word_pattern,
            'consistency_score': 1 - (np.std(lengths) / np.mean(lengths)) if np.mean(lengths) > 0 else 0
        }

    def _discover_linguistic_patterns(self, contents: List[str]) -> Dict:
        """
        Descobre padrões linguísticos: palavras frequentes, n-grams, etc.
        """
        # Extrai todas as palavras
        all_words = []
        for content in contents:
            words = re.findall(r'\b\w+\b', content.lower())
            all_words.extend(words)

        # Palavras mais frequentes
        word_freq = Counter(all_words)
        top_words = word_freq.most_common(20)

        # Descobre bigramas (2 palavras consecutivas)
        bigrams = []
        for content in contents:
            words = re.findall(r'\b\w+\b', content.lower())
            for i in range(len(words) - 1):
                bigrams.append(f"{words[i]} {words[i+1]}")

        bigram_freq = Counter(bigrams)
        top_bigrams = bigram_freq.most_common(10)

        # Descobre trigramas
        trigrams = []
        for content in contents:
            words = re.findall(r'\b\w+\b', content.lower())
            for i in range(len(words) - 2):
                trigrams.append(f"{words[i]} {words[i+1]} {words[i+2]}")

        trigram_freq = Counter(trigrams)
        top_trigrams = trigram_freq.most_common(5)

        return {
            'top_words': top_words,
            'top_bigrams': top_bigrams,
            'top_trigrams': top_trigrams,
            'vocabulary_size': len(word_freq),
            'unique_word_ratio': len(word_freq) / len(all_words) if all_words else 0
        }

    def _discover_stylistic_patterns(self, contents: List[str]) -> Dict:
        """
        Descobre padrões de estilo: tom, formalidade, uso de pontuação, etc.
        """
        styles = {
            'capitalization': self._analyze_capitalization_style(contents),
            'punctuation': self._analyze_punctuation_style(contents),
            'numbers': self._analyze_number_usage(contents),
            'questions': self._analyze_question_usage(contents),
            'emotional_markers': self._analyze_emotional_markers(contents)
        }

        return styles

    def _analyze_capitalization_style(self, contents: List[str]) -> Dict:
        """Analisa padrão de capitalização"""
        patterns = {
            'all_caps': 0,
            'title_case': 0,
            'sentence_case': 0,
            'lowercase': 0,
            'mixed': 0
        }

        for content in contents:
            if content.isupper():
                patterns['all_caps'] += 1
            elif content.istitle():
                patterns['title_case'] += 1
            elif content[0].isupper() if content else False:
                patterns['sentence_case'] += 1
            elif content.islower():
                patterns['lowercase'] += 1
            else:
                patterns['mixed'] += 1

        # Determina padrão dominante
        dominant = max(patterns, key=patterns.get)
        confidence = patterns[dominant] / len(contents) if contents else 0

        return {
            'patterns': patterns,
            'dominant_pattern': dominant,
            'confidence': confidence
        }

    def _analyze_punctuation_style(self, contents: List[str]) -> Dict:
        """Analisa uso de pontuação"""
        total_contents = len(contents)

        exclamation_usage = sum(1 for c in contents if '!' in c) / total_contents
        question_usage = sum(1 for c in contents if '?' in c) / total_contents
        emoji_usage = sum(1 for c in contents if re.search(r'[\U0001F600-\U0001F64F]', c)) / total_contents

        avg_exclamations = np.mean([c.count('!') for c in contents])
        avg_questions = np.mean([c.count('?') for c in contents])

        return {
            'uses_exclamation': exclamation_usage > 0.3,
            'uses_questions': question_usage > 0.3,
            'uses_emojis': emoji_usage > 0.2,
            'avg_exclamations_per_content': float(avg_exclamations),
            'avg_questions_per_content': float(avg_questions),
            'exclamation_frequency': float(exclamation_usage),
            'question_frequency': float(question_usage),
            'emoji_frequency': float(emoji_usage)
        }

    def _analyze_number_usage(self, contents: List[str]) -> Dict:
        """Analisa uso de números"""
        total_contents = len(contents)
        contents_with_numbers = sum(1 for c in contents if re.search(r'\d', c))

        all_numbers = []
        for content in contents:
            numbers = re.findall(r'\d+', content)
            all_numbers.extend([int(n) for n in numbers if n.isdigit()])

        return {
            'frequency': contents_with_numbers / total_contents if total_contents > 0 else 0,
            'uses_numbers': contents_with_numbers / total_contents > 0.3,
            'common_numbers': Counter(all_numbers).most_common(5),
            'avg_numbers_per_content': len(all_numbers) / total_contents if total_contents > 0 else 0
        }

    def _analyze_question_usage(self, contents: List[str]) -> Dict:
        """Analisa uso de perguntas"""
        question_patterns = [
            r'\bcomo\b',
            r'\bpor que\b',
            r'\bporque\b',
            r'\bquando\b',
            r'\bonde\b',
            r'\bquem\b',
            r'\bqual\b',
            r'\bquais\b',
            r'\bo que\b'
        ]

        total_with_questions = 0
        question_types = Counter()

        for content in contents:
            content_lower = content.lower()
            has_question = False

            for pattern in question_patterns:
                if re.search(pattern, content_lower):
                    question_types[pattern] += 1
                    has_question = True

            if has_question or '?' in content:
                total_with_questions += 1

        return {
            'uses_questions': total_with_questions / len(contents) > 0.2 if contents else False,
            'question_frequency': total_with_questions / len(contents) if contents else 0,
            'common_question_types': question_types.most_common(3)
        }

    def _analyze_emotional_markers(self, contents: List[str]) -> Dict:
        """Analisa marcadores emocionais"""
        # Palavras que indicam emoção/engajamento
        engagement_words = {
            'incrível', 'surpreendente', 'chocante', 'impressionante',
            'fantástico', 'espetacular', 'extraordinário', 'único',
            'exclusivo', 'secreto', 'revelado', 'descoberta', 'novo',
            'melhor', 'pior', 'maior', 'menor', 'primeiro', 'último'
        }

        total_engagement_words = 0
        contents_with_engagement = 0

        for content in contents:
            content_lower = content.lower()
            found_engagement = False

            for word in engagement_words:
                if word in content_lower:
                    total_engagement_words += 1
                    found_engagement = True

            if found_engagement:
                contents_with_engagement += 1

        return {
            'uses_engagement_words': contents_with_engagement / len(contents) > 0.3 if contents else False,
            'engagement_frequency': contents_with_engagement / len(contents) if contents else 0,
            'avg_engagement_words': total_engagement_words / len(contents) if contents else 0
        }

    def _discover_format_patterns(self, contents: List[str]) -> Dict:
        """
        Descobre padrões de formato: listas, numeração, símbolos, etc.
        """
        formats = {
            'uses_lists': sum(1 for c in contents if re.search(r'[\-\*\•]', c)) > 0,
            'uses_colons': sum(1 for c in contents if ':' in c) / len(contents) if contents else 0,
            'uses_parentheses': sum(1 for c in contents if '(' in c or ')' in c) / len(contents) if contents else 0,
            'uses_quotes': sum(1 for c in contents if '"' in c or "'" in c) / len(contents) if contents else 0
        }

        # Detecta padrões de início
        start_patterns = Counter()
        for content in contents:
            words = content.split()
            if words:
                first_word = words[0].lower()
                start_patterns[first_word] += 1

        formats['common_starts'] = start_patterns.most_common(5)

        return formats

    def _build_vocabulary_profile(self, contents: List[str]) -> Dict:
        """
        Constrói perfil de vocabulário único do canal.
        """
        all_words = []
        for content in contents:
            words = re.findall(r'\b\w+\b', content.lower())
            all_words.extend(words)

        word_freq = Counter(all_words)

        # Atualiza vocabulário global
        self.discovered_patterns['vocabulary'].update(word_freq)

        return {
            'total_words': len(all_words),
            'unique_words': len(word_freq),
            'lexical_diversity': len(word_freq) / len(all_words) if all_words else 0,
            'top_words': word_freq.most_common(30),
            'rare_words': [word for word, count in word_freq.items() if count == 1][:10]
        }

    def _update_knowledge_base(self, patterns: Dict):
        """
        Atualiza base de conhecimento com novos padrões descobertos.
        """
        self.learning_history.append({
            'timestamp': str(np.datetime64('now')),
            'patterns': patterns
        })

        # Atualiza padrões globais
        if 'structural' in patterns:
            self.discovered_patterns['structures'].append(patterns['structural'])

        if 'stylistic' in patterns:
            self.discovered_patterns['styles'].append(patterns['stylistic'])

        if 'format' in patterns:
            self.discovered_patterns['formats'].append(patterns['format'])

    def get_learned_guidelines(self) -> Dict:
        """
        Retorna diretrizes aprendidas baseadas nos padrões descobertos.
        """
        if not self.discovered_patterns['structures']:
            return {
                'status': 'learning',
                'message': 'Sistema ainda aprendendo. Adicione mais conteúdos.'
            }

        # Agrega todos os padrões estruturais
        all_lengths = []
        all_word_counts = []

        for struct in self.discovered_patterns['structures']:
            if 'length' in struct:
                all_lengths.append(struct['length']['mean'])
            if 'words' in struct:
                all_word_counts.append(struct['words']['mean_words'])

        guidelines = {
            'recommended_length': {
                'min': int(np.mean(all_lengths) - np.std(all_lengths)) if all_lengths else 0,
                'max': int(np.mean(all_lengths) + np.std(all_lengths)) if all_lengths else 0,
                'ideal': int(np.mean(all_lengths)) if all_lengths else 0
            },
            'recommended_word_count': {
                'min': int(np.mean(all_word_counts) - np.std(all_word_counts)) if all_word_counts else 0,
                'max': int(np.mean(all_word_counts) + np.std(all_word_counts)) if all_word_counts else 0,
                'ideal': int(np.mean(all_word_counts)) if all_word_counts else 0
            },
            'style_preferences': self._aggregate_style_preferences(),
            'vocabulary_core': self.discovered_patterns['vocabulary'].most_common(50)
        }

        return guidelines

    def _aggregate_style_preferences(self) -> Dict:
        """Agrega preferências de estilo aprendidas"""
        if not self.discovered_patterns['styles']:
            return {}

        # Agrega dados de todos os estilos aprendidos
        preferences = {
            'prefers_questions': False,
            'prefers_exclamations': False,
            'prefers_numbers': False,
            'prefers_emojis': False,
            'capitalization_style': 'mixed'
        }

        # Analisa tendências
        question_scores = []
        exclamation_scores = []
        number_scores = []

        for style in self.discovered_patterns['styles']:
            if 'questions' in style:
                question_scores.append(style['questions'].get('question_frequency', 0))
            if 'punctuation' in style:
                exclamation_scores.append(style['punctuation'].get('exclamation_frequency', 0))
            if 'numbers' in style:
                number_scores.append(style['numbers'].get('frequency', 0))

        if question_scores:
            preferences['prefers_questions'] = np.mean(question_scores) > 0.3
        if exclamation_scores:
            preferences['prefers_exclamations'] = np.mean(exclamation_scores) > 0.3
        if number_scores:
            preferences['prefers_numbers'] = np.mean(number_scores) > 0.3

        return preferences

    def evaluate_content_against_patterns(self, content: str) -> Dict:
        """
        Avalia um novo conteúdo contra os padrões aprendidos.
        """
        guidelines = self.get_learned_guidelines()

        if guidelines.get('status') == 'learning':
            return {
                'score': 0.5,
                'message': 'Sistema em aprendizado',
                'matches': []
            }

        matches = []
        mismatches = []

        # Verifica comprimento
        content_length = len(content)
        recommended = guidelines['recommended_length']
        if recommended['min'] <= content_length <= recommended['max']:
            matches.append(f"✅ Comprimento ideal ({content_length} caracteres)")
        else:
            mismatches.append(
                f"⚠️ Comprimento fora do padrão (recomendado: {recommended['min']}-{recommended['max']}, atual: {content_length})"
            )

        # Verifica quantidade de palavras
        word_count = len(content.split())
        recommended_words = guidelines['recommended_word_count']
        if recommended_words['min'] <= word_count <= recommended_words['max']:
            matches.append(f"✅ Quantidade de palavras ideal ({word_count} palavras)")
        else:
            mismatches.append(
                f"⚠️ Quantidade de palavras fora do padrão (recomendado: {recommended_words['min']}-{recommended_words['max']}, atual: {word_count})"
            )

        # Verifica vocabulário
        content_words = set(re.findall(r'\b\w+\b', content.lower()))
        core_vocab = set([word for word, _ in guidelines['vocabulary_core'][:20]])
        vocab_overlap = len(content_words & core_vocab)

        if vocab_overlap > 0:
            matches.append(f"✅ Usa {vocab_overlap} palavras do vocabulário principal do canal")

        # Calcula score final
        total_checks = len(matches) + len(mismatches)
        score = len(matches) / total_checks if total_checks > 0 else 0.5

        return {
            'score': score,
            'matches': matches,
            'mismatches': mismatches,
            'recommendations': self._generate_pattern_recommendations(mismatches)
        }

    def _generate_pattern_recommendations(self, mismatches: List[str]) -> List[str]:
        """Gera recomendações baseadas nos desalinhamentos"""
        if not mismatches:
            return ["✅ Conteúdo perfeitamente alinhado com os padrões aprendidos"]

        recommendations = []
        for mismatch in mismatches:
            if 'Comprimento' in mismatch:
                recommendations.append("Ajuste o comprimento do conteúdo para se alinhar com o padrão do canal")
            elif 'palavras' in mismatch:
                recommendations.append("Ajuste a quantidade de palavras")

        return recommendations
