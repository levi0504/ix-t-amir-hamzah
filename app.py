from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ===== DATA UTAMA =====
data = {
    "warna": "#88ccee",
    "musik": "",
    "logo": "",
    "siswa": []
}

# ===== HALAMAN UTAMA =====
main_page = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IX T Amir Hamzah</title>
<style>
body{
    margin:0;
    font-family:'Poppins',sans-serif;
    background:{{warna}};
    color:#333;
    overflow-x:hidden;
    transition:background 0.6s ease;
}
header{
    background:rgba(255,255,255,0.8);
    text-align:center;
    padding:20px;
    font-size:26px;
    font-weight:bold;
    box-shadow:0 2px 8px rgba(0,0,0,0.2);
}
footer{
    text-align:center;
    opacity:0.5;
    font-size:12px;
    margin-top:40px;
}
#wrapper{
    min-height:100vh;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
}
.logo{
    display:block;
    margin:30px auto 10px auto;
    width:120px;
    height:120px;
    border-radius:50%;
    object-fit:cover;
    box-shadow:0 4px 10px rgba(0,0,0,0.3);
    animation:fadeIn 1s ease;
}
.welcome{
    text-align:center;
    font-size:22px;
    margin-top:10px;
    animation:fadeIn 1.5s ease;
}
@keyframes fadeIn{
    from{opacity:0;transform:translateY(30px);}
    to{opacity:1;transform:translateY(0);}
}

/* Sidebar */
#sidebar{
    position:fixed;
    left:-260px;
    top:0;
    width:260px;
    height:100%;
    background:#fff;
    box-shadow:2px 0 10px rgba(0,0,0,0.3);
    transition:left 0.4s ease, opacity 0.3s ease;
    opacity:0;
    padding:20px;
    z-index:10;
}
#sidebar.active{
    left:0;
    opacity:1;
}
#sidebar button{
    display:block;
    width:100%;
    margin-bottom:10px;
    padding:10px;
    border:none;
    background:{{warna}};
    color:#fff;
    border-radius:12px;
    font-size:16px;
    cursor:pointer;
    transition:transform 0.2s ease;
}
#sidebar button:hover{transform:scale(1.05);}
#openSidebar{
    position:fixed;
    left:15px;
    top:15px;
    font-size:26px;
    background:rgba(255,255,255,0.7);
    border:none;
    padding:8px 12px;
    border-radius:10px;
    cursor:pointer;
    z-index:20;
}
#closeSidebar{
    background:#ff4d4d;
    margin-bottom:20px;
}
.content{
    padding:20px;
    text-align:center;
    transition:opacity 0.5s ease;
}
.bubble{
    display:inline-block;
    background:rgba(255,255,255,0.9);
    border-radius:20px;
    padding:15px;
    margin:10px;
    width:250px;
    box-shadow:0 4px 8px rgba(0,0,0,0.2);
    text-align:left;
}
.bubble h3{margin-top:0;font-size:18px;}
</style>
</head>
<body>
{% if musik %}
<audio autoplay loop id="bgMusic"><source src="{{musik}}" type="audio/mpeg"></audio>
{% endif %}
<div id="wrapper">
    <div>
        <button id="openSidebar">☰</button>
        <div id="sidebar">
            <button id="closeSidebar">✖ Tutup</button>
            <button onclick="showCategory('siswa')">👨‍🎓 Siswa</button>
            <button onclick="showCategory('jadwal')">📅 Jadwal Pelajaran</button>
            <button onclick="showCategory('piket')">🧹 Jadwal Piket</button>
            <button onclick="showCategory('struktur')">🏫 Struktur Kelas</button>
            <button onclick="window.location.href='/admin'">⚙️ Admin Control</button>
        </div>

        <header>IX T AMIR HAMZAH</header>
        {% if logo %}
        <img src="{{logo}}" class="logo">
        {% endif %}
        <div class="content" id="mainContent">
            <div class="welcome">
                <p>🌟 Selamat Datang di Website Kelas 🌟</p>
                <p><b>IX T Amir Hamzah</b></p>
            </div>
        </div>
    </div>
    <footer>✨ Dibuat oleh Siswa Kelas IX T Amir Hamzah yang disempurnakan oleh AI ✨</footer>
</div>

