// Ця функція автоматично додає чат на кожну сторінку, де підключено цей скрипт
(function createBillInterface() {
    const billHTML = `
    <div id="bill-chat-container">
        <div id="chat-window">
            <div class="chat-header">УГОДА З ДЕМОНОМ</div>
            <div id="bill-messages">
                <p class="bill-txt">Біл: Ха-ха! Ти думав, що я зник? Я стежу за тобою на кожній сторінці цього сайту!</p>
            </div>
            <div class="chat-input-group">
                <input type="text" id="bill-input" placeholder="Пиши сюди...">
                <button id="send-btn">👁️</button>
            </div>
        </div>
        <div id="bill-eye-trigger" title="Натисни, щоб укласти угоду">
            <div class="pupil"></div>
        </div>
    </div>`;

    // Додаємо HTML в кінець body
    document.body.insertAdjacentHTML('beforeend', billHTML);

    // Словник відповідей Білла
    const responses = {
        "привіт": ["О, ще один смертний! Привіт!", "Хочеш укласти угоду, мішок з м'ясом?", "Я бачу тебе..."],
        "теорії": ["Твої теорії кумедні. Але правда набагато страшніша!", "Аксалотль? Не згадуй це ім'я в моїй присутності!", "Я живий, поки ви про мене пам'ятаєте!"],
        "факти": ["Я спалив свій світ, і твій наступний! Це мій улюблений факт.", "Форд думав, що він головний. Як наївно!"],
        "елфійськ": ["Елфійська Імперія? Твій мозок розплавиться від істини!", "Я знаю її назву, але вона зашифрована в твоїх снах."],
        "weird": ["ДИВНОГЕДОН ПОЧИНАЄТЬСЯ!", "ЧАС ЗМІНИТИ ПОРЯДОК РЕЧЕЙ!"],
        "default": ["Реальність — ілюзія! Всесвіт — голограма! Купуй золото! Бувай!", "Цікава думка... для істоти з 3D-мізками.", "Може мені перетворити твої пальці на сосиски? Ха-ха!"]
    };

    const windowElement = document.getElementById('chat-window');
    const trigger = document.getElementById('bill-eye-trigger');
    const input = document.getElementById('bill-input');
    const btn = document.getElementById('send-btn');
    const msgBox = document.getElementById('bill-messages');

    // Відкрити/закрити чат
    trigger.onclick = () => windowElement.classList.toggle('active');

    // Логіка відправки
    function sendMessage() {
        const text = input.value.toLowerCase().trim();
        if (!text) return;

        // Відображаємо текст користувача
        msgBox.innerHTML += `<p class="user-txt">Ти: ${input.value}</p>`;
        
        let reply = responses.default[Math.floor(Math.random() * responses.default.length)];

        // Перевірка на ключові слова
        if (text.includes("привіт") || text.includes("здрав")) reply = responses.привіт[Math.floor(Math.random() * 3)];
        else if (text.includes("теорі")) reply = responses.теорії[Math.floor(Math.random() * 3)];
        else if (text.includes("факт")) reply = responses.факти[Math.floor(Math.random() * 2)];
        else if (text.includes("елфій") || text.includes("імпері")) reply = responses.елфійськ[Math.floor(Math.random() * 2)];
        else if (text.includes("weird")) {
            reply = responses.weird[Math.floor(Math.random() * 2)];
            document.body.style.filter = "hue-rotate(180deg) contrast(1.5)"; // Ефект Дивногедону!
            setTimeout(() => document.body.style.filter = "none", 3000);
        }

        // Білл відповідає з невеликою затримкою
        setTimeout(() => {
            msgBox.innerHTML += `<p class="bill-txt"><b>Біл:</b> ${reply}</p>`;
            msgBox.scrollTop = msgBox.scrollHeight;
        }, 600);

        input.value = "";
    }

    btn.onclick = sendMessage;
    input.onkeypress = (e) => { if (e.key === 'Enter') sendMessage(); };
})();
// --- КОД ДЛЯ ГОДИННИКА ---
function clock() {
    const clockElement = document.getElementById('bill-clock');
    if (!clockElement) return; // Перевірка, чи є годинник на цій сторінці

    const now = new Date(); // Беремо час із системи
    const timeString = now.toLocaleTimeString(); // Форматуємо (ГГ:ХВ:СС)
    clockElement.innerText = timeString; // Записуємо в HTML
}

// Оновлювати кожну секунду (1000 мілісекунд)
setInterval(clock, 1000);

// Запустити відразу при завантаженні
clock();
function initBillGlitch() {
    const symbols = "!@#$%^&*()_+=-[]{}|;:,.<>?/¿¡†‡ΔΣТ∞☠👁️🔱";
    
    const hp = document.getElementById('glitch-hp');
    const type = document.getElementById('glitch-type');

    if (!hp || !type) return;

    // Зміна символів для HP (тепер виводить довгий ряд)
    setInterval(() => {
        let result = "";
        // Збільшуємо кількість ітерацій до 6-8, щоб рядок був довгим
        for (let i = 0; i < 7; i++) {
            result += symbols[Math.floor(Math.random() * symbols.length)];
        }
        hp.innerText = result;
    }, 120);

    // Зміна символів для ТИПУ (збільшуємо з 3 до 6-8)
    setInterval(() => {
        let result = "";
        for (let i = 0; i < 8; i++) {
            result += symbols[Math.floor(Math.random() * symbols.length)];
        }
        type.innerText = result;
    }, 150);
}
// Запускаємо функцію після завантаження сторінки
initBillGlitch();