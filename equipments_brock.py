import asyncio
import requests
from enkanetwork import EnkaNetworkAPI
from enkanetwork.model.character import CharacterSkill,CharacterConstellations,Equipments
from enkanetwork.enum import EquipmentsType
from enkanetwork.enum import Language
from PIL import ImageFont,ImageDraw
from PIL import Image
import json 
from io import BytesIO
from proceses import get_img,backgroundcolor,convert_jpg_to_semi_transparent_png,backgroundcreate,image_syado

json_open = open(r"./data/characters.json", 'r')
json_load = json.load(json_open)

genshin_color = open(r"data/color.json", 'r')
genshin_color = json.load(genshin_color)

client = EnkaNetworkAPI(lang=Language.JP)


async def main(uid):
    global genshin_color,json_load
    async with client:
        #client.set_language(Language.JP)
        data = await client.fetch_user_by_uid(uid=uid)
        if data: 
            
            print("=== Player Info ===")
            print(f"ニックネーム: {data.player.nickname}")
            print(f"レベル: {data.player.level}")
            print(f"Icon: {data.player.namecards}")
            print(f"ステータスメッセージ: {data.player.signature}")
            print(f"アチーブメント: {data.player.achievement}")
            print(f"螺旋: {data.player.abyss_floor} - {data.player.abyss_room}")
            print(f"Cache timeout: {data.ttl}")
            #天賦の処理
            def equipment_brock(equipment:Equipments):
                back_image = convert_jpg_to_semi_transparent_png("item/box.png",alpha=0.2) 
                equipment_type = equipment.type
                back_x,back_y = back_image.size
                detail = equipment.detail
                if equipment_type == EquipmentsType.WEAPON:
                    weapon_icon = get_img(equipment.detail.icon.url)
                    x,y = weapon_icon.size
                    weapon_icon = weapon_icon.resize((x*4,y*4))
                    back_image.alpha_composite(weapon_icon,dest=(-120,-100))
                    for sutats in equipment.detail.substats:
                        icon_image = Image.open(fr"icon\{sutats.prop_id}.png")
                        unit = ""
                        if sutats.name[-1] == "率":
                            unit = "%"
                        draw = ImageDraw.Draw(back_image)
                        font = ImageFont.truetype(f'./font/ja-jp.ttf', 50)
                        draw.text((20, 20), f"{sutats.name} {sutats.value}", '#ffffff', font=font)

                        print(sutats.name,sutats.value,sutats.prop_id)

                    

                elif equipment_type == EquipmentsType.ARTIFACT:
                    back_image = back_image.resize((back_x,int(back_y*1.5)))
                    artifact_icon = get_img(equipment.detail.icon.url)
                    x,y = artifact_icon.size
                    artifact_icon = artifact_icon.resize((x*4,y*4))
                    back_image.alpha_composite(artifact_icon,dest=(-120,-100))
                    for i,sutats in enumerate(detail.substats):
                        icon_image = Image.open(fr"icon\{sutats.prop_id}.png")
                        icon_image = icon_image.resize((100,100))
                        back_image.alpha_composite(icon_image,dest=(60,500+ 120*i))
                        unit = ""
                        if "PERCENT" in sutats.prop_id:
                            unit = "%"
                        draw = ImageDraw.Draw(back_image)
                        #ステータスの名前
                        font = ImageFont.truetype(f'./font/ja-jp.ttf', 40)
                        draw.text((180,530+ 110*i), f"{sutats.name}", '#ffffff', font=font)
                        #ステータス
                        font = ImageFont.truetype(f'./font/ja-jp.ttf', 80)
                        draw.text((530,500+ 120*i), f"+{sutats.value}{unit}", '#ffffff', font=font)
                        print(sutats.name,sutats.value,sutats.prop_id)

                return back_image
                    
            
            if data.characters:
                for character in data.characters:
                    print(character.name)
                    chara = get_img(character.image.banner.url)
                    chara = chara.crop((650,100,1400,800))
                    draw = ImageDraw.Draw(chara)
                    font = ImageFont.truetype(f'./font/ja-jp.ttf', 50)
                    draw.text((20, 20), f"{character.name}", '#ffffff', font=font)
                    chara = image_syado(chara)
                    for equipment in character.equipments:
                        equipment_brock(equipment).show()
                       

                    




asyncio.run(main(uid=870558538))