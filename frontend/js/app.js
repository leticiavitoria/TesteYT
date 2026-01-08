// YouTube Channel Vector Optimizer - Frontend Application

const API_URL = 'http://localhost:5000/api';

const app = {
    currentChannel: null,
    currentSection: 'channel-selection',

    init() {
        console.log('YouTube Channel Vector Optimizer initialized');
        this.setupEventListeners();
    },

    setupEventListeners() {
        // Form submissions
        const createForm = document.getElementById('create-channel-form');
        if (createForm) {
            createForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.createChannel();
            });
        }
    },

    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });

        // Show selected section
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.add('active');
            this.currentSection = sectionId;
        }
    },

    goBack(sectionId) {
        this.showSection(sectionId);
    },

    showLoading(show = true) {
        const overlay = document.getElementById('loading-overlay');
        overlay.style.display = show ? 'flex' : 'none';
    },

    showCreateChannel() {
        this.showSection('create-channel');
    },

    showLoadChannel() {
        this.showSection('load-channel');
        this.loadChannelsList();
    },

    async createChannel() {
        const name = document.getElementById('channel-name').value;
        const subNiche = document.getElementById('sub-niche').value;
        const description = document.getElementById('channel-description').value;

        this.showLoading();

        try {
            const response = await fetch(`${API_URL}/channel/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, sub_niche: subNiche, description })
            });

            const data = await response.json();
            this.showLoading(false);

            if (data.success) {
                this.currentChannel = data.channel_id;
                alert(`Canal "${name}" criado com sucesso!`);
                this.showSection('train-system');
            } else {
                alert('Erro ao criar canal: ' + (data.error || 'Erro desconhecido'));
            }
        } catch (error) {
            this.showLoading(false);
            alert('Erro de conexão: ' + error.message);
        }
    },

    async loadChannelsList() {
        const listDiv = document.getElementById('channels-list');
        listDiv.innerHTML = '<p class="loading">Carregando canais...</p>';

        try {
            const response = await fetch(`${API_URL}/channels/list`);
            const data = await response.json();

            if (data.channels && data.channels.length > 0) {
                listDiv.innerHTML = '';
                data.channels.forEach(channel => {
                    const card = document.createElement('div');
                    card.className = 'channel-card';
                    card.onclick = () => this.loadChannel(channel.channel_id);
                    card.innerHTML = `
                        <h3>${channel.name}</h3>
                        <p class="meta">📌 ${channel.sub_niche}</p>
                        <p class="meta">🎬 ${channel.videos_count} vídeos</p>
                        <p class="meta">📅 ${new Date(channel.created_at).toLocaleDateString('pt-BR')}</p>
                    `;
                    listDiv.appendChild(card);
                });
            } else {
                listDiv.innerHTML = '<p class="loading">Nenhum canal encontrado. Crie seu primeiro canal!</p>';
            }
        } catch (error) {
            listDiv.innerHTML = '<p class="loading">Erro ao carregar canais.</p>';
        }
    },

    async loadChannel(channelId) {
        this.showLoading();

        try {
            const response = await fetch(`${API_URL}/channel/load/${channelId}`);
            const data = await response.json();

            this.showLoading(false);

            if (data.success) {
                this.currentChannel = channelId;
                document.getElementById('current-channel-name').textContent = data.channel.name;
                document.getElementById('current-channel-info').textContent =
                    `${data.channel.sub_niche} • ${data.channel.videos.length} vídeos`;
                this.showSection('dashboard');
            } else {
                alert('Erro ao carregar canal');
            }
        } catch (error) {
            this.showLoading(false);
            alert('Erro: ' + error.message);
        }
    },

    async trainSystem() {
        const titlesText = document.getElementById('example-titles').value;
        const titles = titlesText.split('\n').filter(t => t.trim().length > 0);

        if (titles.length === 0) {
            alert('Adicione pelo menos um título de exemplo');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${API_URL}/channel/train`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ channel_id: this.currentChannel, titles })
            });

            const data = await response.json();
            this.showLoading(false);

            if (data.success) {
                const resultsDiv = document.getElementById('training-results');
                resultsDiv.style.display = 'block';
                resultsDiv.innerHTML = `
                    <h3>✅ Sistema Treinado!</h3>
                    <p><strong>${data.titles_learned}</strong> títulos aprendidos</p>
                    <div class="analysis-section">
                        <h4>Padrões Descobertos:</h4>
                        <p>O sistema analisou os títulos e começou a aprender os padrões do seu canal.</p>
                    </div>
                    <button onclick="app.showSection('dashboard')" class="btn btn-primary mt-20">
                        Continuar para Dashboard →
                    </button>
                `;
            }
        } catch (error) {
            this.showLoading(false);
            alert('Erro: ' + error.message);
        }
    },

    skipTraining() {
        if (confirm('Deseja pular o treinamento? O sistema terá menos precisão inicialmente.')) {
            this.showSection('dashboard');
        }
    },

    showValidateTitle() {
        this.showSection('validate-title');
    },

    async validateTitle() {
        const title = document.getElementById('title-input').value.trim();

        if (!title) {
            alert('Digite um título');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${API_URL}/title/validate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ channel_id: this.currentChannel, title })
            });

            const data = await response.json();
            this.showLoading(false);

            this.displayTitleAnalysis(data);
        } catch (error) {
            this.showLoading(false);
            alert('Erro: ' + error.message);
        }
    },

    displayTitleAnalysis(data) {
        const resultsDiv = document.getElementById('title-analysis-results');
        resultsDiv.style.display = 'block';

        const scoreClass = data.overall_score >= 80 ? 'score-excellent' :
                          data.overall_score >= 60 ? 'score-good' :
                          data.overall_score >= 40 ? 'score-warning' : 'score-danger';

        resultsDiv.innerHTML = `
            <div class="score-display ${scoreClass}">
                <div>SCORE GERAL</div>
                <div class="score-number">${Math.round(data.overall_score)}</div>
                <div>${data.final_recommendation}</div>
            </div>

            <div class="analysis-section">
                <h3>✅ Por que funciona:</h3>
                <ul class="analysis-list">
                    ${data.why_it_works.map(reason => `<li>${reason}</li>`).join('')}
                </ul>
            </div>

            <div class="analysis-section">
                <h3>⚠️ Riscos Identificados:</h3>
                <ul class="analysis-list">
                    ${data.why_risk.map(risk => `<li>${risk}</li>`).join('')}
                </ul>
            </div>

            <div class="analysis-section">
                <h3>📊 Análise Detalhada:</h3>
                <p><strong>Coerência com Canal:</strong> ${(data.vector_analysis.coherence_with_channel.score * 100).toFixed(1)}%</p>
                <p><strong>Alinhamento Semântico:</strong> ${(data.vector_analysis.semantic_analysis.channel_alignment * 100).toFixed(1)}%</p>
                <p><strong>Nível de Risco:</strong> ${data.vector_analysis.risk_assessment.risk_level}</p>
            </div>

            ${data.approved ? `
                <button onclick="app.copyApprovedTitle('${data.title.replace(/'/g, "\\'")}')" class="btn btn-primary mt-20">
                    ✅ Título Aprovado - Gerar Prompt de Roteiro →
                </button>
            ` : `
                <button onclick="app.showValidateTitle()" class="btn btn-warning mt-20">
                    ⚠️ Revisar e Testar Novo Título
                </button>
            `}
        `;
    },

    copyApprovedTitle(title) {
        document.getElementById('approved-title').value = title;
        this.showSection('generate-script');
    },

    showGenerateScript() {
        this.showSection('generate-script');
    },

    async generateScriptPrompt() {
        const title = document.getElementById('approved-title').value.trim();

        if (!title) {
            alert('Digite o título aprovado');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${API_URL}/script/generate-prompt`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ channel_id: this.currentChannel, title })
            });

            const data = await response.json();
            this.showLoading(false);

            if (data.success) {
                const resultsDiv = document.getElementById('script-prompt-results');
                resultsDiv.style.display = 'block';
                resultsDiv.innerHTML = `
                    <h3>📝 Prompt para Geração de Roteiro</h3>
                    <p>Use este prompt em ferramentas de IA (ChatGPT, Claude, etc.) para gerar seu roteiro:</p>

                    <div class="code-block" id="prompt-text">${this.escapeHtml(data.script_prompt)}</div>

                    <button onclick="app.copyToClipboard('prompt-text')" class="btn btn-primary">
                        📋 Copiar Prompt
                    </button>

                    <div class="analysis-section mt-20">
                        <h4>Diretrizes:</h4>
                        <ul class="analysis-list">
                            ${data.guidelines.map(g => `<li>${g}</li>`).join('')}
                        </ul>
                    </div>

                    <button onclick="app.copyTitleToScriptValidation('${title.replace(/'/g, "\\'")}'); app.showSection('validate-script')"
                            class="btn btn-primary mt-20">
                        Próximo: Validar Roteiro →
                    </button>
                `;
            }
        } catch (error) {
            this.showLoading(false);
            alert('Erro: ' + error.message);
        }
    },

    copyTitleToScriptValidation(title) {
        document.getElementById('script-title').value = title;
    },

    showValidateScript() {
        this.showSection('validate-script');
    },

    async validateScript() {
        const title = document.getElementById('script-title').value.trim();
        const script = document.getElementById('script-content').value.trim();

        if (!title || !script) {
            alert('Preencha título e roteiro');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${API_URL}/script/validate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ channel_id: this.currentChannel, title, script })
            });

            const data = await response.json();
            this.showLoading(false);

            this.displayScriptValidation(data);
        } catch (error) {
            this.showLoading(false);
            alert('Erro: ' + error.message);
        }
    },

    displayScriptValidation(data) {
        const resultsDiv = document.getElementById('script-validation-results');
        resultsDiv.style.display = 'block';

        resultsDiv.innerHTML = `
            <div class="score-display ${data.approved ? 'score-excellent' : 'score-warning'}">
                <div>${data.recommendation}</div>
            </div>

            <div class="analysis-section">
                <h3>📊 Coerência Título ↔ Roteiro:</h3>
                <p><strong>Score:</strong> ${(data.coherence_with_title.score * 100).toFixed(1)}%</p>
                <p>${data.coherence_with_title.message}</p>
            </div>

            <div class="analysis-section">
                <h3>📊 Coerência com Canal:</h3>
                <p><strong>Score:</strong> ${(data.coherence_with_channel.score * 100).toFixed(1)}%</p>
                <p>${data.coherence_with_channel.message}</p>
            </div>

            <div class="analysis-section">
                <h3>💬 Feedback:</h3>
                <ul class="analysis-list">
                    ${data.feedback.map(f => `<li>${f}</li>`).join('')}
                </ul>
            </div>

            ${data.approved ? `
                <button onclick="app.copyToContentGeneration('${data.title.replace(/'/g, "\\'")}'); app.showSection('generate-content')"
                        class="btn btn-primary mt-20">
                    ✅ Roteiro Aprovado - Gerar Conteúdo Complementar →
                </button>
            ` : `
                <button onclick="app.showValidateScript()" class="btn btn-warning mt-20">
                    ⚠️ Revisar Roteiro
                </button>
            `}
        `;
    },

    copyToContentGeneration(title) {
        document.getElementById('final-title').value = title;
        const script = document.getElementById('script-content').value;
        document.getElementById('final-script').value = script;
    },

    showGenerateContent() {
        this.showSection('generate-content');
    },

    async generateContent() {
        const title = document.getElementById('final-title').value.trim();
        const script = document.getElementById('final-script').value.trim();

        if (!title) {
            alert('Digite o título');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`${API_URL}/content/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ channel_id: this.currentChannel, title, script })
            });

            const data = await response.json();
            this.showLoading(false);

            if (data.success) {
                const resultsDiv = document.getElementById('content-generation-results');
                resultsDiv.style.display = 'block';
                resultsDiv.innerHTML = `
                    <h3>✅ Conteúdo Gerado com Sucesso!</h3>

                    <div class="analysis-section">
                        <h4>📝 Descrição do Vídeo:</h4>
                        <div class="code-block" id="description-text">${this.escapeHtml(data.description)}</div>
                        <button onclick="app.copyToClipboard('description-text')" class="btn btn-sm btn-primary">
                            📋 Copiar Descrição
                        </button>
                    </div>

                    <div class="analysis-section">
                        <h4>🏷️ Tags:</h4>
                        <p>${data.tags.join(', ')}</p>
                        <button onclick="app.copyText('${data.tags.join(', ')}')" class="btn btn-sm btn-primary">
                            📋 Copiar Tags
                        </button>
                    </div>

                    <div class="analysis-section">
                        <h4>🎨 Prompt para Thumbnail:</h4>
                        <div class="code-block" id="thumbnail-text">${this.escapeHtml(data.thumbnail_prompt)}</div>
                        <button onclick="app.copyToClipboard('thumbnail-text')" class="btn btn-sm btn-primary">
                            📋 Copiar Prompt
                        </button>
                    </div>

                    <button onclick="app.showSection('dashboard')" class="btn btn-primary mt-20">
                        ✅ Concluir e Voltar ao Dashboard
                    </button>
                `;
            }
        } catch (error) {
            this.showLoading(false);
            alert('Erro: ' + error.message);
        }
    },

    async showChannelSummary() {
        this.showLoading();

        try {
            const response = await fetch(`${API_URL}/channel/summary/${this.currentChannel}`);
            const data = await response.json();

            this.showLoading(false);

            const summaryDiv = document.getElementById('summary-content');
            summaryDiv.innerHTML = `
                <div class="summary-stat">
                    <h4>📊 Progresso de Aprendizado</h4>
                    <p>Títulos aprendidos: ${data.learning_progress.titles_learned}</p>
                    <p>Roteiros analisados: ${data.learning_progress.scripts_analyzed}</p>
                    <p>Total de dados de treinamento: ${data.learning_progress.total_training_data}</p>
                </div>

                <div class="summary-stat">
                    <h4>🎬 Vídeos</h4>
                    <p>Total: ${data.channel.videos.length}</p>
                </div>

                <div class="summary-stat">
                    <h4>🔑 Palavras-chave do Canal</h4>
                    <p>${data.channel.keywords.slice(0, 20).join(', ')}</p>
                </div>

                ${data.learned_guidelines.status !== 'learning' ? `
                    <div class="summary-stat">
                        <h4>📏 Diretrizes Aprendidas</h4>
                        <p>Comprimento ideal: ${data.learned_guidelines.recommended_length.min}-${data.learned_guidelines.recommended_length.max} caracteres</p>
                        <p>Palavras ideais: ${data.learned_guidelines.recommended_word_count.min}-${data.learned_guidelines.recommended_word_count.max} palavras</p>
                    </div>
                ` : ''}
            `;

            this.showSection('channel-summary');
        } catch (error) {
            this.showLoading(false);
            alert('Erro: ' + error.message);
        }
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML.replace(/\n/g, '<br>');
    },

    copyToClipboard(elementId) {
        const element = document.getElementById(elementId);
        const text = element.textContent;

        navigator.clipboard.writeText(text).then(() => {
            alert('Copiado para a área de transferência!');
        }).catch(err => {
            alert('Erro ao copiar: ' + err);
        });
    },

    copyText(text) {
        navigator.clipboard.writeText(text).then(() => {
            alert('Copiado!');
        });
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});
