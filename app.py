from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = "rahasia_login_admin"
DATA_FILE = "data.json"

# ===== LOAD & SAVE =====
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "warna": "#74b9ff",
        "kotak_warna": "#ffffff",
        "musik": "",
        "logo": "",
        "siswa": [],
        "kegiatan": []
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# ====== LOGIN PAGE ======
login_page = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login Admin</title>
<style>
body{margin:0;font-family:'Poppins',sans-serif;background:#74b9ff;display:flex;justify-content:center;align-items:center;height:100vh;}
.card{background:#ffffffee;padding:35px;border-radius:18px;box-shadow:0 4px 15px rgba(0,0,0,0.3);width:320px;text-align:center;}
input{width:100%;padding:12px;margin-top:15px;border-radius:10px;border:1px solid #ccc;font-size:16px;}
button{width:100%;margin-top:15px;padding:12px;font-size:17px;border:none;border-radius:10px;background:#6a5acd;color:white;font-weight:bold;cursor:pointer;}
</style>
</head>
<body>
<div class="card">
<h2>🔐 Login Admin</h2>
<input type="password" id="pass" placeholder="Masukkan Password">
<button onclick="login()">Masuk</button>
<p id="msg" style="color:red;margin-top:10px;"></p>
</div>
<script>
function login(){
    fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({password:document.getElementById('pass').value})})
    .then(r=>r.json()).then(d=>{if(d.success){window.location='/admin';}else{msg.innerText='Password salah!';}});
}
</script>
</body></html>
"""

# ====== UI PUBLIK ======
public_ui = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IX T Amir Hamzah</title>
<style>
body{margin:0;font-family:'Poppins',sans-serif;background:{{warna}};transition:background 0.6s ease;}
header{background:rgba(255,255,255,0.8);text-align:center;padding:20px;font-size:26px;font-weight:bold;box-shadow:0 2px 8px rgba(0,0,0,0.2);}
#sidebar{position:fixed;left:-260px;top:0;width:260px;height:100%;background:#fff;box-shadow:2px 0 10px rgba(0,0,0,0.3);
transition:left 0.4s ease,opacity 0.3s ease;opacity:0;padding:20px;z-index:10;}
#sidebar.active{left:0;opacity:1;}
#sidebar button{display:block;width:100%;margin-bottom:10px;padding:10px;border:none;background:{{warna}};color:#fff;
border-radius:12px;font-size:16px;cursor:pointer;}
#openSidebar{position:fixed;left:15px;top:15px;font-size:26px;background:rgba(255,255,255,0.7);border:none;
padding:8px 12px;border-radius:10px;cursor:pointer;z-index:20;}
.bubble{display:inline-block;background:{{kotak_warna}};border-radius:20px;padding:15px;margin:10px;
width:260px;box-shadow:0 4px 8px rgba(0,0,0,0.2);text-align:left;word-wrap:break-word;}
.detail-modal{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);
display:none;justify-content:center;align-items:center;z-index:30;}
.detail-content{background:#fff;padding:20px;border-radius:15px;max-width:90%;max-height:90%;overflow:auto;text-align:center;}
.detail-content img{max-width:100%;border-radius:10px;margin-bottom:10px;}
button.close{background:#ff4d4d;color:white;border:none;padding:10px 15px;border-radius:10px;cursor:pointer;}
</style>
</head>
<body>
{% if musik %}<audio autoplay loop><source src="{{musik}}" type="audio/mpeg"></audio>{% endif %}
<button id="openSidebar">☰</button>
<div id="sidebar">
    <button onclick="showCategory('siswa')">👨‍🎓 Siswa</button>
    <button onclick="showCategory('kegiatan')">📸 Kegiatan</button>
    <button onclick="showCategory('jadwal')">📅 Jadwal</button>
    <button onclick="showCategory('piket')">🧹 Piket</button>
    <button onclick="showCategory('struktur')">🏫 Struktur</button>
    <button onclick="window.location.href='/login'">⚙️ Admin</button>
</div>

<header>IX T AMIR HAMZAH</header>
{% if logo %}<img src="{{logo}}" style="display:block;margin:20px auto;width:120px;height:120px;border-radius:50%;object-fit:cover;">{% endif %}
<div id="content" style="padding:20px;text-align:center;">
    <h2>🌟 Selamat Datang di Website IX T Amir Hamzah 🌟</h2>
</div>

<div class="detail-modal" id="modal">
    <div class="detail-content" id="modalContent"></div>
</div>

<script>
const sidebar=document.getElementById('sidebar'),content=document.getElementById('content'),
modal=document.getElementById('modal'),modalContent=document.getElementById('modalContent');
document.getElementById('openSidebar').onclick=()=>sidebar.classList.toggle('active');
function showCategory(cat){
    sidebar.classList.remove('active');
    if(cat==='siswa'){
        fetch('/get_siswa').then(r=>r.json()).then(s=>{
            let h="<h2>👨‍🎓 Daftar Murid</h2>";
            s.forEach(a=>h+=`<div class='bubble'><b>${a.nama}</b><br>${a.info}</div>`);
            content.innerHTML=h||"<p>Belum ada data.</p>";
        });
    }else if(cat==='kegiatan'){
        fetch('/get_kegiatan').then(r=>r.json()).then(k=>{
            let h="<h2>📸 Kegiatan IX T Amir Hamzah</h2>";
            k.forEach((x,i)=>{
                h+=`<div class='bubble' onclick='showDetail(${i})'>
                    ${x.foto?`<img src='${x.foto}' style='width:100%;border-radius:10px;'>`:""}
                    <h3>${x.tentang}</h3></div>`;
            });
            content.innerHTML=h||"<p>Belum ada kegiatan.</p>";
        });
    }else{
        const title={jadwal:"📅 Jadwal Pelajaran",piket:"🧹 Jadwal Piket",struktur:"🏫 Struktur Kelas"};
        content.innerHTML=`<h2>${title[cat]}</h2><p>Segera diisi oleh admin.</p>`;
    }
}
function showDetail(i){
    fetch('/get_kegiatan').then(r=>r.json()).then(k=>{
        let d=k[i];if(!d)return;
        modal.style.display='flex';
        modalContent.innerHTML=`<h2>${d.tentang}</h2>
        ${d.foto2?`<img src='${d.foto2}'>`:""}
        <p>${d.isi||""}</p>
        <button class='close' onclick='modal.style.display="none"'>Tutup</button>`;
    });
}
window.onclick=e=>{if(e.target===modal)modal.style.display='none';};
</script>
</body></html>
"""

# ===== ADMIN PANEL =====
admin_panel = """
<!DOCTYPE html>
<html lang="id">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Admin Panel</title>
<style>
body{font-family:'Poppins',sans-serif;background:{{warna}};margin:0;}
.container{max-width:700px;margin:40px auto;background:#ffffffee;padding:25px;border-radius:20px;}
input,textarea{width:100%;padding:10px;margin:6px 0;border-radius:10px;border:1px solid #ccc;}
button{padding:10px 15px;border:none;border-radius:10px;background:#0984e3;color:white;cursor:pointer;margin-top:5px;}
.kotak{background:{{kotak_warna}};padding:10px;border-radius:10px;margin:5px 0;}
</style></head><body>
<div class="container">
<h1>⚙️ Admin Panel</h1>

<h3>🎨 Warna Tema</h3>
<input type="color" id="warna" value="{{warna}}">
<input type="color" id="kotak" value="{{kotak_warna}}">
<button onclick="setWarna()">Simpan Warna</button>

<h3>🎵 Musik</h3>
<input type="text" id="musik" value="{{musik}}" placeholder="URL musik (mp3)">
<button onclick="setMusik()">Simpan Musik</button>

<h3>🖼️ Logo</h3>
<input type="text" id="logo" value="{{logo}}" placeholder="URL logo">
<button onclick="setLogo()">Simpan Logo</button>

<hr>
<h3>👨‍🎓 Tambah Siswa</h3>
<input type="text" id="nama" placeholder="Nama">
<textarea id="info" placeholder="Informasi"></textarea>
<button onclick="tambahSiswa()">Tambah</button>
<div id="listsiswa"></div>

<hr>
<h3>📸 Tambah Kegiatan</h3>
<input type="text" id="foto" placeholder="Foto (opsional)">
<input type="text" id="tentang" placeholder="Judul / Tentang">
<input type="text" id="foto2" placeholder="Foto Kedua (opsional)">
<textarea id="isi" placeholder="Isi kegiatan"></textarea>
<button onclick="tambahKegiatan()">Tambah Kegiatan</button>
<div id="listkegiatan"></div>

</div>
<script>
function loadSiswa(){
 fetch('/get_siswa').then(r=>r.json()).then(d=>{
  let h="";d.forEach((s,i)=>h+=`<div class='kotak'><b>${s.nama}</b><br>${s.info}<br><button onclick='hapusS(${i})'>Hapus</button></div>`);
  listsiswa.innerHTML=h||"<p>Belum ada siswa.</p>";
 });}
function loadKegiatan(){
 fetch('/get_kegiatan').then(r=>r.json()).then(d=>{
  let h="";d.forEach((k,i)=>h+=`<div class='kotak'><b>${k.tentang}</b><br><button onclick='hapusK(${i})'>Hapus</button></div>`);
  listkegiatan.innerHTML=h||"<p>Belum ada kegiatan.</p>";
 });}
function tambahSiswa(){
 fetch('/tambah_siswa',{method:'POST',headers:{'Content-Type':'application/json'},
 body:JSON.stringify({nama:nama.value,info:info.value})}).then(()=>loadSiswa());
}
function hapusS(i){fetch('/hapus_siswa',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({index:i})}).then(()=>loadSiswa());}
function tambahKegiatan(){
 fetch('/tambah_kegiatan',{method:'POST',headers:{'Content-Type':'application/json'},
 body:JSON.stringify({foto:foto.value,tentang:tentang.value,foto2:foto2.value,isi:isi.value})}).then(()=>loadKegiatan());
}
function hapusK(i){fetch('/hapus_kegiatan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({index:i})}).then(()=>loadKegiatan());}
function setWarna(){fetch('/set_warna',{method:'POST',headers:{'Content-Type':'application/json'},
 body:JSON.stringify({warna:warna.value,kotak:kotak.value})});}
function setMusik(){fetch('/set_musik',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({musik:musik.value})});}
function setLogo(){fetch('/set_logo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({logo:logo.value})});}
loadSiswa();loadKegiatan();
</script></body></html>
"""

# ===== ROUTES =====
@app.route("/")
def home():
    return render_template_string(public_ui, warna=data["warna"], kotak_warna=data["kotak_warna"], musik=data["musik"], logo=data["logo"])

@app.route("/login")
def login_page_view():
    return render_template_string(login_page)

@app.route("/login", methods=["POST"])
def login_post():
    if request.json.get("password") == "admin123":
        session["admin"] = True
        return jsonify(success=True)
    return jsonify(success=False)

@app.route("/admin")
def admin_panel_page():
    if not session.get("admin"): return redirect(url_for("login_page_view"))
    return render_template_string(admin_panel, warna=data["warna"], kotak_warna=data["kotak_warna"], musik=data["musik"], logo=data["logo"])

# ===== DATA API =====
@app.route("/get_siswa")
def get_siswa(): return jsonify(data["siswa"])
@app.route("/tambah_siswa",methods=["POST"])
def tambah_siswa():
    data["siswa"].append(request.json);save_data(data);return jsonify(success=True)
@app.route("/hapus_siswa",methods=["POST"])
def hapus_siswa():
    i=request.json["index"]
    if 0<=i<len(data["siswa"]): del data["siswa"][i];save_data(data)
    return jsonify(success=True)

@app.route("/get_kegiatan")
def get_kegiatan(): return jsonify(data["kegiatan"])
@app.route("/tambah_kegiatan",methods=["POST"])
def tambah_kegiatan():
    data["kegiatan"].append(request.json);save_data(data);return jsonify(success=True)
@app.route("/hapus_kegiatan",methods=["POST"])
def hapus_kegiatan():
    i=request.json["index"]
    if 0<=i<len(data["kegiatan"]): del data["kegiatan"][i];save_data(data)
    return jsonify(success=True)

@app.route("/set_warna",methods=["POST"])
def set_warna():
    j=request.json;data["warna"]=j["warna"];data["kotak_warna"]=j["kotak"];save_data(data);return jsonify(success=True)
@app.route("/set_musik",methods=["POST"])
def set_musik():
    data["musik"]=request.json["musik"];save_data(data);return jsonify(success=True)
@app.route("/set_logo",methods=["POST"])
def set_logo():
    data["logo"]=request.json["logo"];save_data(data);return jsonify(success=True)

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
