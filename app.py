from flask import Flask, render_template_string, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "rahasia123"

# ====== Data Awal ======
data = {
    "warna_website": "#6C63FF",
    "music": "",
    "logo": "https://files.catbox.moe/qeim9n.jpg",
    "siswa": []
}

def save_data():
    with open("data.json", "w") as f:
        json.dump(data, f)

def load_data():
    global data
    try:
        with open("data.json") as f:
            data.update(json.load(f))
    except:
        pass

load_data()

# ====== TEMPLATE HTML ======
template = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IX T Amir Hamzah</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Poppins',sans-serif;}
body{
  background-color: {{ warna }};
  transition: background-color 1s ease;
  overflow-x:hidden;
}
header{
  text-align:center;
  padding:20px;
  color:white;
  font-size:25px;
  font-weight:bold;
}
.container{
  padding:20px;
  display:flex;
  flex-wrap:wrap;
  gap:15px;
  justify-content:center;
}
.card{
  border-radius:15px;
  padding:15px;
  width:300px;
  word-wrap:break-word;
  white-space:pre-wrap;
  transition:transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow:0 3px 6px rgba(0,0,0,0.2);
}
.card:hover{transform:translateY(-5px);box-shadow:0 5px 10px rgba(0,0,0,0.3);}
footer{
  position:fixed;
  bottom:5px;
  width:100%;
  text-align:center;
  font-size:12px;
  opacity:0.6;
  color:white;
}
button{cursor:pointer;padding:8px 12px;border:none;border-radius:8px;}
input,select,textarea{padding:6px;width:100%;margin-bottom:10px;border-radius:8px;border:1px solid #ccc;}

.login-container{
  display:flex;justify-content:center;align-items:center;height:100vh;flex-direction:column;
  background:linear-gradient(135deg,#6C63FF,#3B3B98);
  color:white;
  animation:fadeIn 1s ease;
}
.login-container input{width:200px;padding:10px;border:none;border-radius:10px;margin-top:10px;}
.login-container button{margin-top:10px;background:white;color:#3B3B98;font-weight:bold;border:none;border-radius:10px;padding:10px 20px;}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
h3{margin-top:25px;color:#333;}
.admin-box{background:white;padding:20px;border-radius:20px;margin:15px 0;box-shadow:0 3px 6px rgba(0,0,0,0.15);}
</style>
</head>
<body>

{% if page == "login" %}
  <div class="login-container">
    <h2>🔐 Login Admin</h2>
    <form method="POST" action="/login">
      <input type="password" name="password" placeholder="Masukkan Password" required><br>
      <button type="submit">Masuk</button>
    </form>
  </div>

{% elif page == "admin" %}
  <header>⚙️ Admin Control Panel</header>
  <div style="text-align:center;margin:10px;">
    <a href="/logout"><button style="background:red;color:white;">Logout</button></a>
  </div>

  <div style="padding:20px;">
    <div class="admin-box">
      <h3>🎨 Warna Website</h3>
      <form method="POST" action="/set_warna">
        <input type="color" name="warna" value="{{ warna }}">
        <button type="submit">Simpan</button>
      </form>
    </div>

    <div class="admin-box">
      <h3>🖼️ Logo Kelas</h3>
      <form method="POST" action="/set_logo">
        <input type="text" name="logo" value="{{ logo }}" placeholder="Link logo">
        <button type="submit">Simpan</button>
      </form>
      <img src="{{ logo }}" alt="Logo" style="width:100px;margin-top:10px;border-radius:50%;">
    </div>

    <div class="admin-box">
      <h3>🎵 Musik</h3>
      <form method="POST" action="/set_music">
        <input type="text" name="music" value="{{ music }}" placeholder="Link file .mp3">
        <button type="submit">Mulai</button>
        <a href="/stop_music"><button type="button">Stop</button></a>
      </form>
    </div>

    <div class="admin-box">
      <h3>👩‍🎓 Data Siswa</h3>
      <form method="POST" action="/add_siswa">
        <input type="text" name="nama" placeholder="Nama siswa" required>
        <textarea name="info" placeholder="Informasi" required></textarea>
        <select name="mode">
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
        <label>Pilih warna kotak:</label>
        <input type="color" name="warna_kotak" value="#ffffff">
        <button type="submit">Tambah</button>
      </form>

      {% for s in siswa %}
        <div style="background:{{ s['warna_kotak'] }};padding:10px;border-radius:10px;margin:10px 0;">
          <b>{{ s['nama'] }}</b><br>
          Mode: {{ s['mode'] }}<br>
          <form method="POST" action="/hapus_siswa/{{ loop.index0 }}" style="margin-top:5px;">
            <button type="submit" style="background:red;color:white;">Hapus</button>
          </form>
        </div>
      {% endfor %}
    </div>
  </div>

{% else %}
  <header>IX T Amir Hamzah</header>
  <div class="container">
    {% for s in siswa %}
      {% if s['mode'] == 'public' %}
        <div class="card" style="background:{{ s['warna_kotak'] }}">
          <b>{{ s['nama'] }}</b><br>
          {{ s['info'] }}
        </div>
      {% else %}
        <div class="card" style="background:{{ s['warna_kotak'] }}">
          <b>{{ s['nama'] }}</b><br>
          <i>Maaf, informasi tentang siswa ini di-private.</i>
        </div>
      {% endif %}
    {% endfor %}
  </div>
  <footer>Dibuat Oleh Siswa Kelas IX T Amir Hamzah Yang Disempurnakan Oleh AI</footer>
  {% if music %}
    <audio autoplay loop>
      <source src="{{ music }}" type="audio/mpeg">
    </audio>
  {% endif %}
{% endif %}
</body>
</html>
"""

# ====== ROUTES ======
@app.route("/")
def index():
    return render_template_string(template, page="public", siswa=data["siswa"], warna=data["warna_website"], music=data["music"], logo=data["logo"])

@app.route("/admin")
def admin_panel():
    if not session.get("admin"):
        return redirect("/login")
    return render_template_string(template, page="admin", siswa=data["siswa"], warna=data["warna_website"], music=data["music"], logo=data["logo"])

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/admin")
    return render_template_string(template, page="login", siswa=[], warna=data["warna_website"], music="", logo=data["logo"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/set_warna", methods=["POST"])
def set_warna():
    data["warna_website"] = request.form["warna"]
    save_data()
    return redirect("/admin")

@app.route("/set_logo", methods=["POST"])
def set_logo():
    data["logo"] = request.form["logo"]
    save_data()
    return redirect("/admin")

@app.route("/set_music", methods=["POST"])
def set_music():
    data["music"] = request.form["music"]
    save_data()
    return redirect("/admin")

@app.route("/stop_music")
def stop_music():
    data["music"] = ""
    save_data()
    return redirect("/admin")

@app.route("/add_siswa", methods=["POST"])
def add_siswa():
    s = {
        "nama": request.form["nama"],
        "info": request.form["info"],
        "mode": request.form["mode"],
        "warna_kotak": request.form["warna_kotak"]
    }
    data["siswa"].append(s)
    save_data()
    return redirect("/admin")

@app.route("/hapus_siswa/<int:index>", methods=["POST"])
def hapus_siswa(index):
    if 0 <= index < len(data["siswa"]):
        data["siswa"].pop(index)
        save_data()
    return redirect("/admin")

import os

if name == "main":
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
