import requests
from bs4 import BeautifulSoup
import os
from tenacity import retry, stop_after_attempt

class Scrape:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.url ="https://www.webtoons.com/en/slice-of-life/yumi-cell/list" 
        self.session.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.8",
            'sec-ch-ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
            "sec-ch-ua-platform": "Linux",
            "referer": self.url,
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        }

        self.params = {
            "title_no": 478,
            "page": 1,
        }

    @retry(stop=stop_after_attempt(3))
    def _send_request(self,url):
        try:
            return self.session.get(url, params=self.params)
        except Exception as e:
            raise e

    def get_max_pages(self):
        html_response = self._send_request(url=self.url)
        soup = BeautifulSoup(html_response.text, "html.parser")
        max_pages = int(soup.find_all("div", class_="paginate")[0].find_all("a")[-1].text)
        return max_pages

    def get_episode_list(self):
        max_pages = self.get_max_pages()
        episode_list = []
        for page in range(1, max_pages+1):
            self.params["page"] = page
            html_response = self._send_request(url=self.url)
            soup = BeautifulSoup(html_response.text, "html.parser")
            ep_list = soup.find_all("li", class_="_episodeItem")
            for ep in ep_list:
                episode = {}
                episode["title"] = ep.find_all("a")[0].text.split("-")[0].strip()
                episode["link"] = ep.find_all("a")[0]["href"]
                episode_list.append(episode)

        return episode_list

    def get_episode_images(self):
        episode_data = []
        ep_list = self.get_episode_list()
        image_count = 0
        for ep in ep_list:
            episode_images = []
            html_response = self._send_request(url=ep["link"])
            soup = BeautifulSoup(html_response.text, "html.parser")
            images = soup.find_all("img", class_="_images")
            for image in images:
                episode_images.append(image["data-url"])
                image_count += 1
            
            episode_data.append({"episode": ep["title"], "data_url": episode_images}) 

        print(f"Retrieved {len(episode_data)} episodes and {image_count} images.")

        return episode_data

    def save_episode_images(self):
        episode_images = self.get_episode_images()
        for episode in episode_images:
            episode_title = episode["episode"].replace(". ", "_")
            episode_dir = os.path.join(os.getcwd(), "images", episode_title)
            if not os.path.exists(episode_dir):
                os.makedirs(episode_dir)

            for index,img in enumerate(episode["data_url"]):
                img_name = f"{episode_title}_{index+1}.jpg"
                img_path = os.path.join(episode_dir, img_name)
                with open(img_path, "wb") as f:
                    print(f"Saving {img_name}...")
                    f.write(self._send_request(url=img).content)


if __name__ == "__main__":
    scrape = Scrape()
    scrape.save_episode_images()
        

