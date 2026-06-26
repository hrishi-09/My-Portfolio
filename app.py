"""
Hrishita Sinha | Portfolio — app.py
Run locally:  python app.py
Deploy on:    Render (Web Service, Python, Start Command: python app.py)
"""

import http.server
import socketserver
import os

# Render injects PORT automatically; fallback to 8000 for local dev
PORT = int(os.environ.get("PORT", 8000))

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Hrishita Sinha | Portfolio</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  :root{
    --primary:#6c63ff;
    --secondary:#f50057;
    --dark:#060614;
    --card:#1a1a2e;
    --card2:#16213e;
    --text:#e0e0e0;
    --muted:#9e9e9e;
    --accent:#00d4ff;
  }
  html,body{scroll-behavior:smooth;height:100%;}
  body{font-family:'Segoe UI',sans-serif;background:var(--dark);color:var(--text);overflow-x:hidden;}

  /* ── 3-D SPACE CANVAS ── */
  #space-canvas{
    position:fixed;top:0;left:0;width:100%;height:100%;
    z-index:0;pointer-events:none;
  }

  /* everything above the canvas */
  nav,#hero,.section-wrap,footer{position:relative;z-index:1;}

  /* NAV */
  nav{position:fixed;top:0;width:100%;z-index:999;
      background:rgba(6,6,20,0.85);backdrop-filter:blur(14px);
      border-bottom:1px solid rgba(108,99,255,0.2);}
  .nav-inner{max-width:1100px;margin:auto;display:flex;
             justify-content:space-between;align-items:center;padding:16px 24px;}
  .logo{font-size:1.4rem;font-weight:700;
        background:linear-gradient(90deg,var(--primary),var(--accent));
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;}
  .nav-links{display:flex;gap:28px;list-style:none;}
  .nav-links a{color:var(--muted);text-decoration:none;font-size:.95rem;
               transition:.3s;letter-spacing:.5px;}
  .nav-links a:hover{color:var(--accent);}
  .hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;}
  .hamburger span{width:24px;height:2px;background:var(--text);border-radius:2px;transition:.3s;}

  /* HERO */
  #hero{min-height:100vh;display:flex;align-items:center;justify-content:center;
        text-align:center;padding:100px 24px 60px;}
  .avatar-placeholder{width:140px;height:140px;border-radius:50%;
    border:3px solid var(--primary);
    background:linear-gradient(135deg,var(--primary),var(--accent));
    display:flex;align-items:center;justify-content:center;font-size:3.2rem;
    margin:0 auto 24px;box-shadow:0 0 40px rgba(108,99,255,0.6);}
  h1.name{font-size:clamp(2rem,5vw,3.5rem);font-weight:800;
          background:linear-gradient(90deg,#fff,var(--accent));
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px;}
  .tagline{font-size:1.1rem;color:var(--muted);margin-bottom:18px;letter-spacing:1px;}
  .objective{max-width:640px;margin:0 auto 32px;color:#b0b0c8;line-height:1.7;font-size:.97rem;}
  .hero-btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}
  .btn{padding:12px 28px;border-radius:50px;font-size:.95rem;font-weight:600;
       text-decoration:none;transition:.3s;cursor:pointer;border:none;}
  .btn-primary{background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;
               box-shadow:0 4px 20px rgba(108,99,255,0.4);}
  .btn-primary:hover{transform:translateY(-2px);box-shadow:0 6px 28px rgba(108,99,255,0.6);}
  .btn-outline{background:transparent;color:var(--accent);border:2px solid var(--accent);}
  .btn-outline:hover{background:var(--accent);color:#000;}
  .social-links{display:flex;gap:16px;justify-content:center;margin-top:24px;}
  .social-links a{color:var(--muted);font-size:.9rem;text-decoration:none;
                  display:flex;align-items:center;gap:6px;padding:8px 16px;
                  border:1px solid rgba(255,255,255,0.1);border-radius:50px;transition:.3s;}
  .social-links a:hover{color:var(--accent);border-color:var(--accent);}

  /* SECTION WRAPPER */
  .section-wrap{padding:80px 24px;max-width:1100px;margin:auto;}
  .section-wrap.full{max-width:100%;padding:80px 0;}
  .section-wrap.full .inner{max-width:1100px;margin:auto;padding:0 24px;}
  .section-bg{background:rgba(6,6,20,0.55);backdrop-filter:blur(6px);}

  .section-title{font-size:clamp(1.5rem,3vw,2rem);font-weight:700;margin-bottom:48px;
                 text-align:center;position:relative;}
  .section-title::after{content:'';display:block;width:60px;height:3px;
    background:linear-gradient(90deg,var(--primary),var(--accent));
    margin:12px auto 0;border-radius:2px;}

  /* SKILLS */
  .skills-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;}
  .skill-card{background:rgba(26,26,46,0.75);border:1px solid rgba(108,99,255,0.2);
              border-radius:16px;padding:24px;transition:.3s;backdrop-filter:blur(4px);}
  .skill-card:hover{border-color:var(--accent);transform:translateY(-4px);
                    box-shadow:0 8px 30px rgba(0,212,255,0.12);}
  .skill-card h3{color:var(--accent);margin-bottom:14px;font-size:1rem;
                 text-transform:uppercase;letter-spacing:1px;}
  .skill-tags{display:flex;flex-wrap:wrap;gap:8px;}
  .tag{background:rgba(108,99,255,0.15);color:var(--primary);padding:5px 14px;
       border-radius:50px;font-size:.82rem;border:1px solid rgba(108,99,255,0.3);}

  /* EDUCATION TIMELINE */
  .timeline{position:relative;padding-left:32px;}
  .timeline::before{content:'';position:absolute;left:8px;top:0;bottom:0;width:2px;
    background:linear-gradient(to bottom,var(--primary),var(--accent));}
  .tl-item{position:relative;margin-bottom:36px;}
  .tl-dot{position:absolute;left:-28px;top:6px;width:14px;height:14px;border-radius:50%;
          background:var(--primary);border:2px solid var(--accent);
          box-shadow:0 0 10px rgba(108,99,255,0.6);}
  .tl-card{background:rgba(26,26,46,0.75);border:1px solid rgba(108,99,255,0.2);
           border-radius:14px;padding:20px 24px;transition:.3s;backdrop-filter:blur(4px);}
  .tl-card:hover{border-color:var(--accent);}
  .tl-card h3{font-size:1.05rem;margin-bottom:6px;color:#fff;}
  .tl-card .institute{color:var(--accent);font-size:.9rem;margin-bottom:6px;}
  .tl-card .meta{display:flex;gap:16px;flex-wrap:wrap;}
  .tl-card .meta span{font-size:.85rem;color:var(--muted);}
  .badge{background:linear-gradient(135deg,var(--primary),var(--accent));
         color:#fff;padding:3px 12px;border-radius:50px;font-size:.8rem;font-weight:600;}

  /* PROJECTS */
  .projects-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px;}
  .proj-card{background:rgba(26,26,46,0.75);border:1px solid rgba(108,99,255,0.2);
             border-radius:16px;padding:26px;transition:.3s;position:relative;
             overflow:hidden;backdrop-filter:blur(4px);}
  .proj-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,var(--primary),var(--accent));}
  .proj-card:hover{transform:translateY(-5px);box-shadow:0 12px 40px rgba(108,99,255,0.2);
                   border-color:var(--primary);}
  .proj-icon{font-size:2rem;margin-bottom:14px;}
  .proj-card h3{font-size:1.1rem;margin-bottom:10px;color:#fff;}
  .proj-card p{color:var(--muted);font-size:.9rem;line-height:1.6;}

  /* INTERNSHIP */
  .intern-card{background:linear-gradient(135deg,rgba(108,99,255,0.12),rgba(0,212,255,0.06));
    border:1px solid rgba(108,99,255,0.3);border-radius:16px;padding:30px;
    display:flex;gap:20px;align-items:flex-start;backdrop-filter:blur(6px);}
  .intern-icon{font-size:2.5rem;flex-shrink:0;}
  .intern-card h3{font-size:1.15rem;margin-bottom:8px;}
  .intern-card p{color:var(--muted);font-size:.93rem;line-height:1.6;}
  .intern-duration{display:inline-block;margin-top:10px;background:rgba(108,99,255,0.2);
    color:var(--primary);padding:4px 14px;border-radius:50px;font-size:.82rem;
    border:1px solid rgba(108,99,255,0.4);}

  /* INTERESTS */
  .interests-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;}
  .interest-card{background:rgba(22,33,62,0.7);border:1px solid rgba(255,255,255,0.07);
    border-radius:14px;padding:20px;text-align:center;transition:.3s;backdrop-filter:blur(4px);}
  .interest-card:hover{border-color:var(--accent);transform:translateY(-3px);}
  .interest-card .icon{font-size:2rem;margin-bottom:10px;}
  .interest-card p{color:var(--muted);font-size:.9rem;}

  /* LANGUAGES */
  .lang-table{width:100%;border-collapse:collapse;
    background:rgba(26,26,46,0.75);border-radius:14px;overflow:hidden;backdrop-filter:blur(4px);}
  .lang-table th{background:rgba(108,99,255,0.3);color:#fff;padding:14px 20px;
    text-align:left;font-size:.9rem;text-transform:uppercase;letter-spacing:.8px;}
  .lang-table td{padding:14px 20px;border-bottom:1px solid rgba(255,255,255,0.05);
    color:var(--muted);font-size:.92rem;}
  .lang-table tr:last-child td{border-bottom:none;}
  .lang-table tr:hover td{background:rgba(108,99,255,0.07);}
  .check{color:#4caf50;font-size:1.1rem;}
  .prof-badge{padding:3px 12px;border-radius:50px;font-size:.8rem;font-weight:600;}
  .prof-badge.proficient{background:rgba(76,175,80,0.15);color:#4caf50;
    border:1px solid rgba(76,175,80,0.3);}
  .prof-badge.beginner{background:rgba(255,152,0,0.15);color:#ff9800;
    border:1px solid rgba(255,152,0,0.3);}

  /* CONTACT */
  .contact-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;}
  .contact-item{background:rgba(26,26,46,0.75);border:1px solid rgba(108,99,255,0.2);
    border-radius:14px;padding:22px;display:flex;gap:14px;align-items:center;transition:.3s;
    text-decoration:none;color:var(--text);backdrop-filter:blur(4px);}
  .contact-item:hover{border-color:var(--accent);transform:translateY(-3px);}
  .contact-item .ci-icon{font-size:1.8rem;flex-shrink:0;}
  .contact-item .ci-label{font-size:.8rem;color:var(--muted);margin-bottom:3px;
    text-transform:uppercase;letter-spacing:.5px;}
  .contact-item .ci-value{font-size:.92rem;color:var(--accent);}

  footer{text-align:center;padding:30px 24px;
    border-top:1px solid rgba(255,255,255,0.06);color:var(--muted);font-size:.88rem;}

  /* FADE-IN */
  .fade-in{opacity:0;transform:translateY(30px);transition:.6s ease;}
  .fade-in.visible{opacity:1;transform:translateY(0);}

  @media(max-width:768px){
    .nav-links{display:none;flex-direction:column;position:absolute;top:64px;left:0;right:0;
      background:var(--dark);padding:20px 24px;gap:16px;
      border-bottom:1px solid rgba(108,99,255,0.2);}
    .nav-links.open{display:flex;}
    .hamburger{display:flex;}
    .intern-card{flex-direction:column;}
  }
