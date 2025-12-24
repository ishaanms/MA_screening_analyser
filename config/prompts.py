"""
Gemini API prompt templates for M&A strategic analysis
"""

def get_company_context(company_name):
    """
    Get known context about well-known companies to improve analysis specificity
    """
    company_info = {
        "Shopify": "Leading e-commerce platform for online stores, serves 2M+ merchants, GMV $200B+, competes with Amazon/BigCommerce",
        "Deliverr": "Fast fulfillment platform for e-commerce, 2-day delivery network, serves D2C brands, acquired by Shopify 2022 for $2.1B",
        "Stripe": "Payment infrastructure company, processes $640B+ annually, serves millions of businesses, API-first approach",
        "Plaid": "Banking infrastructure, connects 11K+ financial institutions, enables account linking, used by Venmo/Robinhood",
        "Salesforce": "CRM leader, $30B+ revenue, serves 150K+ customers, Customer 360 platform, cloud-based enterprise software",
        "Slack": "Team collaboration platform, 10M+ daily active users, messaging + channels, acquired by Salesforce 2021 for $27.7B",
        "Microsoft": "Tech giant, cloud (Azure), productivity (Office 365), gaming (Xbox), enterprise software, $200B+ revenue",
        "GitHub": "Developer platform, 100M+ developers, code hosting, CI/CD, acquired by Microsoft 2018 for $7.5B",
        "Adobe": "Creative software leader, Photoshop/Illustrator, $20B revenue, design tools, creative cloud",
        "Figma": "Collaborative design platform, web-based, 4M users, competes with Adobe XD, acquisition blocked by regulators",
    }
    
    return company_info.get(company_name, f"Research {company_name} and use your knowledge of this company")


