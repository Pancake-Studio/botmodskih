import os
import zipfile
import shutil
import re
import random

def find_line(hero_id):
  file_path = ".listname/.numberherolist.txt"
  with open(file_path, 'r') as file:
    lines = file.readlines()
    for line_number, line in enumerate(lines):
      if hero_id in line:
        return line_number
    return None


def read_line(filename, line_number):
  with open(filename, 'r') as file:
    lines = file.readlines()
    return lines[line_number]

def check_name(hero_id, file):
  line = find_line(hero_id)
  if line is not None:
      name = read_line(file, line)
      name = name.encode()
      name = name.strip(b"\n")
      name = name.decode()
      return name
  else:
      return None


def list_input_id(folder):
  skin_pt_todo = os.listdir(folder)
  if skin_pt_todo != []:
    return skin_pt_todo
  else:
    print(f"None picture in folder 📁 --> {folder} <-- 📂")
    return []
    
def modify_zip(zip_path, file_path):
    with zipfile.ZipFile(zip_path, 'a') as zip_file:
        file_contents = zip_file.read(file_path)
        modified_contents = file_contents.replace()
        zip_file.delete(file_path)
        zip_file.writestr(file_path, modified_contents)

def back_line_code(code_skill, back_line, skin_id_code):
  count_line = 1
  for char in code_skill:
    if char == "\n":
      count_line += 1
  lines = code_skill.split("\r\n")
  for i in range(1, count_line):
    if skin_id_code in lines[i]:
      return lines[i - int(back_line)]
    else:
      pass

def line_code(code_skill, skin_id_code):
  count_line = 1
  for char in code_skill:
    if char == "\n":
      count_line += 1
  lines = code_skill.split("\r\n")
  for i in range(1, count_line):
    if skin_id_code in lines[i]:
      return lines[i]
    else:
      pass


def find_guid(code):
  try:
    code = str(code)
  except:
    pass
  pattern = r'guid="([^"]*)"'
  match = re.search(pattern, code)

  if match:
    guid_value = match.group(1)
    return guid_value
  else:
    pass

def count_line(code_skill):
  count_line = 1
  for char in code_skill:
    if char == "\n":
      count_line += 1
  return count_line

def split_line(code_skill):
  lines = code_skill.split("\r\n")
  return lines

def find_hex_skinid(input_id):
  input_id = int(input_id)
  hex_skinid = hex(input_id)
  hex_skinid = hex_skinid[2:]
  if len(hex_skinid) == 3:
    hex_skinid = "0" + hex_skinid
  hex_skinid = hex_skinid[2:] + hex_skinid[:2]
  return hex_skinid

def hex_skinid_sound(input):
  output = f"00{input}000000"
  return output

def hex_skinid_heroskin(input):
  output = f"0000{input}0000"
  return output

def number_skin_heroskin(input):
  heroid = input[:3]
  skin_number = str(int(input[-2:]))
  output = f"30{heroid + skin_number}"
  return output

def hextodec_2(input):
  output = input[2:] + input[:2]
  output = int(output, base=16)
  return output

def dectohex_2(input):
  output = int(input)
  output = hex(output)
  output = output.strip("0x")
  if len(output) == 3:
    output = "0" + output
  elif len(output) == 2:
    output = "0" + output + "0"
  output = output[2:] + output[:2]
  return output

def generate_heroskin_code(code_heroskin, skin_id, hero_id, input_id):
  skin_id = f"0000{skin_id}0000"
  pos_skin_id = code_heroskin.find(skin_id)
  pos_dec_code_heroskin = int(pos_skin_id) - 4
  dec_code_heroskin = code_heroskin[pos_dec_code_heroskin:pos_dec_code_heroskin + 4]
  number_dec_code_heroskin = hextodec_2(dec_code_heroskin)
  number_dec_code_heroskin = number_dec_code_heroskin * 2

  code_skin_heroskin = code_heroskin[pos_dec_code_heroskin:pos_dec_code_heroskin + number_dec_code_heroskin]
  output = code_skin_heroskin
  return output

def hex_num_skin_heroskin(input):
  input = int(input)
  output = hex(input)
  output = output.strip("0x")
  if len(output) == 1:
    output = "0" + output
  return output