</style>
</head>
<body>

<!-- 3-D SPACE CANVAS -->
<canvas id="space-canvas"></canvas>

<!-- NAV -->
<nav>
  <div class="nav-inner">
    <div class="logo">HS.</div>
    <ul class="nav-links" id="navLinks">
      <li><a href="#hero">Home</a></li>
      <li><a href="#skills">Skills</a></li>
      <li><a href="#education">Education</a></li>
      <li><a href="#projects">Projects</a></li>
      <li><a href="#internship">Internship</a></li>
      <li><a href="#contact">Contact</a></li>
    </ul>
    <div class="hamburger" id="hamburger" onclick="toggleNav()">
      <span></span><span></span><span></span>
    </div>
  </div>
</nav>

<!-- HERO -->
<section id="hero">
  <div>
    <div class="avatar-placeholder">&#x1F469;&#x200D;&#x1F4BB;</div>
    <h1 class="name">Hrishita Sinha</h1>
    <p class="tagline">BCA Student &nbsp;|&nbsp; Python Developer &nbsp;|&nbsp; Backend Enthusiast</p>
    <p class="objective">Detail-oriented Bachelor's of Computer Application student with a strong foundation in programming and problem-solving, seeking an opportunity in a growth-oriented organisation to apply technical skills, enhance practical knowledge, and contribute effectively to innovative projects.</p>
    <div class="hero-btns">
      <a href="#projects" class="btn btn-primary">View Projects</a>
      <a href="#contact" class="btn btn-outline">Contact Me</a>
    </div>
    <div class="social-links">
      <a href="https://www.linkedin.com/in/hrishita-sinha-90a704320" target="_blank">&#x1F517; LinkedIn</a>
      <a href="https://github.com/hrishi-09" target="_blank">&#x1F419; GitHub</a>
      <a href="mailto:hrishitasinhaiembca2028@gmail.com">&#x2709;&#xFE0F; Email</a>
    </div>
  </div>
