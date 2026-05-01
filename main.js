const { exec } = require('child_process');
const path = require('path');

// 1. Налаштування
// Додали --server.headless true, щоб Білл не відкривав зайву вкладку сам по собі
const pythonCommand = 'streamlit run app.py --server.headless true'; 
const htmlFile = 'головна.html';             // Твій головний файл

console.log('------------------------------------------');
console.log('👁️  БІЛЛ ШИФР: ПРОЦЕС ОЖИВЛЕННЯ ЗАПУЩЕНО');
console.log('------------------------------------------');

// 2. Запускаємо Python-сервер у новому окремому вікні
console.log('🚀 Запускаю сервер Білла...');
exec(`start cmd /k "${pythonCommand}"`);

// 3. Чекаємо 5 секунд і відкриваємо сайт саме в Chrome
console.log('⏳ Чекаю 5 секунд, поки завантажиться Вимір Кошмарів...');

setTimeout(() => {
    console.log('🌐 Відкриваю сайт у Chrome!');
    
    // Отримуємо повний шлях до твого HTML файлу
    const fullPath = path.resolve(htmlFile);
    
    // Спробуємо відкрити саме через Chrome, щоб iframe завантажився правильно
    exec(`start chrome "${fullPath}"`, (err) => {
        if (err) {
            console.log('⚠️ Chrome не знайдено, відкриваю браузером за замовчуванням...');
            exec(`start "" "${fullPath}"`);
        } else {
            console.log('✅ Все готово! Білл чекає всередині сайту.');
            console.log('------------------------------------------');
        }
    });
}, 10000); // Змінюємо на 10000 (це 10 секунд)