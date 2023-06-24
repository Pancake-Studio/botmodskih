import nnytfunction as fc
import os
import itertools
import nnytzstdmodtool as nzm
import zipfile 
import shutil
import re

check_compress_file = "y"
#check_compress_file = input("อยากจะให้เข้ารหัสไฟล์ให้มั้ย[ถ้าไม่เข้ารหัสจะรันเร็วขึ้น] (y/n) : ")

effectskillnamelist = os.path.join(".listname", ".effectskillnamelist.txt")
databinnamelist = os.path.join(".listname", ".databinnamelist.txt")
modelnamelist1 = os.path.join(".listname", ".modelnamelist1.txt")
modelnamelist2 = os.path.join(".listname", ".modelnamelist2.txt")
numberherolist = os.path.join(".listname", ".numberherolist.txt")

condition_id_back = 1
condition_id_haste = 43
condition_id_haste_leave = 36

list_input_id = fc.list_input_id("skin_picture")

for input_id in list_input_id:
  if ".jpg" in input_id:
    input_id = input_id.strip(".jpg")
    mode_common_back = False
    mode_common_haste = False
  if ".png" in input_id:
    input_id = input_id.strip(".png")
    mode_common_back = True
    mode_common_haste = False
  if ".jpeg" in input_id:
    input_id = input_id.strip(".jpeg")
    mode_common_back = True
    mode_common_haste = True
  
  hero_id = input_id[:3]
  first_skin = hero_id + "00"

  heroid = fc.find_hex_skinid(first_skin)
  skinid = fc.find_hex_skinid(input_id)

  effectskillname = fc.check_name(hero_id, effectskillnamelist)
  databinname = fc.check_name(hero_id, databinnamelist)
  modelname1 = fc.check_name(hero_id, modelnamelist1)
  modelname2 = fc.check_name(hero_id, modelnamelist2)
  numberhero = fc.check_name(hero_id, numberherolist)
  file_skill_zip = f"Actor_{hero_id}_Actions.pkg.bytes"
  path_folder_skill = os.path.join("output", "Ages", "Prefab_Characters", "Prefab_Hero")
  path_folder_sound_origin = os.path.join("original", "Databin", "Client", "Sound")
  path_folder_sound_output = os.path.join("output", "Databin", "Client", "Sound")
  path_origin_skill = os.path.join("original", "Ages", "Prefab_Characters", "Prefab_Hero", file_skill_zip)
  path_output_skill = os.path.join("output", "Ages", "Prefab_Characters", "Prefab_Hero", file_skill_zip)

  skill_code_name = hero_id + "_" + effectskillname
  credit_nnyt = bytes.fromhex("4d 61 64 65 42 79 4e 4e 59 54".strip(" ")).decode()
  
  if not os.path.exists(path_folder_sound_output):
    os.makedirs(path_folder_sound_output)

  file_sound_databins = ['BattleBank.bytes', 'ChatSound.bytes', 'HeroSound.bytes', 'LobbySound.bytes', 'LobbyBank.bytes']
  for file_sound_databin in file_sound_databins:
    path_file_sound_databin_output = os.path.join(path_folder_sound_output, file_sound_databin)
    if not os.path.exists(path_file_sound_databin_output):
      path_file_sound_databin_origin = os.path.join(path_folder_sound_origin, file_sound_databin)
    elif os.path.exists(path_file_sound_databin_output):
      path_file_sound_databin_origin = path_file_sound_databin_output
    with open(path_file_sound_databin_origin, 'rb') as file_sound_databin_read:
      code_sound_databin_read = file_sound_databin_read.read()
      code_sound_databin_read = nzm.decompress(code_sound_databin_read)
      code_sound_databin_read = code_sound_databin_read.hex()
      if f'00{fc.find_hex_skinid(input_id)}000000' in code_sound_databin_read:
        check_sound = True
      else:
        check_sound = False
      if check_sound:
        id_skin_hero = fc.hex_skinid_sound(fc.find_hex_skinid(first_skin))
        id_skin_skin = fc.hex_skinid_sound(fc.find_hex_skinid(input_id))
        code_sound_databin_read = code_sound_databin_read.replace(id_skin_hero, fc.hex_skinid_sound("9999"))
        code_sound_databin_read = code_sound_databin_read.replace(id_skin_skin, id_skin_hero)
      else:
        pass
      code_sound_databin_read = bytes.fromhex(code_sound_databin_read)
      if check_compress_file == "y":
        code_sound_databin_read = nzm.compress(code_sound_databin_read)
      else:
        pass
    with open(path_file_sound_databin_output, 'wb') as file_sound_databin_write:
      file_sound_databin_write.write(code_sound_databin_read)

  path_folder_heroskin_origin = os.path.join("original", "Databin", "Client", "Actor")
  path_folder_heroskin_output = os.path.join("output", "Databin", "Client", "Actor")

  if not os.path.exists(path_folder_heroskin_output):
    os.makedirs(path_folder_heroskin_output)
  
  file_heroskin_databin = "heroSkin.bytes"
  path_file_heroskin_origin = os.path.join(path_folder_heroskin_origin, file_heroskin_databin)
  path_file_heroskin_output = os.path.join(path_folder_heroskin_output, file_heroskin_databin)
  if os.path.exists(path_file_heroskin_output):
    path_file_heroskin_origin = path_file_heroskin_output
  else:
    path_file_heroskin_origin = path_file_heroskin_origin
  with open(path_file_heroskin_origin, "rb") as read_heroskin_file:
    heroskin_code = read_heroskin_file.read()
    heroskin_code = nzm.decompress(heroskin_code)
    heroskin_code = heroskin_code.hex()

    code_hero_heroskin = fc.generate_heroskin_code(heroskin_code, heroid, heroid, input_id)
    code_skin_heroskin = fc.generate_heroskin_code(heroskin_code, skinid, heroid, input_id)
    code_skin_heroskin = code_skin_heroskin.replace(f"0000{skinid}0000", f"0000{heroid}0000")
    code_skin_heroskin = code_skin_heroskin.replace(f"00{fc.hex_num_skin_heroskin(input_id[-2:])}00000014000000", f"000000000014000000")

    if int(input_id[3:]) > 9:

      if not int(input_id) == 13210:
        number_dec_code_heroskin = fc.hextodec_2(code_skin_heroskin[:4])
        number_dec_code_heroskin = number_dec_code_heroskin - 1
        code_skin_heroskin = code_skin_heroskin[4:]
        code_skin_heroskin = fc.dectohex_2(number_dec_code_heroskin) + code_skin_heroskin


      code_skin_heroskin = code_skin_heroskin.replace("0008000000", "0007000000")
    code_skin_heroskin = code_skin_heroskin.replace(f"30{(input_id[:-2] + str(int(input_id[-2:]))).encode().hex()}00", f"30{(first_skin[:-2] + '0').encode().hex()}00")