</section>

<!-- SKILLS -->
<div id="skills" class="section-bg" style="padding:80px 0;">
<div class="section-wrap">
  <h2 class="section-title fade-in">Technical Skills</h2>
  <div class="skills-grid fade-in">
    <div class="skill-card">
      <h3>&#x1F4BB; Programming Languages</h3>
      <div class="skill-tags">
        <span class="tag">Python</span><span class="tag">C</span><span class="tag">C++</span>
      </div>
    </div>
    <div class="skill-card">
      <h3>&#x1F5C4;&#xFE0F; Database</h3>
      <div class="skill-tags"><span class="tag">MySQL</span></div>
    </div>
    <div class="skill-card">
      <h3>&#x1F9E0; Core Concepts</h3>
      <div class="skill-tags">
        <span class="tag">OOP</span><span class="tag">DBMS</span><span class="tag">Computer Networks</span>
      </div>
    </div>
    <div class="skill-card">
      <h3>&#x1F6E0;&#xFE0F; Tools</h3>
      <div class="skill-tags"><span class="tag">VS Code</span></div>
    </div>
  </div>
</div>
</div>

<!-- EDUCATION -->
<section id="education">
<div class="section-wrap">
  <h2 class="section-title fade-in">Education</h2>
  <div class="timeline fade-in">
    <div class="tl-item">
      <div class="tl-dot"></div>
      <div class="tl-card">
        <h3>Bachelor of Computer Application (BCA)</h3>
        <div class="institute">Institute of Engineering and Management</div>
        <div class="meta"><span>&#x1F4C5; 2024 – 2028 (Ongoing)</span><span class="badge">CGPA: 8.48</span></div>
      </div>
    </div>
    <div class="tl-item">
      <div class="tl-dot"></div>
      <div class="tl-card">
        <h3>Class XII — CBSE</h3>
        <div class="institute">Gokhale Memorial Girls School</div>
        <div class="meta"><span>&#x1F4C5; 2024</span><span class="badge">77.9%</span></div>
      </div>
    </div>
    <div class="tl-item">
      <div class="tl-dot"></div>
      <div class="tl-card">
        <h3>Class X — CBSE</h3>
        <div class="institute">G.S.S Girls School</div>
        <div class="meta"><span>&#x1F4C5; 2020</span><span class="badge">81.4%</span></div>
      </div>
    </div>
  </div>
