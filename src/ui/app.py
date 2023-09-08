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
                    review_text = f"Отзыв: {text};"
                    all_reviews.append(review_text)
    return all_reviews


def main():
    with open('E:\\customer-feedback-platform\\src\\data\\reviews_data_vladimir_pyaterochka.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    model_path = "D:\\llama.cpp\\models\\7b\\ggml-model-q4_1.bin"
    overall_sys_prompt = 'Ты — русскоязычный автоматический анализатор отзывов покупателей. Ты получаешь на вход текст нескольких отзывов одного филиала. Сделай короткий вывод о филиале.'
    #review_overall_agent = Agent(model_path, overall_sys_prompt)

    request = '''
        Отзыв 1: Свежие фрукты и овощи, чистый и приятный магазин, располагается рядом с домом, хороший выбор товаров, хорошие цены, быстрое обслуживание, нет очередей, вежливый персонал. Отзыв 2: Нет очередей, хороший выбор товаров, хорошие цены, располагается рядом с домом, вежливый персонал, быстрое обслуживание, свежие фрукты и овощи, чистый и приятный магазин. Вежливый персонал. Быстро нашла что мне нужно. Отличные продукты, свежие. Отзыв 3: Невысокие цены. Персонал приветливый. Отзыв 4: Можно купить кофе, капучино, флэт уайт. Даже ночью)
    '''
    #print(review_overall_agent.interact(request))

    overall_all_filials_sys_prompt = 'Ты — русскоязычный автоматический анализатор отзывов. Ты получаешь на вход несколько отзывов. Проанализируй текст отзывов и выделите ключевые проблемы в этих отзывах.'
    review_overall_all_filials_agent = Agent(model_path, overall_all_filials_sys_prompt)
    request = ''.join(extract_reviews_text(json_data)[:100])
    print(review_overall_all_filials_agent.interact(request))

if __name__ == "__main__":
    main()
