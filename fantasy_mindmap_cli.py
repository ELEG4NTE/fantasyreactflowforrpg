import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import networkx as nx
import numpy as np
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import matplotlib.image as mpimg

class FantasyMindMap:
    def __init__(self):
        self.G = nx.DiGraph()
        self.pos = {}
        self.node_colors = {}
        self.node_details = {}
        self.selected_node = None
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
            self.node_colors[node_id] = self.color_palette[attrs['color']]
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
            self.node_colors[node_id] = self.color_palette[attrs['color']]
            self.node_details[node_id] = attrs
            
            # Conecta ao nó principal
            self.G.add_edge('2', node_id)
            
        self.expanded_nodes.add('2')
    
    def create_fantasy_node_style(self, ax, node_id, x, y, label, color):
        """Cria estilo visual de fantasia para os nós"""
        # Tamanho baseado no tipo de nó
        base_size = 0.3
        if node_id in ['1', '7']:  # Nós principais
            size = base_size * 1.5
        elif node_id.startswith('2') and len(node_id) > 1:  # Sub-nós
            size = base_size * 0.8
        else:
            size = base_size
            
        # Cria forma ornamentada (hexágono para magia, círculo para personagens, etc.)
        if 'council' in self.node_details[node_id]['color'] or 'subnode' in self.node_details[node_id]['color']:
            # Hexágono mágico para conselheiros
            angles = np.linspace(0, 2*np.pi, 7)
            hex_x = x + size * np.cos(angles)
            hex_y = y + size * np.sin(angles)
            polygon = plt.Polygon(list(zip(hex_x, hex_y)), 
                                color=color, alpha=0.8, 
                                edgecolor='gold', linewidth=2)
            ax.add_patch(polygon)
            
        elif 'conflict' in self.node_details[node_id]['color']:
            # Losango para conflitos
            diamond = mpatches.RegularPolygon((x, y), 4, radius=size, 
                                            orientation=np.pi/4,
                                            facecolor=color, alpha=0.8,
                                            edgecolor='darkred', linewidth=2)
            ax.add_patch(diamond)
            
        elif 'location' in self.node_details[node_id]['color']:
            # Retângulo ornamentado para locais
            rect = FancyBboxPatch((x-size, y-size*0.7), size*2, size*1.4,
                                boxstyle="round,pad=0.1",
                                facecolor=color, alpha=0.8,
                                edgecolor='darkgreen', linewidth=2)
            ax.add_patch(rect)
            
        else:
            # Círculo padrão com borda ornamentada
            circle = Circle((x, y), size, facecolor=color, alpha=0.8,
                          edgecolor='black', linewidth=2)
            ax.add_patch(circle)
            
        # Adiciona símbolo de fantasia no centro
        self.add_fantasy_symbol(ax, x, y, node_id, size)
        
        # Texto do label
        ax.text(x, y-size-0.3, label, ha='center', va='top', 
               fontsize=8, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    def add_fantasy_symbol(self, ax, x, y, node_id, size):
        """Adiciona símbolos de fantasia aos nós"""
        symbol_size = size * 0.6
        
        node_type = self.node_details[node_id]['color']
        
        if node_type == 'council' or node_type == 'subnode':
            # Estrela mágica
            angles = np.linspace(0, 2*np.pi, 6, endpoint=False)
            star_x = x + symbol_size * 0.3 * np.cos(angles)
            star_y = y + symbol_size * 0.3 * np.sin(angles)
            ax.plot([x, star_x[0]], [y, star_y[0]], 'white', linewidth=2)
            ax.plot([x, star_x[2]], [y, star_y[2]], 'white', linewidth=2)
            ax.plot([x, star_x[4]], [y, star_y[4]], 'white', linewidth=2)
            
        elif node_type == 'conflict':
            # Espadas cruzadas
            ax.plot([x-symbol_size*0.3, x+symbol_size*0.3], 
                   [y-symbol_size*0.3, y+symbol_size*0.3], 'white', linewidth=3)
            ax.plot([x-symbol_size*0.3, x+symbol_size*0.3], 
                   [y+symbol_size*0.3, y-symbol_size*0.3], 'white', linewidth=3)
            
        elif node_type == 'location':
            # Torre/castelo
            ax.plot([x, x], [y-symbol_size*0.3, y+symbol_size*0.3], 'white', linewidth=3)
            ax.plot([x-symbol_size*0.2, x+symbol_size*0.2], 
                   [y+symbol_size*0.3, y+symbol_size*0.3], 'white', linewidth=3)
            
        elif node_type == 'character':
            # Coroa
            crown_x = [x-symbol_size*0.3, x-symbol_size*0.1, x, 
                      x+symbol_size*0.1, x+symbol_size*0.3]
            crown_y = [y, y+symbol_size*0.2, y+symbol_size*0.3, 
                      y+symbol_size*0.2, y]
            ax.plot(crown_x, crown_y, 'white', linewidth=2)
            
        elif node_type == 'quest':
            # Pergaminho
            ax.add_patch(mpatches.Rectangle((x-symbol_size*0.3, y-symbol_size*0.2), 
                                          symbol_size*0.6, symbol_size*0.4,
                                          facecolor='white', alpha=0.8))
            
        elif node_type == 'session' or node_type == 'climax':
            # Dragão simplificado
            ax.plot([x-symbol_size*0.3, x, x+symbol_size*0.3], 
                   [y, y+symbol_size*0.2, y], 'white', linewidth=3)
    
    def draw_fantasy_edges(self, ax):
        """Desenha arestas com estilo de fantasia"""
        for edge in self.G.edges():
            start_pos = self.pos[edge[0]]
            end_pos = self.pos[edge[1]]
            
            # Linha curvada mágica
            mid_x = (start_pos[0] + end_pos[0]) / 2
            mid_y = (start_pos[1] + end_pos[1]) / 2 + 0.1
            
            # Bezier curve simulation
            t = np.linspace(0, 1, 20)
            curve_x = (1-t)**2 * start_pos[0] + 2*(1-t)*t * mid_x + t**2 * end_pos[0]
            curve_y = (1-t)**2 * start_pos[1] + 2*(1-t)*t * mid_y + t**2 * end_pos[1]
            
            ax.plot(curve_x, curve_y, 'darkblue', linewidth=2, alpha=0.7)
            
            # Seta no final
            dx = end_pos[0] - curve_x[-2]
            dy = end_pos[1] - curve_y[-2]
            ax.annotate('', xy=end_pos, xytext=(curve_x[-2], curve_y[-2]),
                       arrowprops=dict(arrowstyle='->', color='darkblue', lw=2))
    
    def plot_mindmap(self, expand_council=False):
        """Plota o mapa mental com tema de fantasia"""
        if expand_council:
            self.expand_council_nodes()
        
        # Configuração da figura
        fig, (ax_main, ax_detail) = plt.subplots(1, 2, figsize=(16, 10))
        fig.suptitle('🏰 Mapa Mental - Sessão de RPG Medieval 🏰', 
                    fontsize=16, fontweight='bold')
        
        # Configura o eixo principal
        ax_main.set_xlim(-1, 10)
        ax_main.set_ylim(-3, 3)
        ax_main.set_aspect('equal')
        ax_main.axis('off')
        ax_main.set_facecolor('#001122')  # Fundo azul escuro noturno
        
        # Adiciona estrelas no fundo
        np.random.seed(42)
        star_x = np.random.uniform(-1, 10, 50)
        star_y = np.random.uniform(-3, 3, 50)
        ax_main.scatter(star_x, star_y, c='white', s=1, alpha=0.3)
        
        # Desenha arestas
        self.draw_fantasy_edges(ax_main)
        
        # Desenha nós
        for node_id in self.G.nodes():
            x, y = self.pos[node_id]
            label = self.node_details[node_id]['label']
            color = self.node_colors[node_id]
            self.create_fantasy_node_style(ax_main, node_id, x, y, label, color)
        
        # Painel de detalhes
        ax_detail.axis('off')
        ax_detail.set_xlim(0, 1)
        ax_detail.set_ylim(0, 1)
        
        # Legenda de cores
        legend_elements = []
        y_pos = 0.9
        ax_detail.text(0.1, 0.95, '🗡️ Legenda de Elementos', 
                      fontsize=14, fontweight='bold')
        
        for category, color in self.color_palette.items():
            legend_elements.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=color))
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
            ax_detail.text(0.15, y_pos, category_names.get(category, category), 
                          fontsize=10)
            circle = Circle((0.1, y_pos+0.01), 0.02, facecolor=color, alpha=0.8)
            ax_detail.add_patch(circle)
            y_pos -= 0.08
        
        # Instruções
        ax_detail.text(0.1, 0.3, '📖 Instruções:', fontsize=12, fontweight='bold')
        instructions = [
            '• Clique nos nós para expandir',
            '• Cores representam categorias',
            '• Símbolos indicam tipo de elemento',
            '• Setas mostram conexões narrativas'
        ]
        
        y_pos = 0.25
        for instruction in instructions:
            ax_detail.text(0.1, y_pos, instruction, fontsize=10)
            y_pos -= 0.04
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def get_node_details(self, node_id):
        """Retorna detalhes de um nó específico"""
        if node_id in self.node_details:
            return self.node_details[node_id]['details']
        return "Nó não encontrado"
    
    def interactive_exploration(self):
        """Versão interativa para explorar o mapa"""
        print("🏰 Bem-vindo ao Mapa Mental de RPG Medieval! 🏰")
        print("\nComandos disponíveis:")
        print("- 'plot': Visualizar o mapa")
        print("- 'expand': Expandir o Conclave dos Sábios")
        print("- 'details [id]': Ver detalhes de um nó")
        print("- 'nodes': Listar todos os nós")
        print("- 'quit': Sair\n")
        
        while True:
            command = input("Digite um comando: ").strip().lower()
            
            if command == 'quit':
                print("Até a próxima aventura! 🗡️")
                break
            elif command == 'plot':
                self.plot_mindmap()
            elif command == 'expand':
                self.plot_mindmap(expand_council=True)
                print("Conclave expandido!")
            elif command.startswith('details'):
                parts = command.split()
                if len(parts) > 1:
                    node_id = parts[1]
                    details = self.get_node_details(node_id)
                    print(f"\n📋 Detalhes do nó {node_id}:")
                    print(details)
                else:
                    print("Por favor, especifique um ID de nó")
            elif command == 'nodes':
                print("\n🗂️ Nós disponíveis:")
                for node_id in self.G.nodes():
                    label = self.node_details[node_id]['label']
                    print(f"  {node_id}: {label}")
            else:
                print("Comando não reconhecido. Digite 'quit' para sair.")

# Exemplo de uso
if __name__ == "__main__":
    # Cria o mapa mental
    fantasy_map = FantasyMindMap()
    
    # Plota o mapa básico
    fantasy_map.plot_mindmap()
    
    # Para versão interativa, descomente a linha abaixo:
    # fantasy_map.interactive_exploration()