<script>
const sidebar=document.getElementById("sidebar");
const openBtn=document.getElementById("openSidebar");
const closeBtn=document.getElementById("closeSidebar");
const content=document.getElementById("mainContent");

openBtn.onclick=()=>{
    sidebar.classList.add("active");
    content.style.opacity="0.3";
};
closeBtn.onclick=()=>{
    sidebar.classList.remove("active");
    content.style.opacity="1";
};

function showCategory(cat){
    let html="";
    if(cat==="siswa"){
        fetch('/get_siswa')
        .then(r=>r.json())
        .then(siswa=>{
            html="<h2>👨‍🎓 Daftar Siswa</h2>";
            if(siswa.length===0){html+="<p>Belum ada data siswa.</p>";}
            siswa.forEach(s=>{
                if(s.info_mode==="private"){
                    html+=`<div class='bubble'><h3>${s.nama}</h3><p><b>Jabatan:</b> ${s.jabatan}</p><p>🔒 Maaf, Informasi Tentang Siswa Ini Private</p></div>`;
                }else{
                    html+=`<div class='bubble'>
                        ${s.foto?`<img src='${s.foto}' width='100%' style='border-radius:15px;'>`:""}
                        <h3>${s.nama}</h3>
                        <p><b>Jabatan:</b> ${s.jabatan}</p>
                        <p>${s.informasi}</p>
                    </div>`;
                }
            });
            content.style.opacity="0";
            setTimeout(()=>{
                content.innerHTML=html;
                content.style.opacity="1";
            },400);
            sidebar.classList.remove("active");
        });
    }else{
        const titles={
            jadwal:"📅 Jadwal Pelajaran",
            piket:"🧹 Jadwal Piket",
            struktur:"🏫 Struktur Kelas"
        };
        html=`<h2>${titles[cat]}</h2><p>Segera diisi oleh admin.</p>`;
        content.style.opacity="0";
        setTimeout(()=>{
            content.innerHTML=html;
            content.style.opacity="1";
        },400);
        sidebar.classList.remove("active");
    }
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(main_page,
        warna=data["warna"], musik=data["musik"], logo=data["logo"])

@app.route('/get_siswa')
def get_siswa():
    return jsonify(data["siswa"])
  # ====== ADMIN PANEL (FIX SCROLL) ======
admin_page = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin Control Panel</title>
<style>
body{
    font-family:'Poppins',sans-serif;
    margin:0;
    background:linear-gradient(135deg,#7ad7f0,#d3b7ff);
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    overflow:hidden;
}
.card{
    background:white;
    border-radius:20px;
    padding:30px;
    width:320px;
    box-shadow:0 8px 20px rgba(0,0,0,0.2);
    animation:fade 0.6s ease;
}
@keyframes fade{
    from{opacity:0;transform:scale(0.9);}
    to{opacity:1;transform:scale(1);}
}
input,select,textarea{
    width:100%;
    margin:6px 0;
    padding:8px;
    border:1px solid #ccc;
    border-radius:8px;
}
button{
    background:#6a5acd;
    color:white;
    padding:10px;
    border:none;
    border-radius:10px;
    width:100%;
    margin-top:8px;
    font-size:15px;
    cursor:pointer;
    transition:0.3s;
}
button:hover{background:#8b7bff;}
#login{
    text-align:center;
}
#panel{
    display:none;
    max-height:90vh;
    overflow-y:auto;
    scrollbar-width:none;
    -ms-overflow-style:none;
}
#panel::-webkit-scrollbar{display:none;}
#colorPicker{
    width:100%;
    height:40px;
    border-radius:10px;
    border:none;
}
.siswa-item{
    background:#f7f7f7;
    padding:10px;
    border-radius:10px;
    margin-top:5px;
}
.footerNote{
    font-size:11px;
    text-align:center;
    opacity:0.6;
    margin-top:10px;
}
</style>
</head>
<body>
<div class="card" id="login">
    <h2>🎮 Login Admin</h2>
    <input type="password" id="password" placeholder="Masukkan Password">
    <button onclick="login()">Masuk</button>
</div>

