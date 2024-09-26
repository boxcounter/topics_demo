# pylint: disable=missing-function-docstring
import json
import logging

import streamlit as st


topics = [
    ("Culture", "文化"),
    ("Technology", "科技"),
    ("Business", "商业"),
    ("Politics", "政治"),
    ("Finance", "金融"),
    ("Food & Drink", "美食与饮品"),
    ("Sports", "体育"),
    ("Art & Illustration", "艺术与插画"),
    ("Fashion & Beauty", "时尚与美容"),
    ("Music", "音乐"),
    ("Faith & Spirituality", "信仰与灵性"),
    ("Climate & Environment", "气候与环境"),
    ("Science", "科学"),
    ("Literature", "文学"),
    ("Fiction", "小说"),
    ("Health & Wellness", "健康与养生"),
    ("Design", "设计"),
    ("Travel", "旅行"),
    ("Parenting", "育儿"),
    ("Philosophy", "哲学"),
    ("Comics", "漫画"),
    ("International", "国际"),
    ("Crypto", "加密货币"),
    ("History", "历史"),
    ("Humor", "幽默"),
    ("Education", "教育"),
    ("Others", "其他"),
]

def load_articles(
    file_path: str
) -> list[dict]:
    """
    Load articles from a JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        A list of articles.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            articles = json.load(file)
        logging.info("Successfully loaded %d articles from %s", len(articles), file_path)
        return articles
    except FileNotFoundError:
        logging.error("File not found: %s", file_path)
        return []
    except json.JSONDecodeError:
        logging.error("Invalid JSON format in file: %s", file_path)
        return []
    except Exception as e:
        logging.error("An error occurred while loading articles from %s: %s", file_path, str(e))
        return []


def organize_articles_by_topic(
    articles: list[dict]
) -> dict[str, list[dict]]:
    """
    Organize articles by topic.

    Args:
        articles: A list of articles.

    Returns:
        A dictionary with topics as keys and articles as values.
    """
    organized_articles = {}
    for article in articles:
        for topic in article.get('topics', []):
            if topic not in organized_articles:
                organized_articles[topic] = []
            organized_articles[topic].append(article)
    return organized_articles


def main(file_path: str):
    articles = load_articles(file_path)
    organized_articles = organize_articles_by_topic(articles)

    tabs = st.tabs([f"{topic[0]} ({topic[1]})" for topic in topics])

    for i, tab in enumerate(tabs):
        with tab:
            if topics[i][0] not in organized_articles:
                st.write('No articles in this topic')
                continue

            for article in organized_articles[topics[i][0]]:
                expander = st.expander(article['title'])
                content = (f'**Topics:** \n{", ".join(article["topics"])}\n\n'
                           f'**Content:** \n\n{article["content"]}')
                expander.write(content)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    main('./bookmarks_with_topics.json')
