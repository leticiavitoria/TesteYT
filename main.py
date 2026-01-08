"""
YouTube Channel Vector Optimizer - Main Application
Sistema adaptativo de otimização de conteúdo para YouTube
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

# Adiciona o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.channel_service import ChannelService
from database.storage import ChannelStorage
from models.channel import Channel

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# Inicializa serviços
channel_service = ChannelService()
storage = ChannelStorage()


@app.route('/')
def index():
    """Serve a aplicação frontend"""
    return send_from_directory('frontend', 'index.html')


@app.route('/api/channel/create', methods=['POST'])
def create_channel():
    """Cria um novo canal"""
    try:
        data = request.json
        name = data.get('name')
        sub_niche = data.get('sub_niche')
        description = data.get('description')

        if not all([name, sub_niche, description]):
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400

        result = channel_service.create_new_channel(name, sub_niche, description)

        # Salva o canal
        if result['success']:
            channel_data = channel_service.current_channel.to_dict()
            learning_data = {
                'vector_data': channel_service.vector_analyzer.channel_vectors,
                'patterns': channel_service.pattern_engine.discovered_patterns
            }
            storage.save_channel(channel_data, learning_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/channels/list', methods=['GET'])
def list_channels():
    """Lista todos os canais salvos"""
    try:
        channels = storage.list_channels()
        return jsonify({'success': True, 'channels': channels})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/channel/load/<channel_id>', methods=['GET'])
def load_channel(channel_id):
    """Carrega um canal existente"""
    try:
        data = storage.load_channel(channel_id)

        if not data:
            return jsonify({'success': False, 'error': 'Canal não encontrado'}), 404

        # Reconstrói o canal no serviço
        channel_service.current_channel = Channel.from_dict(data['channel'])

        # TODO: Restaurar dados de aprendizado (vectors, patterns)
        # Isso requer serialização/deserialização de modelos Word2Vec

        return jsonify({
            'success': True,
            'channel': data['channel']
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/channel/train', methods=['POST'])
def train_channel():
    """Treina o sistema com títulos de exemplo"""
    try:
        data = request.json
        channel_id = data.get('channel_id')
        titles = data.get('titles', [])

        if not titles:
            return jsonify({'success': False, 'error': 'Nenhum título fornecido'}), 400

        result = channel_service.add_example_titles(titles)

        # Salva progresso
        if channel_service.current_channel:
            channel_data = channel_service.current_channel.to_dict()
            learning_data = {
                'vector_data': channel_service.vector_analyzer.channel_vectors,
                'patterns': channel_service.pattern_engine.discovered_patterns
            }
            storage.save_channel(channel_data, learning_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/title/validate', methods=['POST'])
def validate_title():
    """Valida um título"""
    try:
        data = request.json
        title = data.get('title')

        if not title:
            return jsonify({'success': False, 'error': 'Título não fornecido'}), 400

        result = channel_service.validate_title(title)

        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/script/generate-prompt', methods=['POST'])
def generate_script_prompt():
    """Gera prompt para criação de roteiro"""
    try:
        data = request.json
        title = data.get('title')

        if not title:
            return jsonify({'success': False, 'error': 'Título não fornecido'}), 400

        result = channel_service.generate_script_prompt(title)

        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/script/validate', methods=['POST'])
def validate_script():
    """Valida roteiro"""
    try:
        data = request.json
        title = data.get('title')
        script = data.get('script')

        if not title or not script:
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400

        result = channel_service.validate_script(title, script)

        # Salva progresso
        if channel_service.current_channel:
            channel_data = channel_service.current_channel.to_dict()
            learning_data = {
                'vector_data': channel_service.vector_analyzer.channel_vectors,
                'patterns': channel_service.pattern_engine.discovered_patterns
            }
            storage.save_channel(channel_data, learning_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/content/generate', methods=['POST'])
def generate_content():
    """Gera conteúdo complementar (descrição, tags, thumbnail)"""
    try:
        data = request.json
        title = data.get('title')
        script = data.get('script', '')

        if not title:
            return jsonify({'success': False, 'error': 'Título não fornecido'}), 400

        result = channel_service.generate_complementary_content(title, script)

        # Salva vídeo no canal
        video_data = {
            'title': title,
            'script': script,
            'description': result['description'],
            'tags': result['tags'],
            'thumbnail_prompt': result['thumbnail_prompt']
        }
        channel_service.save_video_to_channel(video_data)

        # Salva progresso
        if channel_service.current_channel:
            channel_data = channel_service.current_channel.to_dict()
            learning_data = {
                'vector_data': channel_service.vector_analyzer.channel_vectors,
                'patterns': channel_service.pattern_engine.discovered_patterns
            }
            storage.save_channel(channel_data, learning_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/channel/summary/<channel_id>', methods=['GET'])
def get_channel_summary(channel_id):
    """Retorna resumo do canal"""
    try:
        result = channel_service.get_channel_summary()
        return jsonify(result)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'YouTube Channel Vector Optimizer is running'
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🎯 YouTube Channel Vector Optimizer")
    print("=" * 60)
    print("\n✅ Sistema Adaptativo de Otimização de Conteúdo")
    print("✅ Análise Vetorial com Word2Vec e NLP")
    print("✅ Aprendizado Automático de Padrões")
    print("\n📡 Servidor iniciando em http://localhost:5001")
    print("🌐 Acesse a interface web no navegador\n")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5001)