<div class="card" id="panel">
    <h2>⚙️ Admin Control Panel</h2>
    <h3>🎨 Warna Website</h3>
    <input type="color" id="colorPicker" value="{{warna}}">
    <button onclick="setColor()">Lanjutkan</button>

    <h3>🎵 Musik Latar</h3>
    <input id="musicLink" placeholder="Masukkan link musik">
    <button onclick="setMusic()">Simpan Musik</button>

    <h3>🖼️ Logo Kelas</h3>
    <input id="logoLink" placeholder="Masukkan link logo (opsional)">
    <button onclick="setLogo()">Simpan Logo</button>

    <h3>👨‍🎓 Tambah/Edit Siswa</h3>
    <input id="foto" placeholder="Link Foto (opsional)">
    <input id="nama" placeholder="Nama Siswa">
    <input id="jabatan" placeholder="Jabatan">
    <textarea id="informasi" placeholder="Informasi Siswa" style="border-radius:10px;"></textarea>
    <select id="mode">
        <option value="public">Public</option>
        <option value="private">Private</option>
    </select>
    <button onclick="tambahSiswa()">Tambah / Simpan</button>

    <div id="dataSiswa">
        <h3>📜 Data Semua Siswa</h3>
        <div id="listSiswa"></div>
    </div>

    <button style="background:#ff5555" onclick="logout()">Keluar</button>
    <div class="footerNote">✨ Dibuat oleh Siswa IX T Amir Hamzah & AI ✨</div>
</div>

<script>
function login(){
    const pass=document.getElementById("password").value;
    if(pass==="admin123"){
        document.getElementById("login").style.display="none";
        document.getElementById("panel").style.display="block";
        loadSiswa();
        window.scrollTo(0,0);
    }else{
        alert("Password salah!");
    }
}

function logout(){
    document.getElementById("panel").style.display="none";
    document.getElementById("login").style.display="block";
    window.scrollTo(0,0);
}

function setColor(){
    const warna=document.getElementById("colorPicker").value;
    fetch('/set_warna',{
        method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({warna})
    }).then(()=>alert("Warna berhasil diubah!"));
}

function setMusic(){
    const musik=document.getElementById("musicLink").value;
    fetch('/set_musik',{
        method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({musik})
    }).then(()=>alert("Musik disimpan!"));
}

function setLogo(){
    const logo=document.getElementById("logoLink").value;
    fetch('/set_logo',{
        method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({logo})
    }).then(()=>alert("Logo diperbarui!"));
}

function tambahSiswa(){
    const s={
        foto:document.getElementById("foto").value,
        nama:document.getElementById("nama").value,
        jabatan:document.getElementById("jabatan").value,
        informasi:document.getElementById("informasi").value,
        info_mode:document.getElementById("mode").value
    };
    fetch('/tambah_siswa',{
        method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify(s)
    }).then(r=>r.json())
      .then(()=>{alert("Data siswa disimpan!");loadSiswa();});
}

function loadSiswa(){
    fetch('/get_siswa').then(r=>r.json()).then(list=>{
        const div=document.getElementById("listSiswa");
        div.innerHTML="";
        list.forEach((s,i)=>{
            div.innerHTML+=`
            <div class='siswa-item'>
                <b>${s.nama}</b> - ${s.jabatan} (${s.info_mode})
                <br>
                <button onclick='hapusSiswa(${i})' style='background:#ff7777;margin-top:5px;'>Hapus</button>
            </div>`;
        });
    });
}

function hapusSiswa(i){
    fetch('/hapus_siswa',{
        method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({index:i})
    }).then(()=>{alert("Dihapus!");loadSiswa();});
}
</script>
</body>
</html>
"""

@app.route('/admin')
def admin():
    return render_template_string(admin_page, warna=data["warna"])

@app.route('/set_warna', methods=['POST'])
def set_warna():
    data["warna"]=request.json["warna"]
    return jsonify(success=True)

@app.route('/set_musik', methods=['POST'])
def set_musik():
    data["musik"]=request.json["musik"]
    return jsonify(success=True)

@app.route('/set_logo', methods=['POST'])
def set_logo():
    data["logo"]=request.json["logo"]
    return jsonify(success=True)

@app.route('/tambah_siswa', methods=['POST'])
def tambah_siswa():
    s=request.json
    data["siswa"].append(s)
    return jsonify(success=True)

@app.route('/hapus_siswa', methods=['POST'])
def hapus_siswa():
    idx=request.json["index"]
    if 0<=idx<len(data["siswa"]):
        del data["siswa"][idx]
    return jsonify(success=True)

if __name__=="__main__":
    app.run(debug=True)
