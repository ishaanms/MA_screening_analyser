"""
M&A Strategic Fit Analyzer - Main Streamlit Application
"""

import streamlit as st
import os
from dotenv import load_dotenv
import time

# Import modules
from config.examples import EXAMPLE_DEALS, INDUSTRIES
from agents import DataCollector, GeminiAnalyzer
from utils import (
    create_radar_chart,
    create_gauge_chart,
    create_dimension_bar_chart,
    get_recommendation_color,
    get_recommendation_emoji
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="M&A Strategic Fit Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #008060;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #008060;
    }
    .recommendation-box {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .evidence-item {
        padding: 0.5rem 0;
        border-left: 3px solid #e0e0e0;
        padding-left: 1rem;
        margin: 0.5rem 0;
    }
    .risk-item {
        padding: 0.5rem 0;
        border-left: 3px solid #fac007;
        padding-left: 1rem;
        margin: 0.5rem 0;
        background-color: #fac007;
    }
    .stButton>button {
        background-color: #008060;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #006b4f;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None


def load_example(example_name):
    """Load pre-configured example into form"""
    example = EXAMPLE_DEALS[example_name]
    
    st.session_state.acquirer_name = example['acquirer']['name']
    st.session_state.acquirer_industry = example['acquirer']['industry']
    st.session_state.acquirer_focus = example['acquirer']['focus']
    st.session_state.acquirer_website = example['acquirer']['website']
    
    st.session_state.target_name = example['target']['name']
    st.session_state.target_industry = example['target']['industry']
    st.session_state.target_website = example['target']['website']


def run_analysis(acquirer_name, acquirer_industry, acquirer_focus, acquirer_website,
                target_name, target_industry, target_website, analysis_mode):
    """Run the complete M&A analysis"""
    
    # Progress container
    progress_container = st.empty()
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    try:
        # Step 1: Initialize collectors
        status_text.text("🔧 Initializing analysis engine...")
        progress_bar.progress(10)
        time.sleep(0.5)
        
        collector = DataCollector(mode=analysis_mode)
        analyzer = GeminiAnalyzer()
        
        # Step 2: Collect data
        status_text.text(f"🔍 Scraping company data ({analysis_mode} mode)...")
        progress_bar.progress(30)
        
        collected_data = collector.collect_deal_data(
            acquirer_name=acquirer_name,
            acquirer_website=acquirer_website,
            acquirer_industry=acquirer_industry,
            target_name=target_name,
            target_website=target_website,
            target_industry=target_industry
        )
        
        progress_bar.progress(50)
        time.sleep(0.5)
        
        # Step 3: Analyze with Gemini
        status_text.text("🤖 Running AI strategic analysis...")
        progress_bar.progress(70)
        
        acquirer_data = {
            'name': acquirer_name,
            'industry': acquirer_industry,
            'focus': acquirer_focus,
            'description': collected_data['acquirer'].get('description', '')
        }
        
        target_data = {
            'name': target_name,
            'industry': target_industry,
            'description': collected_data['target'].get('description', '')
        }
        
        analysis = analyzer.analyze_strategic_fit(
            acquirer_data=acquirer_data,
            target_data=target_data,
            collected_data=collected_data
        )
        
        progress_bar.progress(90)
        time.sleep(0.5)
        
        # Step 4: Complete
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(100)
        time.sleep(0.5)
        
        # Clear progress indicators
        progress_container.empty()
        status_text.empty()
        progress_bar.empty()
        
        return {
            'analysis': analysis,
            'collected_data': collected_data,
            'acquirer_data': acquirer_data,
            'target_data': target_data
        }
    
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        st.error("Please check your Gemini API key and try again.")
        return None


def display_results(results):
    """Display analysis results in organized layout"""
    
    analysis = results['analysis']
    acquirer_data = results['acquirer_data']
    target_data = results['target_data']
    
    # Header
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>📊 Analysis Results</h1>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>
            {acquirer_data['name']} → {target_data['name']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab layout
    tab1, tab2, tab3 = st.tabs(["📈 Executive Summary", "🎯 Dimension Breakdown", "📋 Key Insights"])
    
    with tab1:
        display_executive_summary(analysis, acquirer_data, target_data)
    
    with tab2:
        display_dimension_breakdown(analysis)
    
    with tab3:
        display_key_insights(analysis, results['collected_data'])


def display_executive_summary(analysis, acquirer_data, target_data):
    """Display executive summary tab"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Overall score gauge
        st.plotly_chart(
            create_gauge_chart(
                analysis['overall_score'],
                analysis['recommendation']
            ),
            use_container_width=True
        )
        
        # Recommendation box
        rec_color = get_recommendation_color(analysis['recommendation'])
        rec_emoji = get_recommendation_emoji(analysis['recommendation'])
        
        st.markdown(f"""
        <div class='recommendation-box' style='background-color: {rec_color}20; border-left: 4px solid {rec_color};'>
            <div style='color: {rec_color}; font-size: 1.5rem;'>{rec_emoji} {analysis['recommendation']}</div>
            <div style='color: #FFFFFF; margin-top: 0.5rem; font-size: 1rem; font-weight: 400;'>
                {analysis.get('recommendation_detail', 'Strategic fit assessment complete.')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Radar chart
        st.plotly_chart(
            create_radar_chart(analysis['dimensions']),
            use_container_width=True
        )
    
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #666; font-size: 0.9rem;'>Target Company</div>
            <div style='font-size: 1.5rem; font-weight: 700; color: #008060;'>{target_data['name']}</div>
            <div style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>{target_data['industry']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #666; font-size: 0.9rem;'>Acquirer</div>
            <div style='font-size: 1.5rem; font-weight: 700; color: #008060;'>{acquirer_data['name']}</div>
            <div style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>{acquirer_data['industry']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        top_score = max(
            analysis['dimensions'].values(),
            key=lambda x: x.get('score', 0)
        )
        top_dimension = [k for k, v in analysis['dimensions'].items() if v == top_score][0]
        top_dimension_name = top_dimension.replace('_', ' ').title()
        
        st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #666; font-size: 0.9rem;'>Strongest Dimension</div>
            <div style='font-size: 1.5rem; font-weight: 700; color: #008060;'>{top_score['score']}/100</div>
            <div style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>{top_dimension_name}</div>
        </div>
        """, unsafe_allow_html=True)


def display_dimension_breakdown(analysis):
    """Display detailed dimension breakdown"""
    
    st.markdown("### 🎯 Strategic Fit Dimensions")
    
    # Bar chart overview
    st.plotly_chart(
        create_dimension_bar_chart(analysis['dimensions']),
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Detailed breakdowns
    dimension_labels = {
        'technology_synergy': ('💻 Technology Synergy', 'Tech stack compatibility and integration potential'),
        'market_overlap': ('🎯 Market Overlap', 'Customer segments and geographic alignment'),
        'product_complementarity': ('🔧 Product Complementarity', 'Feature gaps and strategic fit'),
        'cultural_alignment': ('🤝 Cultural Alignment', 'Values, mission, and work culture compatibility'),
        'financial_health': ('💰 Financial Health', 'Financial stability and growth trajectory')
    }
    
    for dim_key, (label, description) in dimension_labels.items():
        if dim_key in analysis['dimensions']:
            dim_data = analysis['dimensions'][dim_key]
            
            with st.expander(f"{label} - Score: {dim_data['score']}/100", expanded=False):
                st.markdown(f"*{description}*")
                st.markdown("")
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("**✅ Supporting Evidence:**")
                    for evidence in dim_data.get('evidence', []):
                        st.markdown(f"""
                        <div class='evidence-item'>• {evidence}</div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**⚠️ Key Risks:**")
                    for risk in dim_data.get('risks', []):
                        st.markdown(f"""
                        <div class='risk-item'>• {risk}</div>
                        """, unsafe_allow_html=True)


def display_key_insights(analysis, collected_data):
    """Display key insights and recommendations"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ✨ Top Synergies")
        for i, synergy in enumerate(analysis.get('top_synergies', []), 1):
            st.markdown(f"""
            <div style='padding: 1rem; background-color: #12c947; border-radius: 6px; margin: 0.5rem 0;'>
                <strong>{i}.</strong> {synergy}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ⚠️ Top Risks")
        for i, risk in enumerate(analysis.get('top_risks', []), 1):
            st.markdown(f"""
            <div style='padding: 1rem; background-color: #d92a07; border-radius: 6px; margin: 0.5rem 0;'>
                <strong>{i}.</strong> {risk}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data sources
    st.markdown("### 📚 Data Sources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Acquirer Data:**")
        sources = collected_data['acquirer'].get('data_sources', ['Knowledge base'])
        st.write(", ".join(sources).title())
    
    with col2:
        st.markdown("**Target Data:**")
        sources = collected_data['target'].get('data_sources', ['Knowledge base'])
        st.write(", ".join(sources).title())
    
    # Timestamp
    st.caption(f"Analysis completed: {collected_data.get('timestamp', 'N/A')}")


def main():
    """Main application"""
    
    # Header
    st.markdown("<div class='main-header'>🎯 M&A Strategic Fit Analyzer</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Automated acquisition target assessment powered by AI</div>", unsafe_allow_html=True)
    
    # Show results if analysis is complete
    if st.session_state.analysis_complete and st.session_state.analysis_results:
        display_results(st.session_state.analysis_results)
        
        # Reset button
        if st.button("🔄 Analyze Another Deal", type="primary"):
            st.session_state.analysis_complete = False
            st.session_state.analysis_results = None
            st.rerun()
        
        return
    
    # Pre-configured examples
    st.markdown("### 🚀 Try an Example")
    cols = st.columns(3)
    
    for i, example_name in enumerate(EXAMPLE_DEALS.keys()):
        with cols[i]:
            if st.button(example_name, use_container_width=True):
                load_example(example_name)
                st.rerun()
    
    st.markdown("---")
    
    # Input form
    with st.form("analysis_form"):
        st.markdown("### 🏢 Acquirer Company")
        
        col1, col2 = st.columns(2)
        
        with col1:
            acquirer_name = st.text_input(
                "Company Name *",
                value=st.session_state.get('acquirer_name', ''),
                placeholder="e.g., Shopify"
            )
            acquirer_industry = st.selectbox(
                "Industry *",
                options=INDUSTRIES,
                index=INDUSTRIES.index(st.session_state.get('acquirer_industry', INDUSTRIES[0]))
                if st.session_state.get('acquirer_industry') in INDUSTRIES else 0
            )
        
        with col2:
            acquirer_focus = st.text_input(
                "Strategic Focus *",
                value=st.session_state.get('acquirer_focus', ''),
                placeholder="e.g., Expand fulfillment capabilities"
            )
            acquirer_website = st.text_input(
                "Website (optional)",
                value=st.session_state.get('acquirer_website', ''),
                placeholder="https://www.company.com"
            )
        
        st.markdown("### 🎯 Target Company")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_name = st.text_input(
                "Company Name *",
                value=st.session_state.get('target_name', ''),
                placeholder="e.g., Deliverr"
            )
            target_industry = st.selectbox(
                "Industry *",
                options=INDUSTRIES,
                index=INDUSTRIES.index(st.session_state.get('target_industry', INDUSTRIES[0]))
                if st.session_state.get('target_industry') in INDUSTRIES else 0,
                key="target_industry_select"
            )
        
        with col2:
            target_website = st.text_input(
                "Website (optional)",
                value=st.session_state.get('target_website', ''),
                placeholder="https://www.target.com"
            )
        
        st.markdown("### ⚙️ Analysis Options")
        
        analysis_mode = st.radio(
            "Analysis Mode",
            options=['fast', 'deep'],
            format_func=lambda x: f"{'⚡ Fast Mode (~45 sec)' if x == 'fast' else '🔍 Deep Mode (~2 min)'}",
            horizontal=True
        )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Analyze Strategic Fit", type="primary", use_container_width=True)
        
        if submitted:
            # Validate inputs
            if not acquirer_name or not acquirer_industry or not acquirer_focus or not target_name or not target_industry:
                st.error("❌ Please fill in all required fields (marked with *)")
            else:
                # Run analysis
                results = run_analysis(
                    acquirer_name, acquirer_industry, acquirer_focus, acquirer_website,
                    target_name, target_industry, target_website, analysis_mode
                )
                
                if results:
                    st.session_state.analysis_complete = True
                    st.session_state.analysis_results = results
                    st.rerun()
    
    # Sidebar info
    with st.sidebar:
        st.markdown("### ℹ️ About")
        st.markdown("""
        This tool analyzes strategic fit for M&A transactions across 5 key dimensions:
        
        - 💻 **Technology Synergy**
        - 🎯 **Market Overlap**
        - 🔧 **Product Complementarity**
        - 🤝 **Cultural Alignment**
        - 💰 **Financial Health**
        
        Each dimension is weighted and scored to provide an overall strategic fit assessment.
        """)
        
        st.markdown("---")
        
        st.markdown("### 🔧 Setup")
        api_key_set = bool(os.getenv('GEMINI_API_KEY'))
        
        if api_key_set:
            st.success("✅ Gemini API key configured")
        else:
            st.error("❌ Gemini API key not found")
            st.markdown("Set `GEMINI_API_KEY` in your `.env` file")
        
        st.markdown("---")
        
        st.markdown("### 📊 Analysis Modes")
        st.markdown("""
        **Fast Mode**: Basic website scraping + AI analysis (~45 sec)
        
        **Deep Mode**: Enhanced data collection with news + sentiment (~2 min)
        """)


if __name__ == "__main__":
    main()
