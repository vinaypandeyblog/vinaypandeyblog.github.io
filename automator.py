import re
from datetime import datetime
import os
import glob

def get_length_category(content):
    word_count = len(content.split())
    if word_count < 30:
        return "लघु"
    elif word_count < 100:
        return "मध्यम"
    else:
        return "दीर्घ"

def get_matching_images(date, images_dir):
    date_str = date.strftime('%Y%m%d')
    pattern = os.path.join(images_dir, f'IMG-{date_str}*')
    return glob.glob(pattern)

def process_chat_log(input_file, output_directory, images_directory):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    messages = re.split(
        r'\n(?=\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - Vinay Pandey:)', content)

    for message in messages:
        match = re.match(
            r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - Vinay Pandey: ?(.*)', message, re.DOTALL)
        if match:
            date_time_str, content = match.groups()
            date_time = datetime.strptime(date_time_str, '%d/%m/%Y, %H:%M')

            title_match = re.search(r'\*(.*?)\*', content)
            title = title_match.group(1) if title_match else "Untitled"
            full_title = title
            if len(title) > 25:
                title = title[:25]

            content = content.split('\n', 1)[1] if '\n' in content else content

            day_of_week = date_time.strftime('%A').lower()
            day_based_tag = {
                'sunday': 'रवि दर्शन',
                'monday': 'सोम का मर्म',
                'tuesday': 'मंगल कामना',
                'wednesday': 'बुध की सुध',
                'thursday': 'गुरु का ग्यान',
                'friday': 'शुक्र की फिक्र',
                'saturday': 'शनि का सच'
            }.get(day_of_week, day_of_week)

            length_category = get_length_category(content)

            filename = f"{date_time.strftime('%Y-%m-%d')}-{title.replace(' ', '-')}.md"
            filename = re.sub(r'[^\w\-.]', '', filename)

            # Get matching images
            matching_images = get_matching_images(date_time, images_directory)
            image_markdown = ""
            for img in matching_images:
                image_markdown += f"\n![{os.path.basename(img)}](/images/{os.path.basename(img)}))\n"

            markdown_content = f"""---
title: {full_title}
layout: post
last_modified_at: {date_time.strftime('%Y-%m-%dT%H:%M:%S%z')}
author: Vinay Pandey
tags:
- {day_based_tag}
categories:
- {length_category}
---
{content.strip()}

{image_markdown}
"""

            with open(os.path.join(output_directory, filename), 'w', encoding='utf-8') as output_file:
                output_file.write(markdown_content)

# Usage
input_file = 'bkp.txt'
output_directory = '_posts'
images_directory = 'images'
process_chat_log(input_file, output_directory, images_directory)