"""
Gemini-powered strategic analysis engine
"""

import google.generativeai as genai
import json
import os
import re
from config.prompts import get_analysis_prompt


class GeminiAnalyzer:
    def __init__(self, api_key=None):
        """
        Initialize Gemini analyzer
        
        Args:
            api_key: Google Gemini API key (or set GEMINI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 2.5 Flash for free tier (fast and efficient)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Generation config for more varied responses
        self.generation_config = {
            "temperature": 1.0,  # Max variance - each analysis should be unique
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 4096,
            "response_mime_type": "application/json", 
        }
    
    def analyze_strategic_fit(self, acquirer_data, target_data, collected_data):
        """
        Analyze strategic fit between acquirer and target
        
        Returns:
            dict: Analysis results with scores and recommendations
        """
        print(f"\n🤖 Running Gemini strategic analysis...")
        print(f"   Acquirer: {acquirer_data['name']} ({acquirer_data['industry']})")
        print(f"   Target: {target_data['name']} ({target_data['industry']})")
        
        # Get industry from acquirer data
        industry = acquirer_data.get('industry', 'SaaS/Enterprise Software')
        
        # Generate prompt
        prompt = get_analysis_prompt(
            acquirer_data=acquirer_data,
            target_data=target_data,
            collected_data=collected_data,
            industry=industry
        )
        
        print(f"   📝 Prompt length: {len(prompt)} characters")
        
        try:
            # Call Gemini API with high temperature for variance
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            print(f"   ✅ Received response from Gemini")
            
            # Extract and parse JSON response
            analysis = self._parse_response(response.text)
            
            # Log key metrics for debugging
            print(f"   📊 Overall Score: {analysis.get('overall_score', 'N/A')}/100")
            print(f"   ✅ Recommendation: {analysis.get('recommendation', 'N/A')}")
            
            # Validate analysis structure
            analysis = self._validate_analysis(analysis)
            
            return analysis
        
        except Exception as e:
            print(f"   ❌ Gemini API error: {str(e)}")
            # Return fallback analysis
            return self._get_fallback_analysis(acquirer_data, target_data)
    
    def _parse_response(self, response_text):
        """Parse JSON from Gemini response"""
        try:
            # Remove markdown code blocks if present
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.startswith('```'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            
            cleaned = cleaned.strip()
            
            # Try to parse JSON
            analysis = json.loads(cleaned)
            
            # Verify it has the expected structure
            if 'dimensions' not in analysis or 'overall_score' not in analysis:
                raise ValueError("Missing required fields in response")
            
            return analysis
        
        except json.JSONDecodeError as e:
            print(f"   ⚠️ JSON parse error: {e}")
            
            # Try more aggressive cleaning
            try:
                # Extract everything between first { and last }
                start = response_text.find('{')
                end = response_text.rfind('}')
                if start != -1 and end != -1:
                    json_str = response_text[start:end+1]
                    
                    # Fix common JSON issues
                    json_str = json_str.replace('\n', ' ')
                    json_str = json_str.replace('\r', ' ')
                    # Remove any trailing commas before closing brackets
                    json_str = re.sub(r',\s*}', '}', json_str)
                    json_str = re.sub(r',\s*]', ']', json_str)
                    
                    analysis = json.loads(json_str)
                    print(f"   ✅ Recovered JSON after cleaning")
                    return analysis
            except Exception as e2:
                print(f"   ❌ Still couldn't parse after cleaning: {e2}")
            
            # If all else fails, try regex extraction
            try:
                # Try to extract overall_score at minimum
                score_match = re.search(r'"overall_score":\s*(\d+\.?\d*)', response_text)
                rec_match = re.search(r'"recommendation":\s*"([^"]+)"', response_text)
                
                if score_match:
                    print(f"   ⚠️ Using regex fallback - extracted score: {score_match.group(1)}")
                    # Return minimal valid structure
                    return {
                        "overall_score": float(score_match.group(1)),
                        "recommendation": rec_match.group(1) if rec_match else "Moderate Fit",
                        "recommendation_detail": "JSON parsing encountered issues. Showing extracted score only.",
                        "dimensions": self._get_default_dimensions(),
                        "top_synergies": ["Analysis incomplete due to parsing error"],
                        "top_risks": ["Full analysis unavailable - retry recommended"]
                    }
            except:
                pass
            
            raise ValueError("Could not parse Gemini response as JSON")
    
    def _get_default_dimensions(self):
        """Return default dimension structure"""
        return {
            "technology_synergy": {
                "score": 65,
                "evidence": ["Parsing error - data unavailable", "Retry analysis", "Check terminal logs"],
                "risks": ["Analysis incomplete", "Manual review needed"]
            },
            "market_overlap": {
                "score": 65,
                "evidence": ["Parsing error - data unavailable", "Retry analysis", "Check terminal logs"],
                "risks": ["Analysis incomplete", "Manual review needed"]
            },
            "product_complementarity": {
                "score": 65,
                "evidence": ["Parsing error - data unavailable", "Retry analysis", "Check terminal logs"],
                "risks": ["Analysis incomplete", "Manual review needed"]
            },
            "cultural_alignment": {
                "score": 65,
                "evidence": ["Parsing error - data unavailable", "Retry analysis", "Check terminal logs"],
                "risks": ["Analysis incomplete", "Manual review needed"]
            },
            "financial_health": {
                "score": 65,
                "evidence": ["Parsing error - data unavailable", "Retry analysis", "Check terminal logs"],
                "risks": ["Analysis incomplete", "Manual review needed"]
            }
        }
    
    def _validate_analysis(self, analysis):
        """Validate and fix analysis structure"""
        # Calculate overall score if missing
        if 'overall_score' not in analysis or analysis['overall_score'] is None:
            dimensions = analysis.get('dimensions', {})
            weights = {
                'technology_synergy': 0.30,
                'market_overlap': 0.25,
                'product_complementarity': 0.20,
                'cultural_alignment': 0.15,
                'financial_health': 0.10
            }
            
            total = 0
            for dim, weight in weights.items():
                score = dimensions.get(dim, {}).get('score', 50)
                total += score * weight
            
            analysis['overall_score'] = round(total, 1)
        
        # Determine recommendation if missing
        if 'recommendation' not in analysis:
            score = analysis['overall_score']
            if score >= 80:
                analysis['recommendation'] = "Strong Fit"
            elif score >= 60:
                analysis['recommendation'] = "Moderate Fit"
            elif score >= 40:
                analysis['recommendation'] = "Weak Fit"
            else:
                analysis['recommendation'] = "Poor Fit"
        
        return analysis
    
    def _get_fallback_analysis(self, acquirer_data, target_data):
        """Return a basic fallback analysis if Gemini fails"""
        return {
            "overall_score": 60,
            "recommendation": "Moderate Fit",
            "recommendation_detail": f"API error occurred. Based on limited analysis, {acquirer_data['name']} acquiring {target_data['name']} shows moderate strategic alignment. Manual review recommended.",
            "dimensions": {
                "technology_synergy": {
                    "score": 65,
                    "evidence": [
                        f"{acquirer_data['name']} likely operates on modern tech infrastructure",
                        f"{target_data['name']} appears to use compatible technology stack",
                        "Integration complexity requires deeper technical assessment"
                    ],
                    "risks": [
                        "Technical due diligence needed to confirm compatibility",
                        "Integration timeline and resource requirements unclear"
                    ]
                },
                "market_overlap": {
                    "score": 60,
                    "evidence": [
                        f"Both companies operate in related {acquirer_data.get('industry', 'technology')} sectors",
                        "Some customer segment overlap likely exists",
                        "Geographic market alignment requires verification"
                    ],
                    "risks": [
                        "Exact customer overlap percentage unknown",
                        "Potential channel conflicts need investigation"
                    ]
                },
                "product_complementarity": {
                    "score": 62,
                    "evidence": [
                        f"{target_data['name']} may fill specific capability gaps",
                        "Cross-selling potential exists but needs quantification",
                        "Product roadmap alignment requires strategic review"
                    ],
                    "risks": [
                        "Product overlap and cannibalization risk unclear",
                        "Go-to-market integration complexity unknown"
                    ]
                },
                "cultural_alignment": {
                    "score": 55,
                    "evidence": [
                        "Both companies appear innovation-focused",
                        "Company size and maturity stage compatibility unclear",
                        "Culture assessment limited without internal access"
                    ],
                    "risks": [
                        "Cultural fit is difficult to assess externally",
                        "Talent retention risk requires HR due diligence"
                    ]
                },
                "financial_health": {
                    "score": 58,
                    "evidence": [
                        f"{target_data['name']} appears to be an active company",
                        "Financial details limited without access to data room",
                        "Growth trajectory requires detailed financial analysis"
                    ],
                    "risks": [
                        "Burn rate and runway unknown without financial statements",
                        "Revenue quality and unit economics need verification"
                    ]
                }
            },
            "top_synergies": [
                f"Potential market expansion in {target_data.get('industry', 'target sector')}",
                f"Technology and capability enhancement for {acquirer_data['name']}",
                "Strategic positioning improvement possible"
            ],
            "top_risks": [
                "Limited public data constrains analysis depth",
                "Integration complexity may exceed initial estimates",
                "Full due diligence required before proceeding"
            ],
            "note": "⚠️ This is a fallback analysis due to API error. Results are generic. Please retry or check API configuration."
        }