</div>
</section>

<!-- PROJECTS -->
<div id="projects" class="section-bg" style="padding:80px 0;">
<div class="section-wrap">
  <h2 class="section-title fade-in">Projects</h2>
  <div class="projects-grid fade-in">
    <div class="proj-card">
      <div class="proj-icon">&#x1F3E8;</div>
      <h3>Hotel Management System</h3>
      <p>A comprehensive system to manage hotel operations including bookings, guest records, and room management. Built with strong database integration.</p>
    </div>
    <div class="proj-card">
      <div class="proj-icon">&#x1F4FA;</div>
      <h3>TENFLEX</h3>
      <p>A streaming-inspired platform project showcasing UI and backend integration skills developed during academic coursework.</p>
    </div>
    <div class="proj-card">
      <div class="proj-icon">&#x1F6E1;&#xFE0F;</div>
      <h3>Cyber-AI Dashboard</h3>
      <p>An AI-powered cybersecurity dashboard project focused on monitoring and visualising security metrics and threat intelligence.</p>
    </div>
  </div>
</div>
</div>

<!-- INTERNSHIP -->
<section id="internship">
<div class="section-wrap">
  <h2 class="section-title fade-in">Internship Experience</h2>
  <div class="intern-card fade-in">
    <div class="intern-icon">&#x1F680;</div>
    <div>
      <h3>Python Developer Intern</h3>
      <p>The Entrepreneurship Network — <em>Limitless Technologies LLP</em></p>
      <p style="margin-top:8px;color:var(--muted);font-size:.93rem;">Worked as a Python Developer intern, applying programming skills to real-world projects and gaining hands-on experience in software development within a startup environment.</p>
      <span class="intern-duration">&#x23F1; 3 Months</span>
    </div>
  </div>
