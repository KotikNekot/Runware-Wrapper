# pyrunware

`pyrunware` — это асинхронная библиотека на Python для взаимодействия с [API Runware](https://docs.runware.ai/en/getting-started/introduction) для генерации и обработки изображений.

## Установка

Установить библиотеку можно напрямую из GitHub:

```bash
pip install git+https://github.com/KotikNekot/Runware-Wrapper.git
```

## Пример использования

### 1. Создание объекта класса

```python
from pyrunware import RunwareWS

runware = RunwareWS("<token>")
```

### 2. Генерация изображений по текстовому запросу
```python
images = await runware.image_inference(
    positive_prompt="pixel cat",
    model="runware:100@1",
)

for image in images:
    print(image.image_url)
```

### 3. Улучшение текстового запроса (Prompt Enhancer)
```python
prompts = await runware.prompt_enhancer(
    prompt="pixel cat",
    prompt_max_length=400,
    amount_results=5
)

for prompt in prompts:
    print(prompt.text)
```

### 4. Удаление фона с изображения
```python
image = await runware.remove_background(
    image="https://im.runware.ai/image/ws/0.5/ii/4ef5758a-acce-4f0b-9691-064fbdbc2441.jpg",
)
print(image.image_url)
```

### 5. Увеличение разрешения изображения (Upscale)
```python
image = await runware.upscale(
    image="https://im.runware.ai/image/ws/0.5/ii/0c8492c6-a241-42fa-bba9-3e92851305c8.jpg",
    upscale_factor=4
)

print(image.image_url)
```


## Лицензия

Этот проект лицензирован под MIT License — см. файл LICENSE для деталей.

