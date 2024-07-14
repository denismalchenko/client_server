import requests
import os


def download_files(urls, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for url, filename in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            save_path = f"{save_dir}/{filename}"
            with open(save_path, "wb") as file:
                file.write(response.content)
                print(f"Файл '{filename}' успешно загружен")
        else:
            print(f"Ошибка загрузки файла с URL: {url}")


urls = {
    "https://drive.google.com/uc?id=1htYNpzbKgcIkprqkwGLl6dpEN6HvtpEG&export=download": "Winnie_the_Pooh.MP3",
    "https://drive.google.com/uc?id=1LykGWLsMNYspLqY2De_wsGguNDQwS18r&export=download": "singer.mov",
    "https://drive.google.com/uc?id=15RBOel7CANWBOz20Y7jVyPdBs6fs5JB6&export=download": "picture.jpg",
    "https://drive.google.com/uc?id=1i44JhNEAIRFEdyMP5V2UggDPmFXyYmnh&export=download": "matroskin.mp3",
    "https://drive.google.com/uc?id=1yV3zYiww_C_vOcEiAox5P0nNGT238tcF&export=download": "duet.mp3",
}

save_dir = "examples_files"

if __name__ == "__main__":
    download_files(urls, save_dir)