</div>
</section>

<!-- INTERESTS -->
<div id="interests" class="section-bg" style="padding:80px 0;">
<div class="section-wrap">
  <h2 class="section-title fade-in">Areas of Interest</h2>
  <div class="interests-grid fade-in">
    <div class="interest-card"><div class="icon">&#x2699;&#xFE0F;</div><p>Backend Development</p></div>
    <div class="interest-card"><div class="icon">&#x1F4A1;</div><p>Technology &amp; Innovation</p></div>
    <div class="interest-card"><div class="icon">&#x1F4DA;</div><p>Continuous Learning &amp; Skill Development</p></div>
    <div class="interest-card"><div class="icon">&#x1F30D;</div><p>Exploring New Places</p></div>
  </div>
</div>
</div>

<!-- LANGUAGES -->
<section id="languages">
<div class="section-wrap">
  <h2 class="section-title fade-in">Languages Known</h2>
  <div class="fade-in" style="overflow-x:auto;">
    <table class="lang-table">
      <thead>
        <tr><th>Language</th><th>Read</th><th>Speak</th><th>Write</th><th>Proficiency</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>English</td>
          <td><span class="check">✓</span></td><td><span class="check">✓</span></td><td><span class="check">✓</span></td>
          <td><span class="prof-badge proficient">Proficient</span></td>
        </tr>
        <tr>
          <td>Hindi</td>
          <td><span class="check">✓</span></td><td><span class="check">✓</span></td><td>—</td>
          <td><span class="prof-badge beginner">Beginner</span></td>
        </tr>
        <tr>
          <td>Bengali</td>
          <td><span class="check">✓</span></td><td><span class="check">✓</span></td><td><span class="check">✓</span></td>
          <td><span class="prof-badge proficient">Proficient</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
</section>

<!-- CONTACT -->
<div id="contact" class="section-bg" style="padding:80px 0;">
<div class="section-wrap">
  <h2 class="section-title fade-in">Get In Touch</h2>
  <div class="contact-grid fade-in">
    <a class="contact-item" href="mailto:hrishitasinhaiembca2028@gmail.com">
      <div class="ci-icon">&#x2709;&#xFE0F;</div>
      <div><div class="ci-label">Email</div><div class="ci-value">hrishitasinhaiembca2028@gmail.com</div></div>
    </a>
    <a class="contact-item" href="tel:+917583933738">
      <div class="ci-icon">&#x1F4F1;</div>
      <div><div class="ci-label">Mobile</div><div class="ci-value">+91 7583933738</div></div>
    </a>
    <a class="contact-item" href="https://www.linkedin.com/in/hrishita-sinha-90a704320" target="_blank">
      <div class="ci-icon">&#x1F517;</div>
      <div><div class="ci-label">LinkedIn</div><div class="ci-value">hrishita-sinha-90a704320</div></div>
    </a>
    <a class="contact-item" href="https://github.com/hrishi-09" target="_blank">
      <div class="ci-icon">&#x1F419;</div>
      <div><div class="ci-label">GitHub</div><div class="ci-value">github.com/hrishi-09</div></div>
    </a>
    <div class="contact-item">
      <div class="ci-icon">&#x1F4CD;</div>
      <div><div class="ci-label">Location</div><div class="ci-value">34/1 South Behala Road, Kolkata – 700061</div></div>
    </div>
  </div>
</div>
</div>

