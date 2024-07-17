# 为了方便打标，将json文件转为txt文件
# 记得修改目录路径
import os
import json
from datetime import datetime

# 遍历所有目录下的 JSON 文件
def traverse_and_process(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                input_file = os.path.join(root, file)
                process_file(input_file)

# 处理单个文件
def process_file(input_file):
    count = 1
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            process_line(line, count)
            count += 1

def process_line(line, count):
    try:
        data = json.loads(line)
        # 提取关键数据转为txt
        json2txt(data)
        print(f'Processed line {count}')
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
    except KeyError as e:
        print(f"KeyError: Missing key {e}")

def json2txt(data):
    try:
        danbooru_data = data['danbooru']
        
        # 提取关键参数
        id_value = str(danbooru_data['id'])
        tag_general = danbooru_data.get('tag_string_general', '')
        tag_character = danbooru_data.get('tag_string_character', '')
        tag_copyright = danbooru_data.get('tag_string_copyright', '')
        tag_artist = danbooru_data.get('tag_string_artist', '')
        rating = danbooru_data['rating']
        created_at = danbooru_data['created_at']
        
        # 格式化标签字符串
        def format_tags(tag_string):
            tags = tag_string.split()
            formatted_tags = ', '.join(tags)
            return formatted_tags

        tag_general_formatted = format_tags(tag_general)
        tag_character_formatted = format_tags(tag_character)
        tag_copyright_formatted = format_tags(tag_copyright)
        tag_artist_formatted = format_tags(tag_artist)
        
        # 构造文件名
        filename = f"danbooru_{id_value}.txt"
        year = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%f%z").year
        
        # 写入文本文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"{tag_artist_formatted}, ")
            f.write(f"{tag_general_formatted}, ")
            f.write(f"{tag_character_formatted}, ")
            f.write(f"{tag_copyright_formatted}, ")
            f.write(f"year_{year}, ")
            if rating == 'e':
                f.write("nsfw")
        print(f"文件 {filename} 已成功创建并保存相关数据。")
    
    except KeyError as e:
        print(f"KeyError: Missing key {e}")

# 设置json文件目录路径
root_dir = './'

# 开始遍历和处理
traverse_and_process(root_dir)