#fux 13210
    if int(input_id) == 13210:
      code_skin_heroskin = code_skin_heroskin.replace("33303133333000", f"3330{(first_skin[:-2] + '0').encode().hex()}00")

    heroskin_code = heroskin_code.replace(code_hero_heroskin, code_skin_heroskin)
    heroskin_code = bytes.fromhex(heroskin_code)

    with open(path_file_heroskin_output, "wb") as write_heroskin_file:
      if check_compress_file == "y":
        heroskin_code = nzm.compress(heroskin_code)
      write_heroskin_file.write(heroskin_code)
    







  if not os.path.exists(path_folder_skill):
    os.makedirs(path_folder_skill)
  shutil.copyfile(path_origin_skill, path_output_skill)
  with zipfile.ZipFile(path_origin_skill, 'r') as origin_zip_skill:
    with zipfile.ZipFile(path_output_skill, 'w') as output_zip_skill:
      for file_skill in origin_zip_skill.namelist():
        code_skill = origin_zip_skill.read(file_skill)
        code_skill = nzm.decompress(code_skill)

        skill_effect_before = "/" + skill_code_name
        skill_effect_after = "/" + skill_code_name + "/" + input_id

        if int(code_skill.find(skill_effect_before.encode())) == -1:
          output_zip_skill.writestr(file_skill, code_skill)
          continue

        code_skill = code_skill.decode()

        code_skill = code_skill.replace(skill_effect_before, skill_effect_after)
        code_skill = code_skill.replace(input_id + "/" + input_id, input_id)
        code_skill = code_skill.replace((skill_effect_after + "/skill"), (skill_effect_before + "/skill"))
        try:
          code_skill = code_skill.replace('"bAllowEmptyEffect" value="true"', '"bAllowEmptyEffect" value="false"')
        except:
          pass
        try:
          code_skill = code_skill.replace(f'name="skinId" value="{input_id}"', f'name="skinId" value="{first_skin}"')
        except:
          pass
        if check_sound:
          count_line_skill_file = fc.count_line(code_skill)
          split_line_sound = fc.split_line(code_skill)
          for i in range(1, count_line_skill_file):
            line_word = split_line_sound[i]
            keyword = '"eventName"'
            if keyword in line_word:
              try:
                pattern = r'value="([^"]*)"'
                match = re.search(pattern, line_word)
                sound_name = match.group(1)
              except:
                continue 
              if f'"eventName" value="Play_{input_id}' in sound_name:
                try:
                  confition_status_before = fc.back_line_code(code_skill, 4, sound_name)
                  confition_status_after = confition_status_before.replace('status="true"', 'status="false"')
                  code_skill = code_skill.replace(confition_status_before, confition_status_after)
                except:
                  pass
              if not input_id in sound_name:
                try:
                  code_skill = code_skill.replace(sound_name, sound_name + "_Skin{}".format(str(int(input_id[-2:]))))
                except:
                  pass
        else:
          pass
        output_zip_skill.writestr(file_skill, code_skill)
  print(f"ทำมอดสกิน {input_id} เสร็จแล้ว!!")
  if mode_common_back:
    path_origin_common = os.path.join("original", "Ages", "Prefab_Characters", "Prefab_Hero", "CommonActions.pkg.bytes")
    path_editing_common = os.path.join("original", "Ages", "Prefab_Characters", "Prefab_Hero", "CommonActions.pkg.bytes(editing)")
    path_output_common = os.path.join("output", "Ages", "Prefab_Characters", "Prefab_Hero", "CommonActions.pkg.bytes")
    file_path_back = os.path.join("commonresource", "Back.xml")
    file_path_haste = os.path.join("commonresource", "HasteE1.xml")
    file_path_haste_leave = os.path.join("commonresource", "HasteE1_leave.xml")
    if not os.path.isfile(path_output_common):
      shutil.copyfile(path_origin_common, path_editing_common)
    else:
      shutil.copyfile(path_output_common, path_editing_common)

    copyright = '    <Copyright tag="">\r\n      <Creator name="nnyt official">\r\n        <Chanel name="youtube" link="https://youtube.com/@nnytofficial"/>\r\n      </Creator>\r\n    </Copyright>'
    bottom_line = "  </Action>\r\n</Project>"
    bottom_line_for_target_back = '    <Track trackName="HitTriggerTick0" eventType="HitTriggerTick" guid="3fcc5b3f-3a9c-495c-bddd-5e3b03e5c01b" enabled="false" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">'

    code_target_back = f'    <Track trackName="{input_id}" eventType="CheckHeroIdTick" guid="{input_id}" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false" guid="348e3d6b-4e50-4f22-8f6c-33edc55dc0f7">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="heroId" value="{hero_id}" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>'
    code_target_back_after = code_target_back + "\r\n" + bottom_line_for_target_back
    code_effect_back = f'    <Track trackName="{credit_nnyt}" eventType="GetHolidayResourcePathTick" guid="95cf43e1-a94a-4b6d-a10e-079af17b888c" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="{str(condition_id_back)}" guid="{input_id}" status="true"/>\r\n      <Event eventName="GetHolidayResourcePathTick" time="0.000" isDuration="false" guid="4259cd02-fa70-4934-ba1a-455544daff9f">\r\n        <int name="battleEffectCfgID" value="0" refParamName="" useRefParam="false" />\r\n        <String name="holidayResourcePathPrefix" value="prefab_skill_effects/hero_skill_effects/{skill_code_name}/{input_id}/huijidi_01" refParamName="" useRefParam="false" />\r\n        <String name="outPathParamName" value="strReturnCityFall" refParamName="" useRefParam="false" />\r\n        <String name="outSoundEventParamName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="{credit_nnyt}" eventType="GetHolidayResourcePathTick" guid="cb944be3-2bf1-4b56-a5da-6676a85f329c" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="{str(condition_id_back)}" guid="{input_id}" status="true"/>\r\n      <Event eventName="GetHolidayResourcePathTick" time="0.000" isDuration="false" guid="c7593f4e-f834-491d-ba7a-0a8395d1fabb">\r\n        <int name="battleEffectCfgID" value="0" refParamName="" useRefParam="false" />\r\n        <String name="holidayResourcePathPrefix" value="prefab_skill_effects/hero_skill_effects/{skill_code_name}/{input_id}/huicheng_tongyong_01" refParamName="" useRefParam="false" />\r\n        <String name="outPathParamName" value="strReturnCityEffectPath" refParamName="" useRefParam="false" />\r\n        <String name="outSoundEventParamName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>'
    code_effect_back_after = code_effect_back + "\r\n" + bottom_line
    if mode_common_haste:
      if int(input_id) == 15009:
        effect_haste_name = "T2_Spint"
      elif int(input_id) == 11607:
        effect_haste_name = "jingke_sprint_01"
      elif int(input_id) == 14111:
        effect_haste_name = "14111_luoer_Sprint"
      else:
        effect_haste_name = "jiasu_tongyong_01"
      code_target_haste = f'    <Track trackName="{input_id}" eventType="CheckHeroIdTick" guid="{input_id}" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false" guid="348e3d6b-4e50-4f22-8f6c-33edc55dc0f7">\r\n        <TemplateObject name="targetId" id="1" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="heroId" value="{hero_id}" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>'
      code_effect_haste = f'    <Track trackName="{input_id}" eventType="TriggerParticle" guid="412ea073-5944-46e4-ae5e-3037e855fda7" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="{condition_id_haste}" guid="{input_id}" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="5.000" isDuration="true" guid="33d560cb-4b84-4eaa-a851-e57d7a7de1c7">\r\n        <TemplateObject name="targetId" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/{skill_code_name}/{input_id}/{effect_haste_name}" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>'
      code_effect_haste_leave = f'    <Track trackName="{input_id}" eventType="TriggerParticle" guid="412ea073-5944-46e4-ae5e-3037e855fda7" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="{condition_id_haste_leave}" guid="{input_id}" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="5.000" isDuration="true" guid="33d560cb-4b84-4eaa-a851-e57d7a7de1c7">\r\n        <TemplateObject name="targetId" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/{skill_code_name}/{input_id}/{effect_haste_name}" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>'

    with zipfile.ZipFile(path_editing_common, 'r') as origin_zip_common:
      with zipfile.ZipFile(path_output_common, 'w') as output_zip_common:
        for file_commons in origin_zip_common.namelist():
          if not mode_common_haste:
            if "/HasteE1.xml" in file_commons:
              code_haste = origin_zip_common.read(file_commons)
              output_zip_common.writestr(file_commons, code_haste)
            elif "/HasteE1_leave.xml" in file_commons:
              code_haste = origin_zip_common.read(file_commons)
              output_zip_common.writestr(file_commons, code_haste)
            else:
              pass
          if mode_common_back:
            if file_path_back in file_commons:
              code_back = origin_zip_common.read(file_commons)
              output_common_back = nzm.decompress(code_back)
              if not copyright.encode() in output_common_back:
                output_common_back = output_common_back.replace(bottom_line.encode(), copyright.encode() + b"\r\n" + bottom_line.encode())
              output_common_back = output_common_back.replace(bottom_line.encode(), code_effect_back_after.encode())
              output_common_back = output_common_back.replace(bottom_line_for_target_back.encode(), code_target_back_after.encode())
              if check_compress_file == 'y':
                output_common_back = nzm.compress(output_common_back)
              else:
                pass
              output_zip_common.writestr(file_commons, output_common_back)
              condition_id_back += 1
            else:
              pass
          if mode_common_haste:
            if file_path_haste == file_commons:
              code_haste = origin_zip_common.read(file_commons)
              output_common_haste = nzm.decompress(code_haste)
              if not copyright.encode() in output_common_haste:
                output_common_haste = output_common_haste.replace(bottom_line.encode(), copyright.encode() + b"\r\n" + bottom_line.encode())
              output_common_haste = output_common_haste.replace(bottom_line.encode(), code_effect_haste.encode() + b"\r\n" + bottom_line.encode())
              output_common_haste = output_common_haste.replace(copyright.encode(), code_target_haste.encode() + b"\r\n" + copyright.encode())
              if check_compress_file == 'y':
                output_common_haste = nzm.compress(output_common_haste)
              else:
                pass
              output_zip_common.writestr(file_commons, output_common_haste)
              condition_id_haste += 1
            else:
              pass
            if file_path_haste_leave == file_commons:
              code_haste_leave = origin_zip_common.read(file_commons)
              output_common_haste_leave = nzm.decompress(code_haste_leave)
              if not copyright.encode() in output_common_haste_leave:
                output_common_haste_leave = output_common_haste_leave.replace(bottom_line.encode(), copyright.encode() + b"\r\n" + bottom_line.encode())
              output_common_haste_leave = output_common_haste_leave.replace(bottom_line.encode(), code_effect_haste_leave.encode() + b"\r\n" + bottom_line.encode())
              output_common_haste_leave = output_common_haste_leave.replace(copyright.encode(), code_target_haste.encode() + b"\r\n" + copyright.encode())
              if check_compress_file == 'y':
                output_common_haste_leave = nzm.compress(output_common_haste_leave)
              else:
                pass
              output_zip_common.writestr(file_commons, output_common_haste_leave)
              condition_id_haste_leave += 1
            else:
              pass
          else:
            pass
          if not file_path_haste_leave in file_commons:
            if not file_path_back in file_commons:
              if not file_path_haste in file_commons:
                output_common = origin_zip_common.read(file_commons)
                output_zip_common.writestr(file_commons, output_common)
print("แก้ไขไฟล์ CommonActions.pkg.bytes เสร็จแล้ว")