<footer>
  <p>© 2026 Hrishita Sinha &nbsp;|&nbsp; Crafted with ❤️ &nbsp;|&nbsp; BCA Student @ IEM Kolkata</p>
</footer>

<!-- THREE.JS  -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
/* ═══════════════════════════════════════════════
   3-D SPACE SCENE
   • Starfield (2 000 points)
   • Slow-rotating coloured nebula cloud (fog geometry)
   • 6 orbiting planet spheres with glow halos
   • Shooting-star particles
   • Mouse-parallax tilt
═══════════════════════════════════════════════ */
(function(){
  const canvas = document.getElementById('space-canvas');
  const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:true});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
  renderer.setSize(window.innerWidth, window.innerHeight);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 2000);
  camera.position.set(0, 0, 80);

  /* ── STARS ── */
  const starGeo = new THREE.BufferGeometry();
  const starCount = 2000;
  const starPos = new Float32Array(starCount * 3);
  for(let i=0;i<starCount*3;i++) starPos[i] = (Math.random()-0.5)*1600;
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos,3));
  const starMat = new THREE.PointsMaterial({color:0xffffff, size:0.8, sizeAttenuation:true});
  scene.add(new THREE.Points(starGeo, starMat));

  /* ── NEBULA (random coloured small spheres forming a cloud) ── */
  const nebulaGroup = new THREE.Group();
  const nebulaColors = [0x6c63ff, 0x00d4ff, 0xf50057, 0x9c27b0, 0x3f51b5];
  for(let i=0;i<120;i++){
    const geo = new THREE.SphereGeometry(Math.random()*2+0.5, 6, 6);
    const mat = new THREE.MeshBasicMaterial({
      color: nebulaColors[Math.floor(Math.random()*nebulaColors.length)],
      transparent:true, opacity: Math.random()*0.12+0.03, wireframe:false
    });
    const mesh = new THREE.Mesh(geo, mat);
    const r = Math.random()*180+60;
    const theta = Math.random()*Math.PI*2;
    const phi = (Math.random()-0.5)*Math.PI;
    mesh.position.set(
      r*Math.cos(theta)*Math.cos(phi),
      r*Math.sin(phi)*0.4,
      r*Math.sin(theta)*Math.cos(phi)
    );
    nebulaGroup.add(mesh);
  }
  scene.add(nebulaGroup);

  /* ── PLANETS ── */
  const planetData = [
    {radius:5,  color:0x6c63ff, dist:120, speed:0.0004, tilt:0.3,  wobble:8},
    {radius:3,  color:0x00d4ff, dist:80,  speed:0.0007, tilt:0.8,  wobble:5},
    {radius:7,  color:0x3f51b5, dist:180, speed:0.0002, tilt:0.2,  wobble:12},
    {radius:2.5,color:0xf50057, dist:55,  speed:0.0012, tilt:1.1,  wobble:3},
    {radius:4,  color:0x9c27b0, dist:145, speed:0.0005, tilt:0.5,  wobble:9},
    {radius:6,  color:0x00897b, dist:220, speed:0.00015,tilt:0.15, wobble:16},
  ];

  const planets = planetData.map(p=>{
    const geo = new THREE.SphereGeometry(p.radius, 32, 32);
    const mat = new THREE.MeshPhongMaterial({
      color:p.color, emissive:p.color, emissiveIntensity:0.2,
      shininess:80, specular:0x444444
    });
    const mesh = new THREE.Mesh(geo, mat);

    /* halo glow ring */
    const ringGeo = new THREE.TorusGeometry(p.radius+1.2, 0.3, 8, 80);
    const ringMat = new THREE.MeshBasicMaterial({color:p.color, transparent:true, opacity:0.35});
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = Math.PI/2;
    mesh.add(ring);

    scene.add(mesh);
    return {...p, mesh, angle: Math.random()*Math.PI*2};
  });

  /* ── AMBIENT + POINT LIGHTS ── */
  scene.add(new THREE.AmbientLight(0x111133, 1.5));
  const sunLight = new THREE.PointLight(0x6c63ff, 2, 600);
  sunLight.position.set(0,0,0);
  scene.add(sunLight);
  const fill = new THREE.PointLight(0x00d4ff, 1, 400);
  fill.position.set(-200,80,-100);
  scene.add(fill);

  /* ── SHOOTING STARS ── */
  const shooters = [];
  function spawnShooter(){
    const geo = new THREE.BufferGeometry();
    const len = Math.random()*20+10;
    geo.setAttribute('position', new THREE.BufferAttribute(
      new Float32Array([0,0,0, len,0,0]), 3));
    const mat = new THREE.LineBasicMaterial({
      color:0xffffff, transparent:true, opacity:0.8});
    const line = new THREE.Line(geo, mat);
    line.position.set(
      (Math.random()-0.5)*400, (Math.random()-0.5)*200, (Math.random()-0.5)*200
    );
    line.rotation.z = Math.random()*Math.PI;
    line._vel = new THREE.Vector3(
      (Math.random()-0.5)*3, -(Math.random()*1+0.5), (Math.random()-0.5)*1
    );
    line._life = 1.0;
    scene.add(line);
    shooters.push(line);
  }
  setInterval(spawnShooter, 2000);

  /* ── MOUSE PARALLAX ── */
  let mouseX=0, mouseY=0;
  document.addEventListener('mousemove', e=>{
    mouseX = (e.clientX/window.innerWidth  - 0.5)*2;
    mouseY = (e.clientY/window.innerHeight - 0.5)*2;
  });

  /* ── SCROLL — camera z drift ── */
  let scrollY = 0;
  window.addEventListener('scroll', ()=>{ scrollY = window.scrollY; });

  /* ── RESIZE ── */
  window.addEventListener('resize',()=>{
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
  });

  /* ── RENDER LOOP ── */
  let t=0;
  function animate(){
    requestAnimationFrame(animate);
    t += 0.005;

    /* rotate nebula slowly */
    nebulaGroup.rotation.y = t*0.05;
    nebulaGroup.rotation.x = Math.sin(t*0.03)*0.1;

    /* orbit planets */
    planets.forEach(p=>{
      p.angle += p.speed;
      p.mesh.position.set(
        Math.cos(p.angle)*p.dist,
        Math.sin(t*0.2+p.tilt)*p.wobble,
        Math.sin(p.angle)*p.dist
      );
      p.mesh.rotation.y += 0.003;
    });

    /* shooting stars */
    for(let i=shooters.length-1;i>=0;i--){
      const s = shooters[i];
      s.position.addScaledVector(s._vel, 1);
      s._life -= 0.012;
      s.material.opacity = s._life;
      if(s._life <= 0){ scene.remove(s); shooters.splice(i,1); }
    }

    /* camera parallax tilt */
    camera.position.x += (mouseX*12 - camera.position.x)*0.04;
    camera.position.y += (-mouseY*8  - camera.position.y)*0.04;
    /* drift camera forward as user scrolls */
    const targetZ = 80 - scrollY*0.04;
    camera.position.z += (targetZ - camera.position.z)*0.05;
    camera.lookAt(0,0,0);

    renderer.render(scene, camera);
  }
  animate();
})();

