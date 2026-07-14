from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HumanSafe - Protecting Lives Every Second</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --red: #E63946;
            --red-dark: #C1121F;
            --blue: #1D3557;
            --blue-light: #457B9D;
            --blue-sky: #A8DADC;
            --white: #F1FAEE;
            --pure-white: #FFFFFF;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: var(--white);
            color: #333;
            overflow-x: hidden;
        }

        /* Animated Background Particles */
        .particles {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            border-radius: 50%;
            animation: floatParticle linear infinite;
            opacity: 0.15;
        }

        @keyframes floatParticle {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 0.15; }
            90% { opacity: 0.15; }
            100% { transform: translateY(-100px) rotate(720deg); opacity: 0; }
        }

        /* Navbar */
        nav {
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1000;
            background: rgba(29, 53, 87, 0.95);
            backdrop-filter: blur(20px);
            padding: 15px 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 30px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }

        nav.scrolled {
            padding: 10px 5%;
            background: rgba(29, 53, 87, 0.98);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }

        .logo-icon {
            width: 45px; height: 45px;
            background: linear-gradient(135deg, var(--red), #FF6B6B);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            color: white;
            animation: pulse 2s infinite;
            box-shadow: 0 4px 15px rgba(230, 57, 70, 0.4);
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .logo-text {
            font-size: 24px;
            font-weight: 800;
            color: white;
            letter-spacing: 1px;
        }

        .logo-text span { color: var(--red); }

        .nav-links {
            display: flex;
            gap: 30px;
            list-style: none;
        }

        .nav-links a {
            color: var(--blue-sky);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            padding: 5px 0;
        }

        .nav-links a::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0;
            width: 0; height: 2px;
            background: var(--red);
            transition: width 0.3s ease;
        }

        .nav-links a:hover { color: white; }
        .nav-links a:hover::after { width: 100%; }

        .sos-btn {
            background: linear-gradient(135deg, var(--red), var(--red-dark));
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            animation: sosPulse 1.5s infinite;
            box-shadow: 0 4px 20px rgba(230, 57, 70, 0.5);
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        @keyframes sosPulse {
            0%, 100% { box-shadow: 0 4px 20px rgba(230, 57, 70, 0.5); }
            50% { box-shadow: 0 4px 40px rgba(230, 57, 70, 0.8), 0 0 60px rgba(230, 57, 70, 0.3); }
        }

        .sos-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(230, 57, 70, 0.7);
        }

        /* Hero Section */
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            background: linear-gradient(135deg, var(--blue) 0%, #0D1B2A 50%, var(--blue-dark) 100%);
            overflow: hidden;
            padding: 100px 5% 50px;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle at 30% 50%, rgba(230, 57, 70, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 70% 50%, rgba(168, 218, 220, 0.08) 0%, transparent 50%);
            animation: heroRotate 20s linear infinite;
        }

        @keyframes heroRotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .hero-content {
            position: relative;
            z-index: 2;
            text-align: center;
            max-width: 900px;
        }

        .hero-badge {
            display: inline-block;
            background: rgba(230, 57, 70, 0.2);
            border: 1px solid rgba(230, 57, 70, 0.4);
            color: #FF6B6B;
            padding: 8px 25px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 25px;
            animation: fadeInDown 1s ease;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .hero h1 {
            font-size: clamp(40px, 6vw, 72px);
            font-weight: 800;
            color: white;
            line-height: 1.1;
            margin-bottom: 20px;
            animation: fadeInUp 1s ease 0.2s both;
        }

        .hero h1 .highlight {
            background: linear-gradient(135deg, var(--red), #FF6B6B, #FF8E8E);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
        }

        .hero h1 .highlight-blue {
            background: linear-gradient(135deg, var(--blue-sky), #B8E8EC);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero p {
            font-size: 20px;
            color: var(--blue-sky);
            max-width: 650px;
            margin: 0 auto 40px;
            line-height: 1.7;
            animation: fadeInUp 1s ease 0.4s both;
        }

        .hero-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            animation: fadeInUp 1s ease 0.6s both;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--red), var(--red-dark));
            color: white;
            border: none;
            padding: 16px 40px;
            border-radius: 50px;
            font-size: 17px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 4px 25px rgba(230, 57, 70, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 35px rgba(230, 57, 70, 0.6);
        }

        .btn-secondary {
            background: transparent;
            color: white;
            border: 2px solid var(--blue-sky);
            padding: 14px 40px;
            border-radius: 50px;
            font-size: 17px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .btn-secondary:hover {
            background: var(--blue-sky);
            color: var(--blue);
            transform: translateY(-3px);
        }

        .hero-stats {
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-top: 60px;
            animation: fadeInUp 1s ease 0.8s both;
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            font-size: 42px;
            font-weight: 800;
            color: white;
            display: block;
        }

        .stat-label {
            color: var(--blue-sky);
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Floating Elements */
        .floating-shapes {
            position: absolute;
            width: 100%; height: 100%;
            top: 0; left: 0;
            pointer-events: none;
        }

        .shape {
            position: absolute;
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }

        .shape-1 { width: 80px; height: 80px; background: rgba(230, 57, 70, 0.1); top: 20%; left: 10%; animation-delay: 0s; }
        .shape-2 { width: 120px; height: 120px; background: rgba(168, 218, 220, 0.08); top: 60%; right: 10%; animation-delay: 2s; }
        .shape-3 { width: 60px; height: 60px; background: rgba(230, 57, 70, 0.08); bottom: 20%; left: 20%; animation-delay: 4s; }
        .shape-4 { width: 100px; height: 100px; background: rgba(69, 123, 157, 0.1); top: 30%; right: 20%; animation-delay: 1s; border-radius: 30%; }

        @keyframes float {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(10deg); }
        }

        /* Section Styles */
        section {
            padding: 100px 5%;
            position: relative;
        }

        .section-header {
            text-align: center;
            margin-bottom: 70px;
        }

        .section-badge {
            display: inline-block;
            background: rgba(230, 57, 70, 0.1);
            color: var(--red);
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .section-header h2 {
            font-size: 42px;
            font-weight: 800;
            color: var(--blue);
            margin-bottom: 15px;
        }

        .section-header p {
            color: #666;
            font-size: 18px;
            max-width: 600px;
            margin: 0 auto;
        }

        /* Features Section */
        .features {
            background: var(--pure-white);
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .feature-card {
            background: white;
            border-radius: 20px;
            padding: 40px 30px;
            text-align: center;
            transition: all 0.4s ease;
            border: 1px solid #f0f0f0;
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--red), var(--blue-light));
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }

        .feature-card:hover::before { transform: scaleX(1); }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(29, 53, 87, 0.15);
        }

        .feature-icon {
            width: 80px; height: 80px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 25px;
            font-size: 36px;
            transition: all 0.4s ease;
        }

        .feature-card:hover .feature-icon { transform: scale(1.1) rotate(5deg); }

        .icon-red { background: linear-gradient(135deg, rgba(230, 57, 70, 0.1), rgba(230, 57, 70, 0.05)); color: var(--red); }
        .icon-blue { background: linear-gradient(135deg, rgba(29, 53, 87, 0.1), rgba(29, 53, 87, 0.05)); color: var(--blue); }
        .icon-sky { background: linear-gradient(135deg, rgba(69, 123, 157, 0.1), rgba(69, 123, 157, 0.05)); color: var(--blue-light); }

        .feature-card h3 {
            font-size: 22px;
            font-weight: 700;
            color: var(--blue);
            margin-bottom: 12px;
        }

        .feature-card p {
            color: #666;
            line-height: 1.7;
            font-size: 15px;
        }

        /* How It Works */
        .how-it-works {
            background: linear-gradient(135deg, var(--blue) 0%, #0D1B2A 100%);
            color: white;
        }

        .how-it-works .section-header h2 { color: white; }
        .how-it-works .section-header p { color: var(--blue-sky); }

        .steps {
            display: flex;
            justify-content: center;
            gap: 40px;
            max-width: 1100px;
            margin: 0 auto;
            flex-wrap: wrap;
        }

        .step {
            text-align: center;
            flex: 1;
            min-width: 250px;
            position: relative;
        }

        .step-number {
            width: 70px; height: 70px;
            background: linear-gradient(135deg, var(--red), var(--red-dark));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 800;
            margin: 0 auto 25px;
            box-shadow: 0 8px 30px rgba(230, 57, 70, 0.4);
            position: relative;
        }

        .step-number::after {
            content: '';
            position: absolute;
            width: 90px; height: 90px;
            border: 2px solid rgba(230, 57, 70, 0.3);
            border-radius: 50%;
            animation: stepPulse 2s infinite;
        }

        @keyframes stepPulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0; }
        }

        .step h3 { font-size: 20px; margin-bottom: 10px; color: white; }
        .step p { color: var(--blue-sky); font-size: 15px; line-height: 1.6; }

        /* Emergency Services */
        .emergency-services {
            background: white;
        }

        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 25px;
            max-width: 1100px;
            margin: 0 auto;
        }

        .service-card {
            background: linear-gradient(135deg, var(--white), var(--pure-white));
            border-radius: 16px;
            padding: 30px;
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            cursor: pointer;
        }

        .service-card:hover {
            border-color: var(--red);
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(230, 57, 70, 0.15);
        }

        .service-icon {
            font-size: 48px;
            margin-bottom: 15px;
            display: block;
        }

        .service-card h4 { color: var(--blue); font-size: 18px; margin-bottom: 8px; }
        .service-card p { color: #777; font-size: 14px; }

        /* Testimonials */
        .testimonials {
            background: var(--white);
        }

        .testimonials-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
            max-width: 1100px;
            margin: 0 auto;
        }

        .testimonial-card {
            background: white;
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.05);
            position: relative;
        }

        .testimonial-card::before {
            content: '\\201C';
            font-size: 80px;
            color: rgba(230, 57, 70, 0.1);
            position: absolute;
            top: 10px; left: 25px;
            font-family: serif;
        }

        .testimonial-text {
            font-size: 16px;
            line-height: 1.8;
            color: #555;
            margin-bottom: 25px;
            position: relative;
            z-index: 1;
        }

        .testimonial-author {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .author-avatar {
            width: 50px; height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--blue-light), var(--blue));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 18px;
        }

        .author-info h5 { color: var(--blue); font-size: 16px; }
        .author-info span { color: #999; font-size: 13px; }

        /* Download CTA */
        .download-cta {
            background: linear-gradient(135deg, var(--red), var(--red-dark));
            text-align: center;
            color: white;
            position: relative;
            overflow: hidden;
        }

        .download-cta::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
            animation: ctaRotate 15s linear infinite;
        }

        @keyframes ctaRotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .download-cta h2 {
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 15px;
            position: relative;
        }

        .download-cta p {
            font-size: 18px;
            opacity: 0.9;
            margin-bottom: 35px;
            position: relative;
        }

        .download-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            position: relative;
            flex-wrap: wrap;
        }

        .download-btn {
            background: white;
            color: var(--red);
            border: none;
            padding: 16px 35px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }

        .download-btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        }

        /* Footer */
        footer {
            background: #0D1B2A;
            color: white;
            padding: 70px 5% 30px;
        }

        .footer-grid {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 40px;
            max-width: 1200px;
            margin: 0 auto;
            margin-bottom: 50px;
        }

        .footer-brand .logo-text { font-size: 28px; }
        .footer-brand p { color: var(--blue-sky); margin-top: 15px; line-height: 1.7; font-size: 14px; }

        .footer-col h4 {
            font-size: 16px;
            margin-bottom: 20px;
            color: white;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .footer-col a {
            display: block;
            color: var(--blue-sky);
            text-decoration: none;
            margin-bottom: 12px;
            font-size: 14px;
            transition: color 0.3s;
        }

        .footer-col a:hover { color: var(--red); }

        .social-links {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }

        .social-links a {
            width: 40px; height: 40px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
            transition: all 0.3s;
            margin-bottom: 0;
        }

        .social-links a:hover { background: var(--red); transform: translateY(-3px); }

        .footer-bottom {
            text-align: center;
            padding-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: var(--blue-sky);
            font-size: 14px;
        }

        /* Scroll Animations */
        .reveal {
            opacity: 0;
            transform: translateY(40px);
            transition: all 0.8s ease;
        }

        .reveal.active {
            opacity: 1;
            transform: translateY(0);
        }

        /* SOS Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 2000;
            justify-content: center;
            align-items: center;
        }

        .modal-overlay.active { display: flex; }

        .modal {
            background: white;
            border-radius: 24px;
            padding: 50px;
            text-align: center;
            max-width: 450px;
            width: 90%;
            animation: modalPop 0.4s ease;
            position: relative;
        }

        @keyframes modalPop {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        .modal-icon {
            width: 100px; height: 100px;
            background: linear-gradient(135deg, var(--red), var(--red-dark));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            color: white;
            margin: 0 auto 25px;
            animation: shake 0.5s infinite;
        }

        @keyframes shake {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-5deg); }
            75% { transform: rotate(5deg); }
        }

        .modal h2 { color: var(--red); font-size: 28px; margin-bottom: 10px; }
        .modal p { color: #666; margin-bottom: 25px; }

        .emergency-numbers {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 25px;
        }

        .emergency-number {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--white);
            padding: 15px 20px;
            border-radius: 12px;
            transition: all 0.3s;
        }

        .emergency-number:hover { background: rgba(230, 57, 70, 0.1); }

        .emergency-number span { font-weight: 600; color: var(--blue); }

        .emergency-number a {
            background: var(--red);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s;
        }

        .emergency-number a:hover { background: var(--red-dark); }

        .close-modal {
            background: var(--blue);
            color: white;
            border: none;
            padding: 12px 35px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .close-modal:hover { background: var(--blue-light); }

        /* Responsive */
        @media (max-width: 768px) {
            .nav-links { display: none; }
            .hero-stats { gap: 30px; }
            .stat-number { font-size: 30px; }
            .footer-grid { grid-template-columns: 1fr; }
            .hero-buttons { flex-direction: column; align-items: center; }
        }

        /* Mobile Menu */
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
        }

        @media (max-width: 768px) {
            .mobile-menu-btn { display: block; }
        }

        /* Counter Animation */
        .counter { display: inline-block; }
    </style>
