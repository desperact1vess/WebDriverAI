@echo off
title Qwen AI Assistant - Запуск приложения

echo.
echo ###############################################################################
echo #                                                                             #
echo #                           Qwen AI Assistant                                 #
echo #                        Графический интерфейс                                #
echo #                                                                             #
echo ###############################################################################
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не установлен или не добавлен в PATH
    echo Пожалуйста, установите Python и убедитесь, что он добавлен в PATH
    pause
    exit /b 1
)

REM Проверяем наличие requirements.txt
if not exist "requirements.txt" (
    echo [ОШИБКА] Файл requirements.txt не найден
    echo Убедитесь, что файл requirements.txt находится в текущей директории
    pause
    exit /b 1
)

echo [ИНФО] Устанавливаю зависимости...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ОШИБКА] Не удалось установить зависимости
    pause
    exit /b 1
)

echo.
echo [ИНФО] Запускаю Qwen AI Assistant...
echo.
python qwen_gui.py

echo.
echo [ИНФО] Работа программы завершена.
echo.
pause