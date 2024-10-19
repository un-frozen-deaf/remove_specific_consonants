import pykakasi
import jaconv
import alkana
import re

def replace_english_with_katakana(text):
    def convert_to_katakana(match):
        english_text = match.group(0)
        katakana = alkana.get_kana(english_text)
        return katakana if katakana else english_text

    pattern = r'[a-zA-Z]+'
    result = re.sub(pattern, convert_to_katakana, text)
    return result

def remove_specific_consonants(original_text, remove_consonants):
    hirakata_text = replace_english_with_katakana(original_text)
    kks = pykakasi.kakasi()
    kks_result = kks.convert(hirakata_text)
    kks_converted_text = ''.join([item['hira'] for item in kks_result])
    kks_converted_text = re.sub(r'ん', 'N', kks_converted_text)
    kks_converted_text = re.sub(r'っ', 'Q', kks_converted_text)
    kks_converted_text = re.sub(r'つ', 'tu', kks_converted_text)
    pattern = f"[{''.join(remove_consonants)}](?=[aiueo])"
    romaji_text = jaconv.kana2alphabet(kks_converted_text)

    romaji_text = re.sub(pattern, '', romaji_text)
    romaji_text = re.sub(r'chi', 'i', romaji_text)
    romaji_text = re.sub(r'shi', 'i', romaji_text)
    romaji_text = re.sub(r'N', 'ん', romaji_text)
    romaji_text = re.sub(r'Q', 'っ', romaji_text)

    return_text = jaconv.alphabet2kana(romaji_text)

    return (return_text)

def process_text_file(input_file_path, output_file_path, remove_consonants):
    processed_lines = []

    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for idx, line in enumerate(lines):
            stripped_line = line.strip()

            if stripped_line:
                processed_line = process_line(stripped_line, remove_consonants)
                processed_lines.append(processed_line)
            else:
                if idx < len(lines) - 1 and lines[idx + 1].strip():
                    processed_lines.append('')

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for line in processed_lines:
            file.write(line + '\n')

def process_line(line, remove_consonants):
    return remove_specific_consonants(line, remove_consonants)

def start_remove_specific_consonants(input_file, output_file, remove_consonants):
    process_text_file(input_file, output_file, remove_consonants)
    # process_text_file(output_file, output_file, remove_consonants)

input_file = 'test.txt'
output_file = 'after.txt'
remove_consonants = ['k', 's', 't', 'p']
start_remove_specific_consonants(input_file, output_file, remove_consonants)

print(f"処理結果は {output_file} に保存されました．")