</head>
<body>

    <!-- Particles Background -->
    <div class="particles" id="particles"></div>

    <!-- Navigation -->
    <nav id="navbar">
        <a href="#" class="logo">
            <div class="logo-icon"><i class="fas fa-shield-alt"></i></div>
            <div class="logo-text">Human<span>Safe</span></div>
        </a>
        <ul class="nav-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#how-it-works">How It Works</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#testimonials">Stories</a></li>
        </ul>
        <button class="sos-btn" onclick="openSOSModal()">
            <i class="fas fa-exclamation-triangle"></i> SOS
        </button>
        <button class="mobile-menu-btn"><i class="fas fa-bars"></i></button>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="floating-shapes">
            <div class="shape shape-1"></div>
            <div class="shape shape-2"></div>
            <div class="shape shape-3"></div>
            <div class="shape shape-4"></div>
        </div>
        <div class="hero-content">
            <div class="hero-badge"><i class="fas fa-shield-alt"></i> Your Safety, Our Priority</div>
            <h1>Protecting <span class="highlight">Lives</span> Every <span class="highlight-blue">Second</span></h1>
            <p>HumanSafe is your intelligent safety companion. Instant SOS alerts, real-time location sharing, medical emergency support, and 24/7 protection for you and your loved ones.</p>
            <div class="hero-buttons">
                <button class="btn-primary" onclick="openSOSModal()">
                    <i class="fas fa-bell"></i> Activate SOS
                </button>
                <button class="btn-secondary">
                    <i class="fas fa-play-circle"></i> Watch Demo
                </button>
            </div>
            <div class="hero-stats">
                <div class="stat">
                    <span class="stat-number"><span class="counter" data-target="500000">0</span>+</span>
                    <span class="stat-label">Lives Protected</span>
                </div>
                <div class="stat">
                    <span class="stat-number"><span class="counter" data-target="150">0</span>+</span>
                    <span class="stat-label">Countries</span>
                </div>
                <div class="stat">
                    <span class="stat-number"><span class="counter" data-target="3">0</span>s</span>
                    <span class="stat-label">Response Time</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="features" id="features">
        <div class="section-header reveal">
            <span class="section-badge"><i class="fas fa-star"></i> Features</span>
            <h2>Everything You Need to Stay Safe</h2>
            <p>Powerful features designed to protect you in any emergency situation</p>
        </div>
        <div class="features-grid">
            <div class="feature-card reveal">
                <div class="feature-icon icon-red"><i class="fas fa-bell"></i></div>
                <h3>One-Touch SOS</h3>
                <p>Trigger instant emergency alerts with a single tap. Notify your emergency contacts and authorities within seconds.</p>
            </div>
            <div class="feature-card reveal">
                <div class="feature-icon icon-blue"><i class="fas fa-map-marker-alt"></i></div>
                <h3>Live Location Tracking</h3>
                <p>Share your real-time location with trusted contacts. Always know where your loved ones are for complete peace of mind.</p>
            </div>
            <div class="feature-card reveal">
                <div class="feature-icon icon-sky"><i class="fas fa-heartbeat"></i></div>
                <h3>Medical Emergency</h3>
                <p>Access immediate medical guidance and connect with healthcare professionals during emergencies.</p>
            </div>
            <div class="feature-card reveal">
                <div class="feature-icon icon-red"><i class="fas fa-user-shield"></i></div>
                <h3>Safety Zones</h3>
                <p>Set up geofenced safe zones. Get alerts when loved ones enter or leave designated areas.</p>
            </div>
            <div class="feature-card reveal">
                <div class="feature-icon icon-blue"><i class="fas fa-phone-alt"></i></div>
                <h3>Emergency Contacts</h3>
                <p>Quick access to all your emergency contacts. Pre-configured speed dial for instant connection.</p>
            </div>
            <div class="feature-card reveal">
                <div class="feature-icon icon-sky"><i class="fas fa-video"></i></div>
                <h3>Video Verification</h3>
                <p>Send live video feeds to emergency contacts for real-time situation assessment.</p>
            </div>
        </div>
    </section>

    <!-- How It Works -->
    <section class="how-it-works" id="how-it-works">
        <div class="section-header reveal">
            <span class="section-badge" style="background: rgba(230,57,70,0.2); color: #FF6B6B;"><i class="fas fa-cog"></i> How It Works</span>
            <h2>Stay Safe in 3 Simple Steps</h2>
            <p>Getting protected with HumanSafe takes less than a minute</p>
        </div>
        <div class="steps">
            <div class="step reveal">
                <div class="step-number">1</div>
                <h3>Download & Register</h3>
                <p>Download the app and create your safety profile with emergency contacts and medical info.</p>
            </div>
            <div class="step reveal">
                <div class="step-number">2</div>
                <h3>Set Up Contacts</h3>
                <p>Add trusted family members, friends, and local emergency services to your safety network.</p>
            </div>
            <div class="step reveal">
                <div class="step-number">3</div>
                <h3>Stay Protected</h3>
                <p>Use SOS alerts, location sharing, and medical support whenever you need help most.</p>
            </div>
        </div>
    </section>

    <!-- Emergency Services -->
    <section class="emergency-services" id="services">
        <div class="section-header reveal">
            <span class="section-badge"><i class="fas fa-hospital"></i> Emergency Services</span>
            <h2>Immediate Help When You Need It</h2>
            <p>Access critical emergency services with one tap</p>
        </div>
        <div class="services-grid">
            <div class="service-card reveal">
                <span class="service-icon">🚑</span>
                <h4>Ambulance</h4>
                <p>Immediate medical transport</p>
            </div>
            <div class="service-card reveal">
                <span class="service-icon">🚒</span>
                <h4>Fire Department</h4>
                <p>Fire & rescue services</p>
            </div>
            <div class="service-card reveal">
                <span class="service-icon">🚔</span>
                <h4>Police</h4>
                <p>Law enforcement assistance</p>
            </div>
            <div class="service-card reveal">
                <span class="service-icon">🏥</span>
                <h4>Hospital</h4>
                <p>Nearest hospital finder</p>
            </div>
            <div class="service-card reveal">
                <span class="service-icon">👨‍⚕️</span>
                <h4>Doctor</h4>
                <p>Telemedicine consultation</p>
            </div>
        </div>
    </section>

    <!-- Testimonials -->
    <section class="testimonials" id="testimonials">
        <div class="section-header reveal">
            <span class="section-badge"><i class="fas fa-heart"></i> Real Stories</span>
            <h2>Stories That Inspire</h2>
            <p>Real people, real emergencies, real lifesaving moments</p>
        </div>
        <div class="testimonials-grid">
            <div class="testimonial-card reveal">
                <p class="testimonial-text">HumanSafe saved my life when I had a cardiac emergency. The SOS button connected me to paramedics in under 3 seconds. I cannot recommend this enough!</p>
                <div class="testimonial-author">
                    <div class="author-avatar">RK</div>
                    <div class="author-info">
                        <h5>Rajesh Kumar</h5>
                        <span>Mumbai, India</span>
                    </div>
                </div>
            </div>
            <div class="testimonial-card reveal">
                <p class="testimonial-text">As a woman living alone, HumanSafe gives me complete peace of mind. The location sharing and SOS features make me feel truly protected every day.</p>
                <div class="testimonial-author">
                    <div class="author-avatar">SP</div>
                    <div class="author-info">
                        <h5>Sarah Parker</h5>
                        <span>New York, USA</span>
                    </div>
                </div>
            </div>
            <div class="testimonial-card reveal">
                <p class="testimonial-text">My parents are elderly and live alone. With HumanSafe, I can monitor their safety and get instant alerts. It has brought our family tremendous relief.</p>
                <div class="testimonial-author">
                    <div class="author-avatar">AL</div>
                    <div class="author-info">
                        <h5>Anika Lee</h5>
                        <span>Singapore</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Download CTA -->
    <section class="download-cta">
        <h2>Download HumanSafe Today</h2>
        <p>Join 500,000+ people who trust HumanSafe for their safety</p>
        <div class="download-buttons">
            <button class="download-btn">
                <i class="fab fa-apple"></i> App Store
            </button>
            <button class="download-btn">
                <i class="fab fa-google-play"></i> Google Play
            </button>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="footer-grid">
            <div class="footer-brand">
                <div class="logo-text">Human<span>Safe</span></div>
                <p>Protecting lives through technology. Your safety is our mission, and we never stop innovating to keep you and your loved ones safe.</p>
                <div class="social-links">
                    <a href="#"><i class="fab fa-facebook-f"></i></a>
                    <a href="#"><i class="fab fa-twitter"></i></a>
                    <a href="#"><i class="fab fa-instagram"></i></a>
                    <a href="#"><i class="fab fa-linkedin-in"></i></a>
                </div>
            </div>
            <div class="footer-col">
                <h4>Product</h4>
                <a href="#">Features</a>
                <a href="#">Pricing</a>
                <a href="#">Download</a>
                <a href="#">Updates</a>
            </div>
            <div class="footer-col">
                <h4>Company</h4>
                <a href="#">About Us</a>
                <a href="#">Careers</a>
                <a href="#">Blog</a>
                <a href="#">Press</a>
            </div>
            <div class="footer-col">
                <h4>Support</h4>
                <a href="#">Help Center</a>
                <a href="#">Contact</a>
                <a href="#">Privacy Policy</a>
                <a href="#">Terms of Service</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 HumanSafe. All rights reserved. Made with <i class="fas fa-heart" style="color: var(--red);"></i> for humanity.</p>
        </div>
    </footer>

    <!-- SOS Modal -->
    <div class="modal-overlay" id="sosModal">
        <div class="modal">
            <div class="modal-icon"><i class="fas fa-exclamation-triangle"></i></div>
            <h2>SOS EMERGENCY</h2>
            <p>Select the type of emergency for immediate assistance</p>
            <div class="emergency-numbers">
                <div class="emergency-number">
                    <span><i class="fas fa-ambulance"></i> Medical Emergency</span>
                    <a href="tel:108">Call 108</a>
                </div>
                <div class="emergency-number">
                    <span><i class="fas fa-fire-extinguisher"></i> Fire Emergency</span>
                    <a href="tel:101">Call 101</a>
                </div>
                <div class="emergency-number">
                    <span><i class="fas fa-shield-alt"></i> Police</span>
                    <a href="tel:100">Call 100</a>
                </div>
                <div class="emergency-number">
                    <span><i class="fas fa-female"></i> Women Helpline</span>
                    <a href="tel:1091">Call 1091</a>
                </div>
            </div>
            <button class="close-modal" onclick="closeSOSModal()">Close</button>
        </div>
    </div>

    <script>
        // Create Particles
        function createParticles() {
            const container = document.getElementById('particles');
            const colors = ['#E63946', '#1D3557', '#457B9D', '#A8DADC'];
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.width = Math.random() * 20 + 5 + 'px';
                particle.style.height = particle.style.width;
                particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                particle.style.animationDuration = Math.random() * 15 + 10 + 's';
                particle.style.animationDelay = Math.random() * 10 + 's';
                container.appendChild(particle);
            }
        }

        // Navbar Scroll Effect
        window.addEventListener('scroll', () => {
            const nav = document.getElementById('navbar');
            nav.classList.toggle('scrolled', window.scrollY > 50);
        });

        // Scroll Reveal Animation
        function revealOnScroll() {
            const reveals = document.querySelectorAll('.reveal');
            reveals.forEach(el => {
                const windowHeight = window.innerHeight;
                const elementTop = el.getBoundingClientRect().top;
                if (elementTop < windowHeight - 100) {
                    el.classList.add('active');
                }
            });
        }

        // Counter Animation
        function animateCounters() {
            const counters = document.querySelectorAll('.counter');
            counters.forEach(counter => {
                const target = parseInt(counter.getAttribute('data-target'));
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;

                const updateCounter = () => {
                    current += step;
                    if (current < target) {
                        counter.textContent = Math.floor(current).toLocaleString();
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target.toLocaleString();
                    }
                };

                const observer = new IntersectionObserver(entries => {
                    if (entries[0].isIntersecting) {
                        updateCounter();
                        observer.disconnect();
                    }
                });

                observer.observe(counter);
            });
        }

        // SOS Modal
        function openSOSModal() {
            document.getElementById('sosModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeSOSModal() {
            document.getElementById('sosModal').classList.remove('active');
            document.body.style.overflow = 'auto';
        }

        // Close modal on overlay click
        document.getElementById('sosModal').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) closeSOSModal();
        });

        // Smooth scroll for nav links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });

        // Initialize
        window.addEventListener('load', () => {
            createParticles();
            animateCounters();
            revealOnScroll();
        });

        window.addEventListener('scroll', revealOnScroll);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'HumanSafe'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
