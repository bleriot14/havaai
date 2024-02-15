import requests

url = "http://localhost:1881/tercuman"  # İsteğinizi göndermek istediğiniz URL

# Göndermek istediğiniz verileri bir sözlük olarak tanımlayın
data = {
    "text": "Merhaba, nasılsınız, umarım her şey yolundadır?",
    "language": "en-tr"
}

# POST isteği yapın ve cevabı alın
response = requests.post(url, data=data)

# Cevabı işleyin
if response.status_code == 200:
    response_json = response.json()
    translation_result = response_json["translation_result"]
    translation_metric = response_json["translation_metric"]
    print("Translation Result:", translation_result)
    print("Translation Metric:", translation_metric)
else:
    print("Error:", response.text)
 