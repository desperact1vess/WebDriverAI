#!/usr/bin/env python3
"""
Пример использования webdriverAI для генерации кода в Qwen.
"""

from webdriverAI import WebdriverAI


def generate_code_with_qwen(ai: WebdriverAI, browser_id: int) -> None:
    ai.login_to_ai(
        browser_id=browser_id,
        ai_type="qwen",
        email="errortop111@gmail.com",  # укажите ваш email
        password="Nekit@0805",  # укажите ваш пароль
    )

    print("\n=== Qwen ===")
    current_model = ai.get_current_model(browser_id)
    print(f"Текущая модель: {current_model}")

    available_models = ai.get_available_models(browser_id)
    if "Qwen3-Coder" in available_models:
        ai.set_model(browser_id, "Qwen3-Coder")
        print("Переключились на модель Qwen3-Coder.")

    ai.new_chat(browser_id)
    ai.write_message(
        browser_id,
        "Напиши пример функции на Python, которая считает факториал числа с помощью рекурсии.",
    )
    ai.send(browser_id)

    answer = ai.get_answer(browser_id)
    print("\nОтвет Qwen:\n")
    print(answer)




def main() -> None:
    ai = WebdriverAI()
    ai.start_browsers(1)
    
    qwen_id = 0
    generate_code_with_qwen(ai, qwen_id)
    
    # ai.close_all_browsers()


if __name__ == "__main__":
    main()
