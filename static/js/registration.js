document.getElementById('registrationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const loading = document.getElementById('loading');
    const message = document.getElementById('message');
    const submitBtn = document.querySelector('.register-btn');
    
    // Показываем загрузку
    loading.style.display = 'block';
    message.style.display = 'none';
    submitBtn.disabled = true;
    submitBtn.textContent = 'Регистрация...';
    
    // Собираем данные формы
    const formData = {
        login: document.getElementById('login').value,
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
    
    try {
        const response = await fetch('/auth/registry', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Успешная регистрация
            message.className = 'message success';
            message.textContent = `Успешная регистрация! Добро пожаловать, ${result.username}!`;
            message.style.display = 'block';
            window.location.href = '/';
            
            // Очищаем форму
            document.getElementById('registrationForm').reset();
        } else {
            // Ошибка от сервера
            message.className = 'message error';
            message.textContent = result.detail || 'Произошла ошибка при регистрации';
            message.style.display = 'block';
        }
    } catch (error) {
        // Ошибка сети
        message.className = 'message error';
        message.textContent = 'Ошибка подключения к серверу. Убедитесь, что сервер запущен.';
        message.style.display = 'block';
    } finally {
        // Скрываем загрузку и восстанавливаем кнопку
        loading.style.display = 'none';
        submitBtn.disabled = false;
        submitBtn.textContent = 'Зарегистрироваться';
    }
});