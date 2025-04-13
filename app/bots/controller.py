# 文件: app/bots/gemini_controller.py
from flask_restx import Namespace, Resource, fields
from flask import request

# 导入我们在 service.py 中写好的逻辑
from .service import generate_text, generate_image

api = Namespace("gemini", description="Gemini AI Endpoints")

# 定义一下请求和响应的数据模型(可选)
text_model = api.model("TextRequest", {
    "prompt": fields.String(required=True)
})

image_model = api.model("ImageRequest", {
    "prompt": fields.String(required=True)
})

format = """
Please use this formate to output a Startup Business Plan for user input
here is the format for you to refer

# Cryptocurrency Startup Business Plan

## Executive Summary 
- **Concept Overview**: Brief description of your cryptocurrency, token, or blockchain solution
- **Value Proposition**: The core problem your crypto solution solves in the market
- **Target Market**: Specific blockchain/crypto users, industries, or applications you'll serve
- **Technology Foundation**: Brief overview of the blockchain platform or protocol you'll use
- **Token Economics**: Summary of your token model, utility, and distribution strategy
- **Financial Projections**: Key metrics including token valuation forecasts
- **Funding Requirements**: Seed funding, ICO/IEO/STO plans, or venture capital needs

## Market Analysis
- **Crypto Market Overview**: Current blockchain/cryptocurrency landscape and trends
- **Target User Segmentation**: Detailed analysis of your specific user groups
- **Market Size & Opportunity**: TAM, SAM, and SOM calculations for your solution
- **Competitive Analysis**: Direct and indirect competitors in the crypto space
- **Regulatory Environment**: Analysis of relevant cryptocurrency regulations in target markets

## Product/Technology
- **Blockchain Architecture**: Technical specifications of your blockchain solution
- **Consensus Mechanism**: Proof of Work, Proof of Stake, or other consensus approaches
- **Smart Contract Functionality**: Details on the programmable aspects of your platform
- **Security Framework**: Approach to security, including audit plans and bug bounty programs
- **Scalability Solutions**: How your technology will handle growth and transaction volume
- **Technical Roadmap**: Timeline for development milestones and protocol upgrades

## Token Economics
- **Token Utility & Function**: How your token will be used within your ecosystem
- **Token Distribution**: Allocation among team, investors, community, and development
- **Tokenomics Model**: Inflation/deflation mechanisms, staking, governance rights
- **Token Sale Structure**: Details on pre-sale, public sale, vesting periods
- **Treasury Management**: Plans for managing project funds and treasury reserves

## Go-to-Market Strategy
- **Launch Strategy**: Phased approach from testnet to mainnet release
- **Community Building**: Plans for growing and engaging your early adopter community
- **Exchange Listings**: Strategy for liquidity and trading pair development
- **Partnership Development**: Key industry relationships and integration opportunities
- **Marketing & PR**: Approach to building awareness in the crypto community

## Team & Governance
- **Founding Team**: Technical and business expertise of core team members
- **Advisors**: Industry experts supporting the project
- **Governance Model**: On-chain or off-chain decision-making processes
- **DAO Structure**: If applicable, how community governance will function
- **Organizational Structure**: Legal entities, foundation model, or decentralized org

## Financial Projections
- **Development Costs**: Technical infrastructure and team expenses
- **Revenue Model**: Transaction fees, token appreciation, services, or other sources
- **Liquidity Planning**: Ensuring sufficient trading volume and market depth
- **Burn Rate & Runway**: Monthly expenses and funding requirements
- **Exit Strategies**: Potential acquisition targets or long-term sustainability plans

## Risk Analysis
- **Technical Risks**: Potential vulnerabilities, scalability issues, or development challenges
- **Market Risks**: Competition, adoption barriers, or market volatility
- **Regulatory Risks**: Potential legal challenges or compliance requirements
- **Security Risks**: Attack vectors, exploits, or security concerns
- **Mitigation Strategies**: How you plan to address each major risk category

## Legal & Compliance
- **Regulatory Framework**: Compliance approach for relevant jurisdictions
- **KYC/AML Policies**: How you'll handle identity verification if required
- **Securities Considerations**: Analysis of token classification under securities laws
- **Privacy Compliance**: Approach to data protection regulations
- **Intellectual Property**: Patents, trademarks, or open-source licensing strategy

## Implementation Timeline
- **Development Phases**: Key technical milestones from concept to launch
- **Funding Stages**: Capital raising timeline aligned with development needs
- **Community Growth**: User acquisition targets and community building goals
- **Network Effects**: How you'll achieve critical mass for your platform
- **Long-term Vision**: 3-5 year outlook for your crypto project
"""

@api.route("/text")
class GeminiTextResource(Resource):
    @api.expect(text_model)
    def post(self):
        """
        POST /api/gemini/text
        传入 prompt，返回 Gemini 生成的文本
        """
        data = request.json
        prompt = data.get("prompt", "")
        if not prompt:
            return {"error": "No prompt provided."}, 400


        modified_prompt = f"{format},\n\n User Input here: \n{prompt}"
        
        # 调用 service
        response_text = generate_text(modified_prompt)
        return {"response": response_text}, 200


@api.route("/image")
class GeminiImageResource(Resource):
    @api.expect(image_model)
    def post(self):
        """
        POST /api/gemini/image
        传入 prompt，返回生成图像文件路径
        """
        data = request.json
        prompt = data.get("prompt", "")
        if not prompt:
            return {"error": "No prompt provided."}, 400

        # 调用 service
        file_path = generate_image(prompt)
        return {"image_path": file_path}, 200
