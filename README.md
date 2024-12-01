<div align="center">
  <br />
    <img src="https://drive.google.com/uc?export=view&id=1W2QKxaTIvY17qPVfIZuYhuUroqIhTSP7" alt="LOGO" width="600" />
  <br />
  <br />

  <div>
    <img src="https://img.shields.io/badge/-Nuxt-black?style=for-the-badge&logoColor=white&logo=nuxt.js&color=00C58E" alt="nuxt.js" />
    <img src="https://img.shields.io/badge/-Laravel-black?style=for-the-badge&logoColor=white&logo=laravel&color=FF2D20" alt="laravel" />
    <img src="https://img.shields.io/badge/-Tailwind%20CSS-black?style=for-the-badge&logoColor=white&logo=tailwindcss&color=38BDF8" alt="tailwindcss" />
    <img src="https://img.shields.io/badge/-Twilio-black?style=for-the-badge&logoColor=white&logo=twilio&color=F22F46" alt="twilio" />
  </div>

  <div>
    <img src="https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=3776AB" alt="python" />
    <img src="https://img.shields.io/badge/-Pandas-black?style=for-the-badge&logoColor=white&logo=pandas&color=150458" alt="pandas" />
    <img src="https://img.shields.io/badge/-Scikit--learn-black?style=for-the-badge&logoColor=white&logo=scikit-learn&color=F7931E" alt="scikit-learn" />
    <img src="https://img.shields.io/badge/-Git-black?style=for-the-badge&logoColor=white&logo=git&color=F05032" alt="git" />
  </div>

  <!-- <div>
    <img src="https://img.shields.io/badge/-Composer-black?style=for-the-badge&logoColor=white&logo=composer&color=885630" alt="composer" />
    <img src="https://img.shields.io/badge/-Node.js-black?style=for-the-badge&logoColor=white&logo=node.js&color=339933" alt="node.js" />
  </div> -->

  <h3 align="center">Theft Prediction: A Motion and Gesture Sensor for Identifying Suspicious Activities</h3>

  <div align="center">
    Read 
    <a href="https://drive.google.com/file/d/1mrTZvgCVhBM-IVQL5209tWa12aHNFEAL/view?usp=sharing" target="_blank"><b>documentation</b></a> for more info.
  </div>
</div>

