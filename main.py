# src/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from src.routers import data_handler, user_auth

app = FastAPI(
    title="CAG Project API - Chat with Your PDF",
    description="API for uploading PDFs, querying content via LLM, and managing data.",
    version="0.1.0",
)

# ===================================================
# CUSTOM OPENAPI SCHEMA WITH SECURITY
# ===================================================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token (Swagger will automatically add 'Bearer' prefix)"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include Routers
app.include_router(
    user_auth.router,
    prefix="/api/v1/auth",
    tags=["User Authentication"]
)

app.include_router(
    data_handler.router,
    prefix="/api/v1",
    tags=["Data Handling and Chat with PDF"]
)

# Root endpoint
@app.get("/", response_class=HTMLResponse, tags=["Root"])
def read_root():
    """
    Simple HTML welcome page with links to Swagger and ReDoc docs.
    """
    html_content = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CAG Project - AI-Powered PDF Chat</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }
        
        /* Animated Background */
        .bg-animation {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: 0;
            overflow: hidden;
        }
        
        .bubble {
            position: absolute;
            bottom: -100px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: rise 15s infinite ease-in;
        }
        
        .bubble:nth-child(1) { width: 80px; height: 80px; left: 10%; animation-delay: 0s; }
        .bubble:nth-child(2) { width: 60px; height: 60px; left: 20%; animation-delay: 2s; }
        .bubble:nth-child(3) { width: 100px; height: 100px; left: 40%; animation-delay: 4s; }
        .bubble:nth-child(4) { width: 70px; height: 70px; left: 60%; animation-delay: 1s; }
        .bubble:nth-child(5) { width: 90px; height: 90px; left: 80%; animation-delay: 3s; }
        
        @keyframes rise {
            0% {
                bottom: -100px;
                transform: translateX(0);
                opacity: 0;
            }
            50% {
                opacity: 1;
            }
            100% {
                bottom: 110vh;
                transform: translateX(100px);
                opacity: 0;
            }
        }
        
        /* Container */
        .container {
            position: relative;
            z-index: 1;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        /* Header */
        .header {
            text-align: center;
            padding: 4rem 2rem 2rem;
            animation: fadeInDown 0.8s ease-out;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .logo {
            font-size: 5rem;
            margin-bottom: 1rem;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        h1 {
            font-size: 3.5rem;
            font-weight: 800;
            color: white;
            margin-bottom: 1rem;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            line-height: 1.2;
        }
        
        .subtitle {
            font-size: 1.4rem;
            color: rgba(255, 255, 255, 0.95);
            font-weight: 300;
            margin-bottom: 3rem;
        }
        
        /* Main Card */
        .main-card {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 3rem;
            box-shadow: 0 30px 90px rgba(0, 0, 0, 0.3);
            animation: fadeInUp 0.8s ease-out 0.2s backwards;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Alert Banner */
        .alert {
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            padding: 1.5rem 2rem;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 1.5rem;
            margin-bottom: 3rem;
            box-shadow: 0 10px 30px rgba(253, 203, 110, 0.4);
            animation: slideInLeft 0.8s ease-out 0.4s backwards;
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .alert-icon {
            font-size: 2.5rem;
            filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
        }
        
        .alert-content h3 {
            font-size: 1.3rem;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }
        
        .alert-content p {
            color: #4a5568;
            line-height: 1.6;
        }
        
        /* Features */
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .feature {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 2px solid transparent;
            animation: fadeInUp 0.8s ease-out backwards;
        }
        
        .feature:nth-child(1) { animation-delay: 0.6s; }
        .feature:nth-child(2) { animation-delay: 0.7s; }
        .feature:nth-child(3) { animation-delay: 0.8s; }
        
        .feature:hover {
            transform: translateY(-15px) scale(1.02);
            border-color: #667eea;
            box-shadow: 0 20px 50px rgba(102, 126, 234, 0.3);
        }
        
        .feature-icon {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            display: inline-block;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .feature h3 {
            font-size: 1.5rem;
            color: #2d3748;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        
        .feature p {
            color: #4a5568;
            line-height: 1.8;
            font-size: 1rem;
        }
        
        /* CTA Buttons */
        .cta-section {
            text-align: center;
            margin: 4rem 0 3rem;
        }
        
        .cta-title {
            font-size: 2rem;
            color: #2d3748;
            margin-bottom: 2rem;
            font-weight: 700;
        }
        
        .cta-buttons {
            display: flex;
            gap: 2rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            padding: 1.5rem 3rem;
            border-radius: 15px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.2rem;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            animation: fadeInUp 0.8s ease-out 0.9s backwards;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        
        .btn-secondary:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(240, 147, 251, 0.5);
        }
        
        .btn-icon {
            font-size: 2rem;
        }
        
        /* Stats */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea10 0%, #764ba220 100%);
            border-radius: 20px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-number {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-label {
            color: #4a5568;
            font-size: 1rem;
            margin-top: 0.5rem;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 3rem 2rem;
            color: white;
            margin-top: 4rem;
        }
        
        .footer-content {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            align-items: center;
        }
        
        .footer-badges {
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .badge {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 0.8rem 1.5rem;
            border-radius: 30px;
            color: white;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
        }
        
        .badge:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-3px);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            h1 {
                font-size: 2.5rem;
            }
            
            .subtitle {
                font-size: 1.1rem;
            }
            
            .main-card {
                padding: 2rem 1.5rem;
            }
            
            .alert {
                flex-direction: column;
                text-align: center;
            }
            
            .features {
                grid-template-columns: 1fr;
            }
            
            .cta-buttons {
                flex-direction: column;
            }
            
            .btn {
                width: 100%;
            }
        }
        
        /* Scroll Animation */
        .scroll-hint {
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 2rem;
            animation: bounce-vertical 2s infinite;
            z-index: 10;
        }
        
        @keyframes bounce-vertical {
            0%, 100% { transform: translateX(-50%) translateY(0); }
            50% { transform: translateX(-50%) translateY(10px); }
        }
    </style>
</head>
<body>
    <!-- Animated Background -->
    <div class="bg-animation">
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
    </div>
    
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="logo">🤖📄</div>
            <h1>CAG Project API</h1>
            <p class="subtitle">AI-Powered PDF Chat & Management System</p>
        </div>
        
        <!-- Main Card -->
        <div class="main-card">
            <!-- Alert -->
            <div class="alert">
                <div class="alert-icon">🔐</div>
                <div class="alert-content">
                    <h3>Authentication Required</h3>
                    <p>Most endpoints require JWT authentication. Please register or login first, then use the <strong>"Authorize"</strong> button in Swagger UI to access protected features.</p>
                </div>
            </div>
            
            <!-- Features -->
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">📤</div>
                    <h3>Smart Upload</h3>
                    <p>Upload PDF documents with automatic text extraction and intelligent processing</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">💬</div>
                    <h3>AI Chat</h3>
                    <p>Ask questions about your PDFs and get instant AI-powered answers</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">🔒</div>
                    <h3>Secure</h3>
                    <p>Enterprise-grade JWT authentication protects your data</p>
                </div>
            </div>
            
            <!-- Stats -->
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">∞</div>
                    <div class="stat-label">PDF Processing</div>
                </div>
                <div class="stat">
                    <div class="stat-number">AI</div>
                    <div class="stat-label">Powered Answers</div>
                </div>
                <div class="stat">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Secure</div>
                </div>
                <div class="stat">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">Available</div>
                </div>
            </div>
            
            <!-- CTA Section -->
            <div class="cta-section">
                <h2 class="cta-title">📚 Explore API Documentation</h2>
                <div class="cta-buttons">
                    <a href="/docs" class="btn btn-primary">
                        <span class="btn-icon">📖</span>
                        <span>Swagger UI</span>
                    </a>
                    <a href="/redoc" class="btn btn-secondary">
                        <span class="btn-icon">📘</span>
                        <span>ReDoc</span>
                    </a>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div class="footer-content">
                <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">CAG Project API v0.1.0</h3>
                <p style="opacity: 0.9; font-size: 1.1rem;">Built with FastAPI • Powered by AI</p>
                <div class="footer-badges">
                    <span class="badge">🔒 Secure</span>
                    <span class="badge">⚡ Fast</span>
                    <span class="badge">🤖 AI-Powered</span>
                    <span class="badge">🚀 Modern</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)