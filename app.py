import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import time
import math
from typing import Dict, List, Tuple
import base64
from io import BytesIO

# Page config
st.set_page_config(
    page_title="SBCL Genesis v2.0",
    page_icon="⧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and vibrant colors
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #0a0f1c, #1a1f2e);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00f0ff;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
    }
    .main-subtitle {
        font-size: 1.2rem;
        color: #9f4aff;
        font-weight: 500;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid;
        margin: 0.5rem 0;
    }
    .disease-info {
        background: linear-gradient(135deg, rgba(255, 51, 102, 0.1), rgba(170, 102, 255, 0.1));
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stSelectbox > div > div {
        background-color: #1a1f2e;
    }
    .stSlider > div > div > div {
        background-color: #1a1f2e;
    }
</style>
""", unsafe_allow_html=True)

class SBCLGenesis:
    def __init__(self):
        self.language_configs = {
            'Basic': {
                'membrane': {'name': 'Drug Delivery', 'desc': 'How well the drug gets through cell walls'},
                'entropy': {'name': 'Disease Recognition', 'desc': 'How well the drug recognizes diseased cells'},
                'structural': {'name': 'Drug Flexibility', 'desc': 'How well the drug adapts its shape'},
                'charge': {'name': 'Electric Attraction', 'desc': 'Electric charge helps stick to targets'},
                'selectivity': {'name': 'Precision Targeting', 'desc': 'How precisely it attacks only disease cells'},
                'stability': {'name': 'Drug Durability', 'desc': 'How long the drug stays active'}
            },
            'Scientific': {
                'membrane': {'name': 'Membrane Permeability', 'desc': 'Molecular passage through cellular barriers'},
                'entropy': {'name': 'Entropy Coupling', 'desc': 'Resonance with disorder\'s chaotic patterns'},
                'structural': {'name': 'Structural Adaptability', 'desc': 'Molecular flexibility and dynamics'},
                'charge': {'name': 'Charge Distribution', 'desc': 'Electrostatic field alignment'},
                'selectivity': {'name': 'Target Selectivity', 'desc': 'Precision of molecular recognition'},
                'stability': {'name': 'Symbolic Stability', 'desc': 'Resistance to field decay'}
            },
            'Symbolic': {
                'membrane': {'name': 'Veil Threading', 'desc': 'Gracefully piercing cellular veils'},
                'entropy': {'name': 'Chaos Dancing', 'desc': 'Communion with disorder\'s hidden patterns'},
                'structural': {'name': 'Form Wisdom', 'desc': 'Sacred balance between flow and permanence'},
                'charge': {'name': 'Electric Soul', 'desc': 'Spiritual polarity guiding essence'},
                'selectivity': {'name': 'Divine Precision', 'desc': 'Recognizing darkness from light'},
                'stability': {'name': 'Eternal Coherence', 'desc': 'Resistance to entropy\'s dissolution'}
            },
            'Mathematical': {
                'membrane': {'name': 'Permeability Coefficient', 'desc': 'Diffusion rate constant (log P)'},
                'entropy': {'name': 'Information Entropy', 'desc': 'Shannon entropy of binding states'},
                'structural': {'name': 'Conformational Energy', 'desc': 'Free energy barrier (kcal/mol)'},
                'charge': {'name': 'Electrostatic Potential', 'desc': 'Net charge distribution (Coulombs)'},
                'selectivity': {'name': 'Binding Specificity', 'desc': 'On/off-target binding ratio'},
                'stability': {'name': 'Thermodynamic Stability', 'desc': 'Gibbs free energy (ΔG°)'}
            }
        }
        
        self.disease_profiles = {
            'Cancer (Entropy Pattern)': {
                'color': '#ff3366', 'frequency': 1.2, 'amplitude': 0.8, 'chaos': 0.9, 'phase': 0
            },
            'Alzheimer\'s (Protein Misfolding)': {
                'color': '#aa66ff', 'frequency': 0.8, 'amplitude': 0.6, 'chaos': 0.7, 'phase': math.pi/4
            },
            'Chronic Inflammation': {
                'color': '#ff9900', 'frequency': 1.0, 'amplitude': 0.9, 'chaos': 0.6, 'phase': math.pi/2
            },
            'Type 2 Diabetes': {
                'color': '#3388ff', 'frequency': 0.6, 'amplitude': 0.7, 'chaos': 0.5, 'phase': math.pi/3
            },
            'Autoimmune Disorders': {
                'color': '#ff4488', 'frequency': 1.4, 'amplitude': 0.85, 'chaos': 0.8, 'phase': math.pi/6
            }
        }
        
        self.molecular_structures = {
            'simple': {'id': 'SBCL-2024-S1A2', 'mw': 156.2, 'logP': 1.2, 'hbd': 1, 'hba': 2},
            'medium': {'id': 'SBCL-2024-A7X3', 'mw': 342.7, 'logP': 2.4, 'hbd': 3, 'hba': 5},
            'complex': {'id': 'SBCL-2024-Z9Q7', 'mw': 487.3, 'logP': 3.1, 'hbd': 4, 'hba': 7},
            'advanced': {'id': 'SBCL-2024-Ω4Ψ6', 'mw': 623.8, 'logP': 4.2, 'hbd': 2, 'hba': 4}
        }

    def generate_wave_data(self, params: Dict, disease_profile: Dict, t: float = 0) -> Tuple[np.ndarray, np.ndarray, List]:
        """Generate therapeutic wave interference patterns with disease signatures"""
        x = np.linspace(0, 10, 1000)
        
        # Parameter influences
        entropy_influence = params['entropy']
        membrane_influence = params['membrane'] / 5
        selectivity_influence = params['selectivity']
        stability_influence = params['stability'] / 5
        charge_influence = abs(params['charge']) / 2
        
        # Disease signature
        disease_freq = disease_profile['frequency']
        disease_amp = disease_profile['amplitude']
        disease_chaos = disease_profile['chaos']
        
        # Generate multiple wave layers with vibrant colors
        waves = []
        colors = ['#00ffcc', '#ff66ff', '#66ccff', '#ccff66', '#ff9966', '#9966ff']
        
        for i in range(6):
            layer_amp = (12 + i * 3) * (0.4 + entropy_influence * disease_amp + charge_influence * 0.3)
            layer_freq = (0.6 + i * 0.2) * disease_freq * (0.6 + membrane_influence * 0.5 + selectivity_influence * 0.4)
            layer_phase = (i * math.pi/6) + (stability_influence * math.pi/4) + disease_profile['phase']
            
            # Primary therapeutic wave
            primary_wave = layer_amp * np.sin(layer_freq * x + t + layer_phase)
            
            # Disease chaos component
            chaos_wave = (layer_amp * 0.2 * disease_chaos) * np.sin(
                layer_freq * 3.7 * x + t * 2.1 + layer_phase + math.pi/7
            )
            
            # Therapeutic response
            therapeutic_response = (layer_amp * 0.25 * selectivity_influence) * np.sin(
                layer_freq * x + t * 0.8 + layer_phase + math.pi
            )
            
            wave = primary_wave + chaos_wave + therapeutic_response
            
            # Add disease signature (dashed overlay) for specific layers
            disease_signature = None
            if i in [1, 3]:  # Add disease signature to layers 2 and 4
                disease_signature = layer_amp * 0.7 * np.sin(
                    layer_freq * 1.3 * x + t * 1.2 + layer_phase
                ) + layer_amp * 0.3 * disease_chaos * np.sin(
                    layer_freq * 2.7 * x + t * 1.8 + layer_phase + math.pi/3
                )
            
            waves.append({
                'x': x,
                'y': wave + i * 0.8,  # Offset layers vertically
                'color': colors[i % len(colors)],
                'opacity': min(0.4 + entropy_influence * 0.3 + selectivity_influence * 0.2, 0.9),
                'disease_signature': disease_signature + i * 0.8 if disease_signature is not None else None
            })
        
        return x, waves

    def calculate_scores(self, params: Dict, disease_profile: Dict) -> Dict:
        """Calculate therapeutic performance scores"""
        # Individual score calculations
        stability_score = min(100, params['stability'] * 20)
        coupling_score = min(100, params['entropy'] * 100 * disease_profile['chaos'])
        entropy_align_score = min(100, params['entropy'] * 80 + 20)
        selectivity_score = min(100, params['selectivity'] * 100)
        coherence_score = min(100, 60 + params['selectivity'] * 30 + params['stability'] * 8)
        
        # Overall phase lock calculation
        membrane_score = min(100, max(0, 100 - abs(params['membrane'] - 2.5) * 20))
        charge_score = min(100, max(0, 100 - abs(params['charge'] + 1.0) * 25))
        structural_score = min(100, max(0, 100 - abs(params['structural'] - 3.0) * 15))
        
        phase_lock = round(
            membrane_score * 0.15 + coupling_score * 0.25 + structural_score * 0.15 + 
            charge_score * 0.15 + selectivity_score * 0.20 + stability_score * 0.10
        )
        
        return {
            'stability': stability_score,
            'coupling': coupling_score,
            'entropy_align': entropy_align_score,
            'selectivity': selectivity_score,
            'coherence': coherence_score,
            'phase_lock': phase_lock
        }

    def get_molecular_complexity(self, params: Dict) -> str:
        """Determine molecular complexity based on parameters"""
        total_complexity = (
            params['membrane'] + params['entropy'] * 5 + params['structural'] + 
            abs(params['charge']) + params['selectivity'] * 3 + params['stability']
        )
        
        if total_complexity < 6: return 'simple'
        elif total_complexity < 10: return 'medium'
        elif total_complexity < 14: return 'complex'
        else: return 'advanced'

def main():
    # Initialize app
    app = SBCLGenesis()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">⧬ SBCL Genesis v2.0</div>
        <div class="main-subtitle">Symbolic Therapeutic Design Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Controls
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # Language selection
        language = st.selectbox(
            "Interface Language",
            options=['Basic', 'Scientific', 'Symbolic', 'Mathematical'],
            index=1,
            help="Select your preferred terminology level"
        )
        
        # Disease selection
        disease = st.selectbox(
            "🎯 Target Disorder",
            options=list(app.disease_profiles.keys()),
            help="Select the disease pattern to target"
        )
        
        st.markdown("---")
        st.subheader(f"🧬 {app.language_configs[language]['membrane']['name']}")
        
        # Parameter sliders with dynamic labels
        config = app.language_configs[language]
        
        membrane = st.slider(
            config['membrane']['name'],
            min_value=0.0, max_value=5.0, value=2.3, step=0.1,
            help=config['membrane']['desc']
        )
        
        entropy = st.slider(
            config['entropy']['name'],
            min_value=0.0, max_value=1.0, value=0.47, step=0.01,
            help=config['entropy']['desc']
        )
        
        structural = st.slider(
            config['structural']['name'],
            min_value=0.0, max_value=5.0, value=2.8, step=0.1,
            help=config['structural']['desc']
        )
        
        charge = st.slider(
            config['charge']['name'],
            min_value=-2.0, max_value=2.0, value=-0.8, step=0.1,
            help=config['charge']['desc']
        )
        
        selectivity = st.slider(
            config['selectivity']['name'],
            min_value=0.0, max_value=1.0, value=0.74, step=0.01,
            help=config['selectivity']['desc']
        )
        
        stability = st.slider(
            config['stability']['name'],
            min_value=0.0, max_value=5.0, value=3.2, step=0.1,
            help=config['stability']['desc']
        )
        
        # Real-time animation toggle
        st.markdown("---")
        animate = st.checkbox("🌊 Real-time Animation", value=True)
    
    # Main content area
    params = {
        'membrane': membrane, 'entropy': entropy, 'structural': structural,
        'charge': charge, 'selectivity': selectivity, 'stability': stability
    }
    
    disease_profile = app.disease_profiles[disease]
    scores = app.calculate_scores(params, disease_profile)
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🎯 Phase Lock",
            f"{scores['phase_lock']}%",
            delta=f"{'Excellent' if scores['phase_lock'] >= 90 else 'Good' if scores['phase_lock'] >= 75 else 'Moderate'}"
        )
    
    with col2:
        st.metric("🔗 Coupling", f"{scores['coupling']:.1f}")
    
    with col3:
        st.metric("🎲 Entropy Align", f"{scores['entropy_align']:.1f}")
    
    with col4:
        st.metric("🛡️ Selectivity", f"{scores['selectivity']:.1f}")
    
    # Main visualization area
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.subheader("🌊 Therapeutic Wave Field Visualization")
        
        # Create wave visualization
        if animate:
            # Use session state to maintain animation time
            if 'animation_time' not in st.session_state:
                st.session_state.animation_time = 0
            
            # Create placeholder for animation
            chart_placeholder = st.empty()
            
            # Animation loop
            for i in range(60):  # 60 frames
                t = st.session_state.animation_time + i * 0.1
                x, waves = app.generate_wave_data(params, disease_profile, t)
                
                fig = go.Figure()
                
                # Add therapeutic waves
                for j, wave in enumerate(waves):
                    fig.add_trace(go.Scatter(
                        x=wave['x'], y=wave['y'],
                        mode='lines',
                        line=dict(color=wave['color'], width=3),
                        opacity=wave['opacity'],
                        name=f'Therapeutic Layer {j+1}',
                        showlegend=False
                    ))
                    
                    # Add disease signature overlays
                    if wave['disease_signature'] is not None:
                        fig.add_trace(go.Scatter(
                            x=wave['x'], y=wave['disease_signature'],
                            mode='lines',
                            line=dict(color=disease_profile['color'], width=2, dash='dash'),
                            opacity=0.8,
                            name=f'Disease Signature {j+1}',
                            showlegend=False
                        ))
                
                fig.update_layout(
                    title=f"Phase Correlation: {scores['phase_lock']}% Lock Achieved",
                    xaxis_title="Spatial Domain",
                    yaxis_title="Field Amplitude",
                    height=500,
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                
                if not animate:
                    break
                    
                time.sleep(0.05)  # Control animation speed
            
            st.session_state.animation_time += 6  # Update for next cycle
        
        else:
            # Static visualization
            x, waves = app.generate_wave_data(params, disease_profile)
            
            fig = go.Figure()
            
            for j, wave in enumerate(waves):
                fig.add_trace(go.Scatter(
                    x=wave['x'], y=wave['y'],
                    mode='lines',
                    line=dict(color=wave['color'], width=3),
                    opacity=wave['opacity'],
                    name=f'Therapeutic Layer {j+1}'
                ))
                
                if wave['disease_signature'] is not None:
                    fig.add_trace(go.Scatter(
                        x=wave['x'], y=wave['disease_signature'],
                        mode='lines',
                        line=dict(color=disease_profile['color'], width=2, dash='dash'),
                        opacity=0.8,
                        name=f'Disease Signature {j+1}'
                    ))
            
            fig.update_layout(
                title=f"Therapeutic Field Synchronization - {scores['phase_lock']}% Phase Lock",
                xaxis_title="Spatial Domain",
                yaxis_title="Field Amplitude",
                height=500,
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("📊 Performance Metrics")
        
        # Score breakdown
        scores_data = {
            'Metric': ['Stability', 'Coupling', 'Entropy', 'Selectivity', 'Coherence'],
            'Score': [scores['stability'], scores['coupling'], scores['entropy_align'], 
                     scores['selectivity'], scores['coherence']]
        }
        
        fig_bar = px.bar(
            scores_data, x='Score', y='Metric', orientation='h',
            color='Score', color_continuous_scale='Viridis',
            title="Real-Time Scoring"
        )
        fig_bar.update_layout(height=300, template='plotly_dark', showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Disease info
        st.markdown(f"""
        <div class="disease-info">
            <h4>🎯 {disease}</h4>
            <p><strong>Signature Color:</strong> <span style="color: {disease_profile['color']}">{disease_profile['color']}</span></p>
            <p><strong>Chaos Level:</strong> {disease_profile['chaos']:.2f}</p>
            <p><strong>Frequency:</strong> {disease_profile['frequency']:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Bottom section - Molecular structure and export
    st.markdown("---")
    col_mol, col_export = st.columns([2, 1])
    
    with col_mol:
        st.subheader("🧬 Generated Molecular Candidate")
        
        complexity = app.get_molecular_complexity(params)
        mol_data = app.molecular_structures[complexity]
        
        # Molecular properties table
        mol_df = pd.DataFrame({
            'Property': ['Molecule ID', 'Molecular Weight', 'LogP', 'H-Bond Donors', 'H-Bond Acceptors'],
            'Value': [mol_data['id'], f"{mol_data['mw']} Da", mol_data['logP'], 
                     mol_data['hbd'], mol_data['hba']],
            'Assessment': ['Generated', 'Good' if mol_data['mw'] < 500 else 'High', 
                          'Optimal' if 0 <= mol_data['logP'] <= 5 else 'Suboptimal',
                          'Good' if mol_data['hbd'] <= 5 else 'High',
                          'Good' if mol_data['hba'] <= 10 else 'High']
        })
        
        st.dataframe(mol_df, use_container_width=True)
        
        # Drug-likeness assessment
        violations = 0
        if mol_data['mw'] > 500: violations += 1
        if mol_data['logP'] > 5: violations += 1
        if mol_data['hbd'] > 5: violations += 1
        if mol_data['hba'] > 10: violations += 1
        
        drug_like = "✅ Lipinski Compliant" if violations == 0 else f"⚠️ {violations} Lipinski Violations"
        st.success(drug_like)
    
    with col_export:
        st.subheader("📤 Export Options")
        
        # Export buttons
        if st.button("📄 Generate Report", use_container_width=True):
            report_data = {
                'parameters': params,
                'scores': scores,
                'disease': disease,
                'molecule': mol_data,
                'phase_lock': scores['phase_lock']
            }
            
            report_text = f"""
SBCL Genesis v2.0 - Therapeutic Report
=====================================
Generated: {pd.Timestamp.now()}

Target Disorder: {disease}
Phase Lock: {scores['phase_lock']}%
Molecule ID: {mol_data['id']}

Parameters:
- Membrane: {params['membrane']:.2f}
- Entropy: {params['entropy']:.2f}  
- Structural: {params['structural']:.2f}
- Charge: {params['charge']:.2f}
- Selectivity: {params['selectivity']:.2f}
- Stability: {params['stability']:.2f}

Performance Scores:
- Stability: {scores['stability']:.1f}
- Coupling: {scores['coupling']:.1f}
- Entropy Align: {scores['entropy_align']:.1f}
- Selectivity: {scores['selectivity']:.1f}
- Coherence: {scores['coherence']:.1f}

Molecular Properties:
- MW: {mol_data['mw']} Da
- LogP: {mol_data['logP']}
- HBD: {mol_data['hbd']}
- HBA: {mol_data['hba']}

Assessment: {drug_like}
Recommendation: {'Proceed to testing' if scores['phase_lock'] >= 80 else 'Optimize parameters'}
            """
            
            st.download_button(
                label="📥 Download Report",
                data=report_text,
                file_name=f"{mol_data['id']}_report.txt",
                mime="text/plain"
            )
        
        if st.button("📊 Export Data (CSV)", use_container_width=True):
            export_df = pd.DataFrame([{
                'molecule_id': mol_data['id'],
                'disease': disease,
                'phase_lock': scores['phase_lock'],
                'membrane': params['membrane'],
                'entropy': params['entropy'],
                'structural': params['structural'],
                'charge': params['charge'],
                'selectivity': params['selectivity'],
                'stability': params['stability'],
                'mw': mol_data['mw'],
                'logP': mol_data['logP'],
                'drug_like': violations == 0
            }])
            
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{mol_data['id']}_data.csv",
                mime="text/csv"
            )
        
        if st.button("🧪 SMILES Export", use_container_width=True):
            smiles_map = {
                'simple': 'C1=CC=C(C=C1)C(=O)N',
                'medium': 'C1=CC2=C(C=C1)N=C(S2)C3=CC=CC=C3N',
                'complex': 'C1=CC=C2C(=C1)C(=CN2)C3=CC=C(C=C3)C(=O)NCC4=CC=CC=C4F',
                'advanced': 'C1=CC=C2C(=C1)C(=C(N2)C3=CC=C(C=C3)Cl)C4=CC=C(C=C4)Br'
            }
            
            smiles_data = f"{mol_data['id']}\t{smiles_map[complexity]}\t{scores['phase_lock']}%\t{disease}"
            
            st.download_button(
                label="📥 Download SMILES",
                data=smiles_data,
                file_name=f"{mol_data['id']}_smiles.smi",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
