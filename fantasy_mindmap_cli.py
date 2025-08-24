import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import numpy as np
import pandas as pd
from math import cos, sin, pi

class FantasyMindMapPlotly:
    def __init__(self):
        self.G = nx.DiGraph()
        self.pos = {}
        self.node_details = {}
        self.expanded_nodes = set()
        
        # Cores temáticas de fantasia medieval
        self.color_palette = {
            'session': '#8B4513',      # Marrom escuro - sessão principal
            'council': '#4169E1',      # Azul real - conclave
            'location': '#228B22',     # Verde floresta - locais
            'conflict': '#DC143C',     # Vermelho carmesim - conflitos
            'character': '#9932CC',    # Roxo - personagens
            'quest': '#FF8C00',        # Laranja escuro - missões
            'climax': '#8B0000',       # Vermelho escuro - clímax
            'subnode': '#DAA520'       # Dourado - sub-nós
        }
        
        self.symbols = {
            'session': 'star',
            'council': 'hexagon',
            'location': 'square',
            'conflict': 'diamond',
            'character': 'circle',
            'quest': 'pentagon',
            'climax': 'star-triangle-up',
            'subnode': 'hexagon'
        }
        
        self.setup_initial_graph()
        
    def setup_initial_graph(self):
        """Configura o grafo inicial com nós e arestas"""
        initial_nodes = [
            ('1', {'label': 'Sessão: Chegada a Elvedruin', 
                   'details': 'O grupo chega junto ao Elveranorien,\no Conclave dos Sábios, em Mirthond...', 
                   'color': 'session', 'pos': (0, 0)}),
            ('2', {'label': 'Conclave dos Sábios', 
                   'details': 'Sete anciões élficos,\ncada um representando\numa faceta do reino.', 
                   'color': 'council', 'pos': (3, -1)}),
            ('3', {'label': 'Locais Importantes', 
                   'details': 'Lugares icônicos de Mirthond,\ncomo a Sala dos Espelhos\ne a Ponte de Sirithar.', 
                   'color': 'location', 'pos': (3, 1)}),
            ('4', {'label': 'Pontos de Conflito', 
                   'details': 'Discussões no conselho entre\ndiplomacia, guerra, feitiços\ne elementais.', 
                   'color': 'conflict', 'pos': (6, -2)}),
            ('5', {'label': 'Personagens Secundários', 
                   'details': 'NPCs que influenciam\na intriga política\ne social.', 
                   'color': 'character', 'pos': (6, 0)}),
            ('6', {'label': 'Ganchos de Missão', 
                   'details': 'Diplomacia, Códice da Aurora,\nespião infiltrado\ne elemental.', 
                   'color': 'quest', 'pos': (6, 2)}),
            ('7', {'label': 'Clímax Possível', 
                   'details': 'Reunião final do conselho,\nlevando a guerra, ritual mágico\nou retração.', 
                   'color': 'climax', 'pos': (9, 0)})
        ]
        
        initial_edges = [
            ('1', '2'), ('1', '3'), ('2', '4'), 
            ('2', '5'), ('2', '6'), ('6', '7')
        ]
        
        # Adiciona nós ao grafo
        for node_id, attrs in initial_nodes:
            self.G.add_node(node_id, **attrs)
            self.pos[node_id] = attrs['pos']
            self.node_details[node_id] = attrs
            
        # Adiciona arestas
        self.G.add_edges_from(initial_edges)
    
    def expand_council_nodes(self):
        """Expande os sub-nós do Conclave dos Sábios"""
        if '2' in self.expanded_nodes:
            return
            
        council_members = [
            ('2a', {'label': 'Thalorien Lúmivarë', 
                   'details': 'Arquimago da Lua Pálida,\nlíder espiritual do conclave.\nMestre em magia lunar.', 
                   'color': 'subnode', 'pos': (5.5, -2.5)}),
            ('2b', {'label': 'Celadrien Veythil', 
                   'details': 'Senhora das Canções,\nguardiã da cultura élfica.\nPreserva as tradições ancestrais.', 
                   'color': 'subnode', 'pos': (5.5, -2)}),
            ('2c', {'label': 'Orandur Faeneth', 
                   'details': 'General pragmático,\nGuardião das Fronteiras.\nDefensor militar do reino.', 
                   'color': 'subnode', 'pos': (5.5, -1.5)}),
            ('2d', {'label': 'Irveth Alcarimë', 
                   'details': 'Mestre das Runas,\nestrategista arcano.\nEspecialista em magia antiga.', 
                   'color': 'subnode', 'pos': (5.5, -1)}),
            ('2e', {'label': 'Velindor Aerethil', 
                   'details': 'Diplomata experiente,\nbusca evitar a guerra\na todo custo.', 
                   'color': 'subnode', 'pos': (5.5, -0.5)}),
            ('2f', {'label': 'Nymirith Calerë', 
                   'details': 'Sacerdotisa da Árvore Anciã,\nligada à natureza\ne aos espíritos da floresta.', 
                   'color': 'subnode', 'pos': (5.5, 0)}),
            ('2g', {'label': 'Elmarion Túrath', 
                   'details': 'Guardião da história\ne dos tratados antigos.\nMemória viva do reino.', 
                   'color': 'subnode', 'pos': (5.5, 0.5)})
        ]
        
        # Adiciona membros do conclave
        for node_id, attrs in council_members:
            self.G.add_node(node_id, **attrs)
            self.pos[node_id] = attrs['pos']
            self.node_details[node_id] = attrs
            
            # Conecta ao nó principal
            self.G.add_edge('2', node_id)
            
        self.expanded_nodes.add('2')
    
    def create_plotly_graph(self, expand_council=False):
        """Cria o gráfico usando Plotly"""
        if expand_council:
            self.expand_council_nodes()
        
        # Prepara dados dos nós
        node_x = []
        node_y = []
        node_colors = []
        node_symbols = []
        node_sizes = []
        node_text = []
        node_hover = []
        
        for node in self.G.nodes():
            x, y = self.pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # Configurações do nó
            node_info = self.node_details[node]
            color_type = node_info['color']
            node_colors.append(self.color_palette[color_type])
            node_symbols.append(self.symbols[color_type])
            
            # Tamanho baseado no tipo
            if node in ['1', '7']:  # Nós principais
                node_sizes.append(40)
            elif node.startswith('2') and len(node) > 1:  # Sub-nós
                node_sizes.append(25)
            else:
                node_sizes.append(30)
            
            # Textos
            node_text.append(node)
            node_hover.append(f"<b>{node_info['label']}</b><br>" + 
                            node_info['details'].replace('\n', '<br>'))
        
        # Prepara dados das arestas
        edge_x = []
        edge_y = []
        
        for edge in self.G.edges():
            x0, y0 = self.pos[edge[0]]
            x1, y1 = self.pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Cria o gráfico
        fig = go.Figure()
        
        # Adiciona arestas
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#1f4e79'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
        
        # Adiciona nós
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(
                size=node_sizes,
                color=node_colors,
                symbol=node_symbols,
                line=dict(width=2, color='white')
            ),
            text=node_text,
            textposition="bottom center",
            textfont=dict(size=10, color='white'),
            hovertemplate='%{hovertext}<extra></extra>',
            hovertext=node_hover,
            showlegend=False
        ))
        
        # Configurações do layout
        fig.update_layout(
            title={
                'text': "🏰 Mapa Mental - Sessão de RPG Medieval 🏰",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=60),
            annotations=[ 
                dict(
                    text="Passe o mouse sobre os nós para ver detalhes",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    xanchor='left', yanchor='bottom',
                    font=dict(color='gray', size=12)
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117'
        )
        
        return fig
    
    def get_node_details(self, node_id):
        """Retorna detalhes de um nó específico"""
        if node_id in self.node_details:
            return self.node_details[node_id]['details']
        return "Nó não encontrado"


def main():
    st.set_page_config(page_title="Mapa Mental RPG", page_icon="🏰", layout="wide")
    
    st.title("🏰 Mapa Mental - Sessão de RPG Medieval")
    st.markdown("---")
    
    # Inicializa o mapa mental no session state
    if 'fantasy_map' not in st.session_state:
        st.session_state.fantasy_map = FantasyMindMapPlotly()
    
    # Sidebar para controles
    st.sidebar.header("🎮 Controles")
    
    # Botão para expandir conclave
    expand_council = st.sidebar.checkbox("Expandir Conclave dos Sábios", value=False)
    
    # Botão para mostrar detalhes
    show_details = st.sidebar.checkbox("Mostrar Painel de Detalhes", value=True)
    
    # Selector de nó para detalhes
    node_options = list(st.session_state.fantasy_map.G.nodes())
    selected_node = st.sidebar.selectbox(
        "Selecione um nó para ver detalhes:",
        options=node_options,
        format_func=lambda x: f"{x}: {st.session_state.fantasy_map.node_details[x]['label']}"
    )
    
    # Layout principal
    if show_details:
        col1, col2 = st.columns([3, 1])
    else:
        col1 = st.container()
    
    with col1:
        st.subheader("📊 Mapa Mental Interativo")
        
        # Plota o mapa usando Plotly
        fig = st.session_state.fantasy_map.create_plotly_graph(expand_council=expand_council)
        st.plotly_chart(fig, use_container_width=True)
    
    if show_details:
        with col2:
            st.subheader("📋 Detalhes do Nó")
            
            if selected_node:
                node_info = st.session_state.fantasy_map.node_details[selected_node]
                
                st.markdown(f"**ID:** `{selected_node}`")
                st.markdown(f"**Título:** {node_info['label']}")
                st.markdown(f"**Categoria:** {node_info['color'].title()}")
                
                # Mostra cor do nó
                color = st.session_state.fantasy_map.color_palette[node_info['color']]
                st.markdown(f"**Cor:** <span style='color: {color}'>●</span> {color}", 
                           unsafe_allow_html=True)
                
                st.markdown("**Descrição:**")
                st.text_area("", value=node_info['details'], height=100, disabled=True)
    
    # Legenda de elementos
    st.markdown("---")
    st.subheader("🎨 Legenda de Elementos")
    
    cols = st.columns(4)
    categories = list(st.session_state.fantasy_map.color_palette.items())
    
    category_names = {
        'session': '📜 Sessão Principal',
        'council': '👑 Conclave dos Sábios',
        'location': '🏰 Locais Importantes',
        'conflict': '⚔️ Pontos de Conflito',
        'character': '🧙 Personagens',
        'quest': '🗺️ Ganchos de Missão',
        'climax': '💀 Clímax',
        'subnode': '✨ Membros do Conclave'
    }
    
    for i, (category, color) in enumerate(categories):
        with cols[i % 4]:
            st.markdown(f"<span style='color: {color}; font-size: 20px'>●</span> {category_names.get(category, category)}", 
                       unsafe_allow_html=True)
    
    # Lista de todos os nós
    st.markdown("---")
    st.subheader("📝 Explorar Todos os Nós")
    
    tab1, tab2, tab3 = st.tabs(["🎭 Personagens & Conselho", "🏰 Locais & Missões", "⚔️ Conflitos & Clímax"])
    
    with tab1:
        for node_id in st.session_state.fantasy_map.G.nodes():
            node_info = st.session_state.fantasy_map.node_details[node_id]
            if node_info['color'] in ['council', 'character', 'subnode']:
                with st.expander(f"{node_id}: {node_info['label']}"):
                    col_a, col_b = st.columns([1, 3])
                    with col_a:
                        color = st.session_state.fantasy_map.color_palette[node_info['color']]
                        st.markdown(f"<div style='width: 50px; height: 50px; background-color: {color}; border-radius: 10px; margin: 10px 0;'></div>", 
                                   unsafe_allow_html=True)
                    with col_b:
                        st.write(f"**Categoria:** {node_info['color'].title()}")
                        st.text(node_info['details'])
    
    with tab2:
        for node_id in st.session_state.fantasy_map.G.nodes():
            node_info = st.session_state.fantasy_map.node_details[node_id]
            if node_info['color'] in ['location', 'quest', 'session']:
                with st.expander(f"{node_id}: {node_info['label']}"):
                    col_a, col_b = st.columns([1, 3])
                    with col_a:
                        color = st.session_state.fantasy_map.color_palette[node_info['color']]
                        st.markdown(f"<div style='width: 50px; height: 50px; background-color: {color}; border-radius: 10px; margin: 10px 0;'></div>", 
                                   unsafe_allow_html=True)
                    with col_b:
                        st.write(f"**Categoria:** {node_info['color'].title()}")
                        st.text(node_info['details'])
    
    with tab3:
        for node_id in st.session_state.fantasy_map.G.nodes():
            node_info = st.session_state.fantasy_map.node_details[node_id]
            if node_info['color'] in ['conflict', 'climax']:
                with st.expander(f"{node_id}: {node_info['label']}"):
                    col_a, col_b = st.columns([1, 3])
                    with col_a:
                        color = st.session_state.fantasy_map.color_palette[node_info['color']]
                        st.markdown(f"<div style='width: 50px; height: 50px; background-color: {color}; border-radius: 10px; margin: 10px 0;'></div>", 
                                   unsafe_allow_html=True)
                    with col_b:
                        st.write(f"**Categoria:** {node_info['color'].title()}")
                        st.text(node_info['details'])
    
    # Footer
    st.markdown("---")
    st.markdown("*Criado para sessões de RPG medieval - Explore as conexões narrativas!*")
    st.info("💡 **Dica:** Passe o mouse sobre os nós no gráfico para ver detalhes rápidos!")


if __name__ == "__main__":
    main()
