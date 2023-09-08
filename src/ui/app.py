import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.agent import Agent


def extract_reviews_text(json_data):
    all_reviews = []
    
    for url, data in json_data.items():
        if 'reviews_list' in data:
            reviews_list = data['reviews_list']
            for i, review in enumerate(reviews_list):
                text = review.get('text', '').strip()
                if text:
                    review_text = f"{text};"
                    all_reviews.append(review_text)
    return all_reviews


def main():
    with open('E:\\customer-feedback-platform\\src\\data\\reviews_data_vladimir_pyaterochka.json', 'r', encoding='utf-8') as f:
        x5_json_data = json.load(f)
    with open('E:\\customer-feedback-platform\\src\\data\\reviews_data_vladimir_magnit.json', 'r', encoding='utf-8') as f:
        magnit_json_data = json.load(f)

    model_path = "D:\\llama.cpp\\models\\7b\\ggml-model-q4_1.bin"

    overall_all_filials_sys_prompt = 'Ты — русскоязычный автоматический анализатор отзывов. Ты получаешь на вход несколько отзывов. Проанализируй текст отзывов и выделите ключевые проблемы в этих отзывах. Ответ дай коротким списком. Обобщи.'
    review_overall_all_filials_agent = Agent(model_path, overall_all_filials_sys_prompt)
    request_x5 = 'Отзывы о магазине "Пятерочка": ' + ''.join(extract_reviews_text(x5_json_data)[:10])
    request_magnit = 'Отзывы о магазине "Магнит": ' + ''.join(extract_reviews_text(magnit_json_data)[:10])
    x5_summary = review_overall_all_filials_agent.interact(request_x5)
    magnit_summary = review_overall_all_filials_agent.interact(request_magnit)

    print('=== Анализ магазинов ===')
    print(f'Пятерочка: {x5_summary}')
    print('----------------')
    print(f'Магнит: {magnit_summary}')
    print('================')

    comparer_sys_prompt = 'Ты — русскоязычный автоматический анализатор магазинов. Ты получаешь на вход два описания магазинов в формате "Магазин 1: <описание 1>; Магазин 1: <описание 1>". Ты должен сравнить их и сообщить, какой магазин лучше.'
    comparer_agent = Agent(model_path, comparer_sys_prompt)
    compare_request = f'Какой магазин лучше и почему? Сравни:\n 1. Магазин "Пятерочка": <{x5_summary}>;\n 2. Магазин "Магнит": <{magnit_summary}>'
    print('=== Сравнение магазинов ===')
    print(comparer_agent.interact(compare_request))

    adviser_sys_prompt = 'Ты — русскоязычный бизнес-советник. Ты получаешь на вход данные о магазине. Напиши, что можно улучшить и как на основе данных.'
    adviser_agent = Agent(model_path, adviser_sys_prompt)
    advise_request_x5 = f'Магазин "Пятерочка": {x5_summary}'
    advise_request_magnit = f'Магазин "Магнит": {magnit_summary}'

    print('=== Советы по развитию ===')
    print(f'Пятерочка: {adviser_agent.interact(advise_request_x5)}')
    print('----------------')
    print(f'Магнит: {adviser_agent.interact(advise_request_magnit)}')
    print('================')

if __name__ == "__main__":
    main()
