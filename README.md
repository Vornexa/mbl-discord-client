
# MybestLink Discord Client

Mbl-client adalah sebuah aplikasi Discord Bot berbasis Python yang terintegrasi dengan MybestLink API.
Bot ini dibuat sebagai contoh implementasi penggunaan proxy API dari Mybest App menuju MybestLinked.

Project ini bersifat open-source dan ditujukan sebagai sarana pembelajaran, bukan untuk tujuan komersial ataupun diperjualbelikan.


## Fitur Utama

- Integrasi dengan MybestLink API untuk menampilkan data atau layanan terkait.
- Command berbasis prefix maupun slash command (bisa disesuaikan).
- Struktur project modular agar mudah dipelajari dan dikembangkan.
- Dukungan event handler untuk berbagai aktivitas di Discord.

## Reminder
- Project ini tidak ditujukan untuk penggunaan komersial, melainkan:
- Sebagai contoh implementasi bot Discord dengan integrasi API.
- Sebagai bagian dari portofolio open-source untuk CV atau profil GitHub.
- Sebagai sarana belajar pengembangan aplikasi berbasis bot.
## Deployment

To deploy this project run

```bash
git clone https://github.com/username/mybestlink-client.git
cd mybestlink-client
```

virtual enviroment (optional)
```
python -m venv venv
source venv/bin/activate   # Linux/MacOS
venv\Scripts\activate      # Windows
```

Install Dependencies
```
pip install -r requirements.txt
```

Enviroment
```ini
CLIENT_PREFIX=
CLIENT_DC_TOKEN=
CLIENT_TOKEN=
CLIENT_BOT_NAME=
CLIENT_BOT_STATUS=
```


