# 💹 NataTrade - Atur Transaksi, Kuasai Masa Depan

**NataTrade** adalah platform hibrida profesional yang dirancang untuk membantu trader mengelola strategi, aset, risiko, dan psikologi secara terpadu. Dengan pendekatan desain **Zen-UI**, platform ini memberikan pengalaman manajemen portofolio yang bersih, presisi, dan modern.

---

## 🚀 4 Pilar Utama (Functional Requirements)

NataTrade dibangun berdasarkan dokumen SKPL yang menitikberatkan pada empat aspek krusial trading:

1.  **Nata Strategi**: Modul evaluasi performa harian yang menghitung laba bersih (**Net P&L**) secara matematis dengan rumus presisi.
    * *Rumus: Net P&L = Gross P&L - (Commission + Funding Fee + Gas Fee)*.
2.  **Nata Aset**: Pengelolaan portofolio jangka panjang menggunakan strategi **Dollar Cost Averaging (DCA)** dan pantauan pergerakan **Net Asset Value (NAV)** secara berkala.
3.  **Nata Risiko**: Mitigasi risiko melalui kalkulator ukuran posisi otomatis untuk menjaga keamanan modal trader.
4.  **Nata Mental**: Audit psikologi trading menggunakan teknologi **AI Vision** dan **NLP** untuk mendeteksi emosi dan tingkat disiplin pengguna.

---

## 🎨 Fitur Visual (Zen-UI)

Platform ini mengedepankan estetika dan kenyamanan pengguna dengan fitur:
* **Glassmorphism Design**: Tampilan transparan yang futuristik dan elegan.
* **Light & Dark Mode**: Perpindahan tema yang halus untuk kenyamanan mata di segala kondisi.
* **Smooth Animations**: Menggunakan library AOS (Animate On Scroll) untuk interaksi elemen yang premium.
* **Inter Font**: Menggunakan tipografi Inter untuk keterbacaan data finansial yang optimal.

---

## 🛠️ Arsitektur Teknologi

NataTrade dikembangkan dengan arsitektur **Django Monolith** untuk menjamin stabilitas dan efisiensi pengiriman data antara server dan tampilan:

* **Backend**: Django (Python) dengan struktur modular di dalam folder `apps/`.
* **Frontend**: Django Templates & Tailwind CSS.
* **Icons**: Lucide Icons.
* **Animations**: AOS (Animate On Scroll).

---