## 📂 Requirements
Make sure you have the following installed on your computer/device:
- ✅ Visual Studio Code ([download here](https://code.visualstudio.com/)).
- ✅ Composer ([download here](https://getcomposer.org/)).
- ✅ Node.js ([download here](https://nodejs.org/en)).
- ✅ XAMPP ([download here](https://www.apachefriends.org/)).
- ✅ Python ([download here](https://www.python.org/downloads/)).
- ✅ Git ([download here](https://git-scm.com/downloads)).

## 👉 Get Started 
Run Project Locally
<details>
<summary><code>1. Open XAMPP Software (MySQL database)</code></summary>

  > Choose these modules to start:
  > 
  > ![xampp](https://drive.google.com/uc?export=view&id=1MaZx_BNTGF825tGRqm4aav16ggfK3gMp)
  > 
  > After that, click **Admin** action in **MySQL** module.
  >
  > If the window appears as shown in the browser, proceed to the next step.
  >
  > ![phpmyadmin](https://drive.google.com/uc?export=view&id=1eWiUBuPAoPiUPQTM8rTGlCcvTxMKCDrZ)
</details>

<details>
<summary><code>2. Clone the repository (Source Code)</code></summary>

  > **In your Desktop, open a command prompt of your choice (git bash, cmd, or any)**
  > ```bash
  > git clone https://github.com/KJLEscoto/Theft-Prediction-System.git
  > cd Theft-Prediction-System
  > ```
  > Open folder to VS Code
  > ```bash
  > code .
  > ```
</details>

<details>
<summary><code>3. Start Flask Server (Camera API)</code></summary>

  > **Open a terminal inside VS Code**
  >
  > Go to ALGORITHM folder
  > ```bash
  > cd algorithm
  > ```
  > Install modules and change the path directory
  > ```bash
  > pip install 'C:\[path-directory]\requirements.txt'
  > ```
  > Load the motions and Start the Server 
  > ```bash
  > python app.py
  > ```
</details>

<details>
<summary><code>4. Install Dependencies for Laravel (Back-end Framework)</code></summary>

  > **Open another terminal inside VS Code**
  >
  > Go to API folder
  > ```bash
  > cd api
  > ```
  > Install modules
  > ```bash
  > composer install
  > ```
  > Copy the .env file
  > ```bash
  > cp .env.example .env
  > ```
  > Generate application key
  > ```bash
  > php artisan key:generate
  > ```
  > **Migrate**, **Seed** all tables and type 'yes' to create **Database**
  > ```bash
  > php artisan migrate --seed
  > ```
  > Run the server
  > ```bash
  > php artisan serve
  > ```
</details>

<details>
<summary><code>5. Install Dependencies for Nuxt (Front-end Framework)</code></summary>

  > **Open another terminal inside VS Code**
  >
  > Go to VIEW folder
  > ```bash
  > cd view
  > ```
  > Install modules
  > ```bash
  > npm install
  > ```
  > Fix compatibilities
  > ```bash
  > npm audit fix
  >```
  > Run the server
  > ```bash
  > npm run dev
  > ```
</details>

Optional:
<details>
<summary><code>Add New Motion (Train Model)</code></summary>

  > **Open a terminal inside VS Code**
  >
  > Go to ALGORITHM folder
  > ```bash
  > cd algorithm
  > ```
  > Run this command and choose how you train a model (via Live, Video, Image)
  > ```bash
  > python train.py
  > ```
</details>

<hr />

<div align="center">
  <h3 align="center">⭐ That's it! The system is now running. Enjoy Dark-mode Theme. ⭐</h3>

  <p>Start Monitoring - <a href="http://localhost:3000/" target="_blank">http://localhost:3000/</a></p>
</div>

![landing-page](https://drive.google.com/uc?export=view&id=17uKbu88C3i3U5fEAU_o6aHezuaVQSuxZ)

<h4>🔑 Login Credentials</h4>
<p>Use these accounts to access the system. <span style="color: #FF0000;"><strong>NOTE:</strong></span> Each role has unique functionalities.</p>

<details>
<summary><code>Client</code></summary>

  > **username**: client
  >
  > **password**: client123
</details>

<details>
<summary><code>Admin</code></summary>

  > **username**: admin
  >
  > **password**: admin123
</details>

<details>
<summary><code>Superadmin</code></summary>

  > **username**: superadmin
  >
  > **password**: superadmin123
</details>

<hr />

## 🧑‍💻 Developers
This project was developed by:
- [Luis Suizo](https://github.com/evander092002)
- [Rochele Cocjin](https://github.com/iochel)
- [Reynaldo Baja Jr.](https://github.com/rey-cloud)
- [Ralph Hernandez](https://github.com/yourboiralph)
- [Kent Joemar Escoto](https://github.com/KJLEscoto)

## ❔ Where to ask for help?
You can send a message to our following socials:

<div>
  <a href="mailto:sti.bscs.thesis@gmail.com" target="_blank">
    <img src="https://img.shields.io/badge/-Email-black?style=for-the-badge&logoColor=white&logo=gmail&color=EA4335" alt="email" />
  </a>

  <a href="https://discord.gg/CBUbE33zPF" target="_blank">
    <img src="https://img.shields.io/badge/-Discord-black?style=for-the-badge&logoColor=white&logo=discord&color=5865F2" alt="discord" />
  </a>
</div>

## ©️ Copyright
Copyright 2024 | Bachelor of Science in Computer Science | Batch 2025 🎓


