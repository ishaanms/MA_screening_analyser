"""
Pre-configured M&A deal examples for quick testing
"""

EXAMPLE_DEALS = {
    "Shopify → Deliverr": {
        "acquirer": {
            "name": "Shopify",
            "industry": "E-commerce/Retail",
            "focus": "Enhance merchant fulfillment capabilities and compete with Amazon FBA",
            "website": "https://www.shopify.com"
        },
        "target": {
            "name": "Deliverr",
            "industry": "E-commerce/Retail",
            "website": "https://www.deliverr.com"
        }
    },
    "Stripe → Plaid": {
        "acquirer": {
            "name": "Stripe",
            "industry": "FinTech/Payments",
            "focus": "Expand banking infrastructure and account-to-account payment capabilities",
            "website": "https://www.stripe.com"
        },
        "target": {
            "name": "Plaid",
            "industry": "FinTech/Payments",
            "website": "https://www.plaid.com"
        }
    },
    "Salesforce → Slack": {
        "acquirer": {
            "name": "Salesforce",
            "industry": "SaaS/Enterprise Software",
            "focus": "Build integrated communication layer for Customer 360 platform",
            "website": "https://www.salesforce.com"
        },
        "target": {
            "name": "Slack",
            "industry": "SaaS/Enterprise Software",
            "website": "https://www.slack.com"
        }
    }
}

INDUSTRIES = [
    "E-commerce/Retail",
    "FinTech/Payments",
    "SaaS/Enterprise Software"
]
