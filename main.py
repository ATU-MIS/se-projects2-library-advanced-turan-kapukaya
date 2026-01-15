import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import time

app = FastAPI()

# --- VERİTABANI VE DERS İÇERİKLERİ ---
users_db = {"turan": {"pass": "12345", "name": "Turan Kapukaya"}}
# İstediğin videolar ve başlıklar eklendi
courses_db = [
    {
        "id": 101, 
        "title": "Yazılım Mühendisliğine Giriş", 
        "cat": "Mühendislik", 
        "embed_url": "https://www.youtube.com/embed/-2tzE5NWDPI",
        "desc": "Yazılım yaşam döngüsü ve temel prensipler."
    },
    {
        "id": 102, 
        "title": "Python ile Veri Bilimi", 
        "cat": "Programlama", 
        "embed_url": "https://www.youtube.com/embed/_c83igSzuZA",
        "desc": "Veri analizi ve Python kütüphaneleri eğitimi."
    },
    {
        "id": 103, 
        "title": "Ağ Güvenliği Temelleri", 
        "cat": "Siber Güvenlik", 
        "embed_url": "https://www.youtube.com/embed/AmvaCnkTKAk",
        "desc": "Network security ve temel kavramlar."
    },
    {
        "id": 104, 
        "title": "Modern Web Teknolojileri", 
        "cat": "Web Tasarım", 
        "embed_url": "https://www.youtube.com/embed/9vuoDtLfZc4",
        "desc": "Güncel web mimarileri ve güvenlik bakış açısı."
    }
]

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    if data.username in users_db and users_db[data.username]["pass"] == data.password:
        return {"status": "Success", "user": data.username, "fullname": users_db[data.username]["name"]}
    raise HTTPException(status_code=401)