/* ── PAGE JS (nav, scroll-fade, typing) ── */
document.querySelectorAll('.nav-links a, .hero-btns a').forEach(a=>{
  a.addEventListener('click', e=>{
    const href = a.getAttribute('href');
    if(href && href.startsWith('#')){
      e.preventDefault();
      const tgt = document.querySelector(href);
      if(tgt) tgt.scrollIntoView({behavior:'smooth', block:'start'});
      document.getElementById('navLinks').classList.remove('open');
    }
  });
});
function toggleNav(){ document.getElementById('navLinks').classList.toggle('open'); }
const obs = new IntersectionObserver(entries=>{
  entries.forEach(e=>{ if(e.isIntersecting) e.target.classList.add('visible'); });
},{threshold:.1});
document.querySelectorAll('.fade-in').forEach(el=>obs.observe(el));

const tagline = document.querySelector('.tagline');
const txt = tagline.textContent;
tagline.textContent='';
let i=0;
setTimeout(()=>{
  const ti = setInterval(()=>{ tagline.textContent+=txt[i++]; if(i>=txt.length) clearInterval(ti); },40);
},600);
</script>
</body>
</html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        print(f"[{self.address_string()}] {fmt % args}")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"✅  Portfolio running at  http://localhost:{PORT}")
        print("    Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋  Server stopped.")
