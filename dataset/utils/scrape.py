import requests
from bs4 import BeautifulSoup
import os
import json
from tenacity import retry, stop_after_attempt

class Scrape:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers = {
            "content-type": "application/json",
            'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-platform": "Linux",
            "referer": "https://mangakakalot.so/",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        }

    @retry(stop=stop_after_attempt(3))
    def _send_request(self,url):
        try:
            return self.session.get(url)
        except Exception as e:
            raise e

    def get_all_chapters(self):
        response = self._send_request(url="https://api.mangago.to/v1/stories/yumis-cells")
        data = json.loads(response.text)
        chapters = data["chapters"]
        return chapters

    def get_chapter_images(self):
        chapters = self.get_all_chapters()
        images_data = []
        total_image_count = 0
        chapter_count = 0
        for chapter in chapters:
            image_count = 0
            images_link = []
            chapter_name = chapter["name"].split(":")[0].strip()
            response = self._send_request(url=f"https://api.mangago.to/v1/chapters/{chapter['id']}/images?page_size=100")
            data = json.loads(response.text)
            results = data["results"]
            for result in results:
                images_link.append(result["image"])
                image_count += 1

            images_data.append({"chapter": chapter_name, "images": images_link})
            total_image_count += image_count
            chapter_count += 1
            print(f"Retrieved chapter - {chapter_name} with {len(images_link)} images")
            self.save_chapter_images(images_data[chapter_count-1])

        print(f"Retrieved {len(images_data)} chapters and {total_image_count} images.")

    def save_chapter_images(self,images_data):
        chapter_title = images_data["chapter"].lower().replace(" ", "_")
        chapter_dir = os.path.join(os.getcwd(), "images", chapter_title)
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)

        for index,img in enumerate(images_data["images"]):
            img_name = f"{chapter_title}_{index+1}.jpg"
            img_path = os.path.join(chapter_dir, img_name)
            with open(img_path, "wb") as f:
                print(f"Successfully saved {img_name} at {img_path}")
                f.write(self._send_request(url=img).content)

if __name__ == "__main__":
    scrape = Scrape()
    scrape.get_chapter_images()