def get_analysis_prompt(acquirer_data, target_data, collected_data, industry):
    """
    Generate dynamic prompt based on acquirer and target context
    """
    
    industry_context = {
        "E-commerce/Retail": """
        Key considerations for e-commerce M&A:
        - Customer data integration and privacy compliance
        - Omnichannel fulfillment and logistics synergies
        - Supply chain optimization potential
        - Payment processing and checkout flow compatibility
        - Merchant/seller platform integration
        """,
        
        "FinTech/Payments": """
        Key considerations for fintech M&A:
        - Regulatory compliance alignment (PCI-DSS, banking regulations)
        - Payment infrastructure and API compatibility
        - Security standards and fraud prevention capabilities
        - Banking partnership overlap and relationships
        - Risk management and compliance frameworks
        """,
        
        "SaaS/Enterprise Software": """
        Key considerations for SaaS M&A:
        - API integration feasibility and architecture compatibility
        - Customer overlap and cross-sell/upsell opportunities
        - Cloud infrastructure and scalability alignment
        - Sales channel and go-to-market synergies
        - Data migration and system integration complexity
        """
    }
    
    context = industry_context.get(industry, industry_context["SaaS/Enterprise Software"])
    
    # Get company-specific context
    acquirer_context = get_company_context(acquirer_data['name'])
    target_context = get_company_context(target_data['name'])
    
    prompt = f"""You are a senior M&A strategy consultant at McKinsey analyzing a potential acquisition.

⚠️ CRITICAL INSTRUCTIONS:
1. Provide HIGHLY SPECIFIC analysis based on these EXACT companies
2. DO NOT give generic analysis - reference actual products, markets, customers, and competitors
3. Scores MUST vary based on actual fit - bad fits = 20-45, medium fits = 50-70, great fits = 75-95
4. If industries don't align well (e.g., Microsoft buying an e-commerce logistics company), scores should be LOW
5. Each piece of evidence must mention specific company details, not generic statements

ACQUIRER PROFILE:
Company: {acquirer_data['name']}
Industry: {acquirer_data['industry']}
Strategic Focus: {acquirer_data.get('focus', 'Strategic expansion')}
What they're known for: {acquirer_context}
Additional context: {acquirer_data.get('description', 'N/A')}

TARGET COMPANY:
Company: {target_data['name']}
Industry: {target_data['industry']}
What they're known for: {target_context}
Additional context: {target_data.get('description', 'N/A')}

COLLECTED DATA:
{format_collected_data(collected_data)}

INDUSTRY-SPECIFIC CONSIDERATIONS:
{context}

SCORING GUIDELINES (FOLLOW THESE STRICTLY):
- 85-100: Near-perfect alignment (same industry, complementary products, obvious synergies)
  Example: Shopify + Deliverr (e-commerce + fulfillment)
  
- 70-84: Strong fit with some gaps (related industries, clear value)
  Example: Salesforce + Slack (CRM + collaboration)
  
- 55-69: Moderate fit (some synergies, notable integration challenges)
  Example: Adobe + Figma (creative software but overlapping products)
  
- 40-54: Weak fit (limited synergies, significant challenges)
  Example: Microsoft + Deliverr (tech giant + e-commerce logistics)
  
- 0-39: Poor fit (misaligned industries, minimal strategic value)
  Example: Stripe + Slack (payments + collaboration - totally different)

ANALYSIS TASK:
Evaluate the acquisition of {target_data['name']} by {acquirer_data['name']}.

For EACH of the 5 dimensions below:
1. Score (0-100): Use the guidelines above. Think: "Does this make strategic sense?"
2. Evidence (3 points): MUST reference specific products, customers, markets, or capabilities
3. Risks (2 points): MUST reference actual business challenges, not generic statements

DIMENSIONS TO ANALYZE:

1. TECHNOLOGY SYNERGY (30% weight)
   - How do {acquirer_data['name']}'s tech stack and {target_data['name']}'s platform integrate?
   - Specific APIs, infrastructure, technical architectures to consider
   - Integration complexity and technical debt

2. MARKET OVERLAP (25% weight)
   - Do {acquirer_data['name']} and {target_data['name']} serve the same customers?
   - Geographic presence alignment
   - Go-to-market channel compatibility

3. PRODUCT COMPLEMENTARITY (20% weight)
   - Does {target_data['name']} fill a specific gap in {acquirer_data['name']}'s product suite?
   - Cross-selling and bundling opportunities
   - Competitive positioning improvement

4. CULTURAL ALIGNMENT (15% weight)
   - Company size and growth stage compatibility
   - Work culture and values (based on public info)
   - Talent retention and integration risk

5. FINANCIAL HEALTH (10% weight)
   - {target_data['name']}'s growth trajectory and business model
   - Revenue quality and sustainability
   - Profitability path and burn rate

OUTPUT FORMAT (respond ONLY with valid JSON, no markdown):
{{
    "overall_score": <weighted average of all dimensions>,
    "recommendation": "<Strong Fit|Moderate Fit|Weak Fit|Poor Fit>",
    "recommendation_detail": "<2-3 specific sentences explaining why, mentioning both company names>",
    "dimensions": {{
        "technology_synergy": {{
            "score": <0-100, be realistic>,
            "evidence": [
                "Specific point mentioning {acquirer_data['name']} or {target_data['name']} tech",
                "Another specific point with actual product/platform names",
                "Third specific point with technical details"
            ],
            "risks": [
                "Specific integration risk mentioning actual systems",
                "Another specific technical challenge"
            ]
        }},
        "market_overlap": {{
            "score": <0-100>,
            "evidence": [
                "Specific customer segment both companies serve",
                "Specific geographic market detail",
                "Specific go-to-market channel fact"
            ],
            "risks": [
                "Specific market challenge for this acquisition",
                "Another specific market risk"
            ]
        }},
        "product_complementarity": {{
            "score": <0-100>,
            "evidence": [
                "Specific product or feature {target_data['name']} adds to {acquirer_data['name']}",
                "Specific cross-sell opportunity with product names",
                "Specific competitive advantage gained"
            ],
            "risks": [
                "Specific product overlap or cannibalization risk",
                "Specific product integration challenge"
            ]
        }},
        "cultural_alignment": {{
            "score": <0-100>,
            "evidence": [
                "Specific culture aspect of both companies",
                "Specific company size or growth stage fact",
                "Specific work style or values alignment"
            ],
            "risks": [
                "Specific cultural integration challenge",
                "Specific talent retention risk"
            ]
        }},
        "financial_health": {{
            "score": <0-100>,
            "evidence": [
                "Specific revenue or growth metric of {target_data['name']}",
                "Specific business model strength",
                "Specific financial milestone or trajectory"
            ],
            "risks": [
                "Specific financial concern or burn rate issue",
                "Specific profitability challenge"
            ]
        }}
    }},
    "top_synergies": [
        "Specific synergy #1 mentioning actual capabilities/products",
        "Specific synergy #2 with company names",
        "Specific synergy #3 with business impact"
    ],
    "top_risks": [
        "Specific risk #1 with actual business challenges",
        "Specific risk #2 mentioning integration details",
        "Specific risk #3 with strategic concern"
    ]
}}

REMEMBER: 
- Be brutally honest about fit quality
- Microsoft buying Deliverr? That's a 45/100 (weak fit)
- Shopify buying Deliverr? That's an 85/100 (strong fit)
- Every evidence point must be SPECIFIC to these companies"""

    return prompt


def format_collected_data(data):
    """Format collected data for prompt injection"""
    formatted = []
    
    if data.get('acquirer'):
        acq = data['acquirer']
        formatted.append(f"Acquirer Details:")
        if acq.get('description'):
            formatted.append(f"  Description: {acq['description']}")
        if acq.get('founded'):
            formatted.append(f"  Founded: {acq['founded']}")
        if acq.get('employees'):
            formatted.append(f"  Employees: {acq['employees']}")
    
    if data.get('target'):
        tgt = data['target']
        formatted.append(f"\nTarget Details:")
        if tgt.get('description'):
            formatted.append(f"  Description: {tgt['description']}")
        if tgt.get('founded'):
            formatted.append(f"  Founded: {tgt['founded']}")
        if tgt.get('employees'):
            formatted.append(f"  Employees: {tgt['employees']}")
    
    return "\n".join(formatted) if formatted else "Limited data collected - use your knowledge of these companies."