# --- ARAYÜZ (HTML/CSS/JS) ---
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>T-Kampüs | Online Eğitim Platformu</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            
            body { 
                background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                            url('https://images.unsplash.com/photo-1524178232363-1fb2b075b655?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
                background-size: cover;
                background-attachment: fixed;
                min-height: 100vh;
                color: #333;
            }

            /* Navbar */
            .navbar { background: rgba(255, 255, 255, 0.95); padding: 10px 30px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 15px rgba(0,0,0,0.2); }
            .logo { font-size: 26px; font-weight: 900; color: #d32f2f; letter-spacing: -1px; }
            .stats-info { font-size: 13px; color: #555; display: flex; gap: 15px; font-weight: 600; }
            .online-dot { height: 10px; width: 10px; background-color: #4caf50; border-radius: 50%; display: inline-block; margin-right: 5px; animation: pulse 2s infinite; }
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }

            /* Menü */
            .menu-icon { font-size: 30px; cursor: pointer; color: #333; transition: 0.3s; }
            .dropdown { display: none; position: absolute; top: 60px; right: 20px; background: white; border-radius: 10px; box-shadow: 0 5px 25px rgba(0,0,0,0.2); width: 240px; overflow: hidden; }
            .dropdown div { padding: 15px 20px; border-bottom: 1px solid #f0f0f0; cursor: pointer; }
            .dropdown div:hover { background: #f8f8f8; color: #d32f2f; }

            /* Kartlar */
            .container { padding: 40px; display: flex; justify-content: center; width: 100%; }
            .card { background: rgba(255, 255, 255, 0.98); padding: 30px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.4); width: 100%; max-width: 1000px; }
            .hidden { display: none !important; }

            /* Ders Grid */
            .course-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
            .course-card { background: #fff; border: 1px solid #eee; border-radius: 15px; overflow: hidden; transition: 0.3s; padding: 20px; }
            .course-card:hover { transform: translateY(-10px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); border-color: #d32f2f; }
            .tag { background: #ffebee; color: #c62828; font-size: 11px; padding: 4px 10px; border-radius: 20px; font-weight: bold; text-transform: uppercase; }

            /* Video Player */
            .video-container { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 15px; border: 4px solid #d32f2f; margin: 20px 0; }
            .video-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }

            /* İlerleme Çubuğu */
            .progress-container { background: #eee; height: 12px; border-radius: 10px; margin: 15px 0; overflow: hidden; }
            .progress-bar { height: 100%; background: #4caf50; width: 0%; transition: 0.5s; }

            /* Input ve Buton */
            input { width: 100%; padding: 12px; margin: 10px 0; border: 2px solid #eee; border-radius: 10px; outline: none; }
            input:focus { border-color: #d32f2f; }
            button { background: #d32f2f; color: white; padding: 12px; border: none; border-radius: 10px; width: 100%; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 10px; }
        </style>
    </head>
    <body>

    <nav class="navbar">
        <div class="logo">T-Kampüs</div>
        <div id="nav-info" class="hidden">
            <div class="stats-info">
                <span><span class="online-dot"></span><span id="real-online">1</span> Online</span>
                <span>Oturum: <span id="session-clock">00:00</span></span>
                <span class="menu-icon" onclick="toggleMenu()">☰</span>
            </div>
            <div id="menuBox" class="dropdown">
                <div style="background:#f9f9f9; font-weight:800; color:#d32f2f" id="userTitle">Kullanıcı</div>
                <div onclick="showTab('course-tab')">📚 Ders Katalogu</div>
                <div onclick="showTab('profile-tab')">👤 Profilim</div>
                <div onclick="showTab('pass-tab')">🔑 Şifre Değiştir</div>
                <div onclick="showTab('suggest-tab')">💡 Öneri Sun</div>
                <div onclick="location.reload()" style="color:#d32f2f; font-weight:bold">🚪 Güvenli Çıkış</div>
            </div>
        </div>
    </nav>

    <div class="container">
        <div id="login-tab" class="card">
            <h2 style="text-align:center; margin-bottom:20px; color:#d32f2f">Eğitim Portalı Girişi</h2>
            <input type="text" id="userInput" placeholder="Kullanıcı Adı (turan)">
            <input type="password" id="passInput" placeholder="Şifre (12345)">
            <button onclick="login()">Sisteme Gir</button>
        </div>

        <div id="course-tab" class="card hidden">
            <h2 style="margin-bottom:20px; border-left: 5px solid #d32f2f; padding-left: 15px;">Ders Katalogu</h2>
            <div class="course-grid" id="grid"></div>
        </div>

        <div id="watch-tab" class="card hidden">
            <button onclick="showTab('course-tab')" style="width:auto; padding:5px 20px; margin-bottom:15px; background:#666">< Geri Dön</button>
            <h2 id="video-title">Ders</h2>
            <div class="video-container">
                <iframe id="player" src="" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            </div>
            <div class="progress-container"><div id="p-bar" class="progress-bar"></div></div>
            <p id="p-text" style="font-weight:bold">İlerleme: %0</p>
        </div>

        <div id="profile-tab" class="card hidden">
            <h2>Öğrenci Profili</h2>
            <div style="margin-top:20px; line-height:2">
                <p><b>Ad Soyad:</b> <span id="full-name"></span></p>
                <p><b>Numara:</b> 220202033</p>
                <p><b>Bölüm:</b> Yazılım Mühendisliği</p>
            </div>
            <button onclick="showTab('course-tab')">Tamam</button>
        </div>

        <div id="suggest-tab" class="card hidden">
            <h2>Öneri / Şikayet Formu</h2>
            <textarea style="width:100%; height:120px; margin-top:15px; padding:10px; border-radius:10px" placeholder="T-Kampüs geliştirme önerilerinizi yazın..."></textarea>
            <button onclick="alert('Teşekkürler, öneriniz kaydedildi!'); showTab('course-tab')">Gönder</button>
        </div>
    </div>

    <script>
        let user = "";
        let loginTime = 0;
        let progressVal = 0;
        let pInterval;

        // GERÇEKÇİ ONLINE SAYISI: Sayfada durdukça rastgele artıp azalır (Gerçek hayat simülasyonu)
        setInterval(() => {
            let base = Math.floor(Math.random() * 50) + 120; // 120-170 arası gerçekçi aktif kullanıcı
            if(user) document.getElementById('real-online').innerText = base;
        }, 4000);

        // OTURUM SÜRESİ
        setInterval(() => {
            if(loginTime > 0) {
                let sec = Math.floor((Date.now() - loginTime) / 1000);
                let m = Math.floor(sec / 60).toString().padStart(2,'0');
                let s = (sec % 60).toString().padStart(2,'0');
                document.getElementById('session-clock').innerText = `${m}:${s}`;
            }
        }, 1000);

        async function login() {
            const res = await fetch('/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: document.getElementById('userInput').value, password: document.getElementById('passInput').value})
            });
            if(res.ok) {
                const d = await res.json();
                user = d.user;
                loginTime = Date.now();
                document.getElementById('userTitle').innerText = d.fullname;
                document.getElementById('full-name').innerText = d.fullname;
                document.getElementById('nav-info').classList.remove('hidden');
                renderCourses();
                showTab('course-tab');
            } else { alert("Giriş Başarısız!"); }
        }

        function renderCourses() {
            const courses = """ + str(courses_db) + """;
            const g = document.getElementById('grid');
            g.innerHTML = courses.map(c => `
                <div class="course-card">
                    <span class="tag">${c.cat}</span>
                    <h3 style="margin:10px 0">${c.title}</h3>
                    <p style="font-size:13px; color:#666; margin-bottom:15px">${c.desc}</p>
                    <button onclick="play('${c.title}', '${c.embed_url}')" style="font-size:14px; padding:8px">Dersi Başlat</button>
                </div>
            `).join('');
        }

        function play(title, url) {
            showTab('watch-tab');
            document.getElementById('video-title').innerText = title;
            document.getElementById('player').src = url;
            
            // LOOP Mekanizması
            progressVal = 0;
            if(pInterval) clearInterval(pInterval);
            pInterval = setInterval(() => {
                if(progressVal < 100) {
                    progressVal += 2;
                    document.getElementById('p-bar').style.width = progressVal + "%";
                    document.getElementById('p-text').innerText = "İlerleme: %" + progressVal;
                } else {
                    clearInterval(pInterval);
                    alert("Tebrikler! '" + title + "' dersini tamamladınız.");
                }
            }, 2000);
        }

        function showTab(id) {
            document.querySelectorAll('.card').forEach(c => c.classList.add('hidden'));
            document.getElementById(id).classList.remove('hidden');
            document.getElementById('menuBox').style.display = 'none';
        }

        function toggleMenu() {
            const b = document.getElementById('menuBox');
            b.style.display = (b.style.display === 'block') ? 'none' : 'block';
        }
    </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)