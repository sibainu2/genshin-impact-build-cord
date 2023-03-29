import asyncio
import requests
from enkanetwork import EnkaNetworkAPI
from enkanetwork.model.character import CharacterSkill,CharacterConstellations
from enkanetwork.enum import Language
from PIL import ImageFont,ImageDraw
from PIL import Image
import json 
from io import BytesIO
from proceses import get_img,backgroundcolor,convert_jpg_to_semi_transparent_png,backgroundcreate,image_syado


json_open = open(r"data/characters.json", 'r')
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
            def skill_icon(skill:CharacterSkill|CharacterConstellations,icon:int) -> Image.Image:
                icon_url = ["icon/Circl.png","icon/Const.png"]
                response = requests.get(skill.icon.url)
                bytes_io = BytesIO(response.content)
                image = Image.open(bytes_io).convert("RGBA")
                x,y = image.size
                image = image.resize((120,120))
                skill_back = Image.open(icon_url[icon]).convert("RGBA")
                #リサイズする
                new_size = (200, 200)
                skill_back = skill_back.resize(new_size).convert("RGBA")
                x,y = skill_back.size
                skill_back.alpha_composite(image,dest=(40,40))
                if icon == 0:

                    draw = ImageDraw.Draw(skill_back)
                    font = ImageFont.truetype(f'./font/ja-jp.ttf', 30)
                    draw.text((x/2-10, y-40), f"{skill.level}", '#000000', font=font)#ffffff
                if icon == 1:
                    if skill.unlocked is False:
                        lock = Image.open(r"icon/lock.png").convert("RGBA")
                        x,y = skill_back.size
                        lock = lock.resize((200,200))
                        skill_back.alpha_composite(lock,dest=(int(0),int(0)))
                        

                skill_back = skill_back.resize((110,110))
                return skill_back
            
            if data.characters:
                for character in data.characters:
                    character.equipments
                    print(character.name)
                    chara = get_img(character.image.banner.url)
                    chara = chara.crop((650,100,1400,800))
                    draw = ImageDraw.Draw(chara)
                    font = ImageFont.truetype(f'./font/ja-jp.ttf', 50)
                    draw.text((20, 20), f"{character.name}", '#ffffff', font=font)
                    chara = image_syado(chara)

                    for i,skill in enumerate(character.skills):
                        skill_image = skill_icon(skill=skill,icon=0)
                        chara.alpha_composite(skill_image,dest=(30,200+170*i))

                    for i,constellation in enumerate(character.constellations):
                        #constellation.icon     
                        constellation_image = skill_icon(skill=constellation,icon=1)
                        chara.alpha_composite(constellation_image,dest=(600,10+120*i))               
                    
                    
                    chara.show()





asyncio.run(main(uid=870558538))