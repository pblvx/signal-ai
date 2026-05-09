import requests
from typing import List, Dict, Any

def get_reddit_trends(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Obtiene los posts más populares de r/technology en Reddit.
    """
    url = f"https://www.reddit.com/r/technology/hot.json?limit={limit}"
    headers = {"User-Agent": "SignalApp/1.0"}
    trends = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        posts = data.get("data", {}).get("children", [])
        for post in posts:
            post_data = post.get("data", {})
            trends.append({
                "title": post_data.get("title", "No Title"),
                "url": post_data.get("url", ""),
                "score": post_data.get("score", 0),
                "source": "Reddit"
            })
    except requests.RequestException as e:
        print(f"Error fetching from Reddit: {e}")
        
    return trends

def get_hackernews_trends(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Obtiene las historias principales de Hacker News.
    """
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    trends = []
    
    try:
        # Obtener los IDs de las mejores historias
        response = requests.get(top_stories_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()
        
        # Limitar la cantidad de IDs
        top_ids = story_ids[:limit]
        
        # Obtener detalles de cada historia por su ID
        for story_id in top_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            try:
                story_response = requests.get(story_url, timeout=5)
                story_response.raise_for_status()
                story_data = story_response.json()
                
                if story_data:
                    trends.append({
                        "title": story_data.get("title", "No Title"),
                        "url": story_data.get("url", ""),
                        "score": story_data.get("score", 0),
                        "source": "Hacker News"
                    })
            except requests.RequestException as item_err:
                print(f"Error fetching Hacker News item {story_id}: {item_err}")
                continue
                
    except requests.RequestException as e:
        print(f"Error fetching from Hacker News: {e}")
        
    return trends
