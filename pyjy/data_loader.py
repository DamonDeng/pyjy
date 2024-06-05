from pyjy.constants import GameConfig
from pyjy.utils.binary_reader import BinaryReader

import struct

class RangerLoader:
    
    def __init__(self):
        self.temp_name_bytes = None
        pass
    
    def load(self, \
            index_file_name="./original_resource/save/ranger.idx32", \
            grp_file_name="./original_resource/save/ranger.grp32"):
        ranger_index_result = BinaryReader.read_file_to_vector(index_file_name, "I")
        
        # the following mapping relationship is hard coded by the original project
        
        basic_info_start = 0
        basic_info_end = ranger_index_result[0]
        
        roles_info_start = ranger_index_result[0]
        roles_info_end = ranger_index_result[1]
        
        items_info_start = ranger_index_result[1]
        items_info_end = ranger_index_result[2]
        
        submaps_info_start = ranger_index_result[2]
        submaps_info_end = ranger_index_result[3]
        
        magics_info_start = ranger_index_result[3]
        magics_info_end = ranger_index_result[4]
        
        shops_info_start = ranger_index_result[4]
        shops_info_end = ranger_index_result[5]
        
        # load all information into memory at first
        ranger_grp_result = BinaryReader.read_file_to_vector(grp_file_name, "B")

        # basic information
        basic_info = ranger_grp_result[basic_info_start:basic_info_end]
        self.load_basic_info(basic_info)
        
        # roles information
        roles_info = ranger_grp_result[roles_info_start:roles_info_end]
        self.load_roles_info(roles_info)
        
        # items information
        items_info = ranger_grp_result[items_info_start:items_info_end]
        self.load_items_info(items_info)
        
        # submaps information
        submaps_info = ranger_grp_result[submaps_info_start:submaps_info_end]
        self.load_submaps_info(submaps_info)
        
        # magics information
        magics_info = ranger_grp_result[magics_info_start:magics_info_end]
        self.load_magics_info(magics_info)
        
        # shops information
        shops_info = ranger_grp_result[shops_info_start:shops_info_end]
        self.load_shops_info(shops_info)
        
        
    def convert_byte_array_to_int(self, byte_array):
        return struct.unpack('i', bytes(list(byte_array)))[0]
    
    def convert_byte_array_to_int16(self, byte_array):
        return struct.unpack('h', bytes(list(byte_array)))[0]
        
    def load_basic_info(self, basic_info_bytes):
        
        # convert the byte array to int array at first
        basic_info = []
        for i in range(0, len(basic_info_bytes), 4):
            basic_info.append(self.convert_byte_array_to_int(basic_info_bytes[i:i+4]))
        
        
        # original c++ code of the basic info data format:
        # int InShip, InSubMap, MainMapX, MainMapY, SubMapX, SubMapY, FaceTowards, ShipX, ShipY, ShipX1, ShipY1, Encode;
        # int Team[TEAMMATE_COUNT];
        # ItemList Items[ITEM_IN_BAG_COUNT];
        # loading above data into self attributes
        
        self.InShip = basic_info[0]
        self.InSubMap = basic_info[1]
        self.MainMapX = basic_info[2]
        self.MainMapY = basic_info[3]
        self.SubMapX = basic_info[4]
        self.SubMapY = basic_info[5]
        self.FaceTowards = basic_info[6]
        self.ShipX = basic_info[7]
        self.ShipY = basic_info[8]
        self.ShipX1 = basic_info[9]
        self.ShipY1 = basic_info[10]
        self.Encode = basic_info[11]
        
        self.team = []
        for i in range(GameConfig.TEAMMATE_COUNT):
            self.team.append(basic_info[12+i])
            
        self.items = []
        for i in range(GameConfig.ITEM_IN_BAG_COUNT):
            item_id_offset = 12+GameConfig.TEAMMATE_COUNT+i*2
            item_count_offset = 12+GameConfig.TEAMMATE_COUNT+i*2+1
            if item_id_offset >= len(basic_info) or item_count_offset >= len(basic_info):
                break
            
            item_id = basic_info[12+GameConfig.TEAMMATE_COUNT+i*2]
            item_count = basic_info[12+GameConfig.TEAMMATE_COUNT+i*2+1]
            self.items.append((item_id, item_count))
            
    def load_roles_info(self, roles_info):
        
        ROLE_DATA_LENGTH = 364 # 364 bytes
        number_of_roles = len(roles_info) // ROLE_DATA_LENGTH
        print("Loading roles, number: ", number_of_roles)
        
        self.roles = []
        for i in range(number_of_roles):
            role_data = roles_info[i*ROLE_DATA_LENGTH:(i+1)*ROLE_DATA_LENGTH]
            role = self.load_one_role(role_data)
            self.roles.append(role)
            
    def load_items_info(self, items_info):
            
        ITEM_DATA_LENGTH = 380 # 380 bytes
        
        number_of_items = len(items_info) // ITEM_DATA_LENGTH
        print("Loading items, number: ", number_of_items)
        
        self.items = []
        for i in range(number_of_items):
            item_data = items_info[i*ITEM_DATA_LENGTH:(i+1)*ITEM_DATA_LENGTH]
            item = self.load_one_item(item_data)
            self.items.append(item)
            
    def load_submaps_info(self, submaps_info):
        SUBMAP_DATA_LENGTH = 104 # 104 bytes
        
        number_of_submaps = len(submaps_info) // SUBMAP_DATA_LENGTH
        print("Loading submaps, number: ", number_of_submaps)
        
        self.submaps = []
        for i in range(number_of_submaps):
            submap_data = submaps_info[i*SUBMAP_DATA_LENGTH:(i+1)*SUBMAP_DATA_LENGTH]
            submap = self.load_one_submap(submap_data)
            self.submaps.append(submap)
            
    def load_magics_info(self, magics_info):
        MAGIC_DATA_LENGTH = 272 # 272 bytes
        
        number_of_magics = len(magics_info) // MAGIC_DATA_LENGTH
        print("Loading magics, number: ", number_of_magics)
        
        self.magics = []
        for i in range(number_of_magics):
            magic_data = magics_info[i*MAGIC_DATA_LENGTH:(i+1)*MAGIC_DATA_LENGTH]
            magic = self.load_one_magic(magic_data)
            self.magics.append(magic)
            
    def load_shops_info(self, shops_info):
        SHOP_DATA_LENGTH = 60 # 60 bytes
        
        number_of_shops = len(shops_info) // SHOP_DATA_LENGTH
        print("Loading shops, number: ", number_of_shops)
        
        self.shops = []
        for i in range(number_of_shops):
            shop_data = shops_info[i*SHOP_DATA_LENGTH:(i+1)*SHOP_DATA_LENGTH]
            shop = self.load_one_shop(shop_data)
            self.shops.append(shop)
            
    def decode_chinese_string(self, chinese_bytes):
        chinese_bytes = list(chinese_bytes)
        # remove the 0s at the beginning
        while chinese_bytes[0] == 0:
            chinese_bytes.pop(0)
            
        # remove the trailing 0s
        while chinese_bytes[-1] == 0:
            chinese_bytes.pop()
            
            
        
        try:
            if self.Encode != 65001:
                if self.Encode == 936:
                    # it is CP936 encoding
                    chinese_bytes = bytes(list(chinese_bytes))
                    chinese_str = chinese_bytes.decode("cp936")
                else:
                    # it is CP950 encoding
                    chinese_bytes = bytes(list(chinese_bytes))
                    chinese_str = chinese_bytes.decode("cp950")
            else:
                chinese_bytes = bytes(list(chinese_bytes))
                chinese_str = chinese_bytes.decode("utf-8")
        except:
            chinese_str = "DecodeError"
            
        return chinese_str
        
            
    def load_one_role(self, role_data_bytes):
        
        # original c++ code of the roles info data format:
        # int ID;
        # int HeadID, IncLife, UnUse;
        # char Name[20], Nick[20];
        # int Gender;    //性别 0-男 1 女 2 其他
        # int Level;
        # int Exp;
        # int HP, MaxHP, Hurt, Poison, PhysicalPower;
        # int ExpForMakeItem;
        # int Equip0, Equip1;
        # //int Frame[15];    //动作帧数，改为不在此处保存，故实际无用，另外延迟帧数对效果几乎无影响，废弃
        # int EquipMagic[4];     //装备武学
        # int EquipMagic2[4];    //装备被动武学
        # int EquipItem;         //装备物品
        # int Frame[6];          //帧数，现仅用于占位
        # int MPType, MP, MaxMP;
        # int Attack, Speed, Defence, Medicine, UsePoison, Detoxification, AntiPoison, Fist, Sword, Knife, Unusual, HiddenWeapon;
        # int Knowledge, Morality, AttackWithPoison, AttackTwice, Fame, IQ;
        # int PracticeItem;
        # int ExpForItem;
        # int MagicID[ROLE_MAGIC_COUNT], MagicLevel[ROLE_MAGIC_COUNT];
        # int TakingItem[ROLE_TAKING_ITEM_COUNT], TakingItemCount[ROLE_TAKING_ITEM_COUNT];
        
        current_role = {}
        
        current_role["ID"] = self.convert_byte_array_to_int(role_data_bytes[0:4])
        current_role["HeadID"] = self.convert_byte_array_to_int(role_data_bytes[4:8])
        current_role["IncLife"] = self.convert_byte_array_to_int(role_data_bytes[8:12])
        current_role["UnUse"] = self.convert_byte_array_to_int(role_data_bytes[12:16])
        if self.temp_name_bytes is None:
            self.temp_name_bytes = role_data_bytes[16:36]
        name_str = self.decode_chinese_string(role_data_bytes[16:36])
        current_role["Name"] = name_str
        nick_str = self.decode_chinese_string(role_data_bytes[36:56])
        current_role["Nick"] = nick_str
        current_role["Gender"] = self.convert_byte_array_to_int(role_data_bytes[56:60])
        current_role["Level"] = self.convert_byte_array_to_int(role_data_bytes[60:64])
        current_role["Exp"] = self.convert_byte_array_to_int(role_data_bytes[64:68])
        current_role["HP"] = self.convert_byte_array_to_int(role_data_bytes[68:72])
        current_role["MaxHP"] = self.convert_byte_array_to_int(role_data_bytes[72:76])
        current_role["Hurt"] = self.convert_byte_array_to_int(role_data_bytes[76:80])
        current_role["Poison"] = self.convert_byte_array_to_int(role_data_bytes[80:84])
        current_role["PhysicalPower"] = self.convert_byte_array_to_int(role_data_bytes[84:88])
        current_role["ExpForMakeItem"] = self.convert_byte_array_to_int(role_data_bytes[88:92])
        current_role["Equip0"] = self.convert_byte_array_to_int(role_data_bytes[92:96])
        current_role["Equip1"] = self.convert_byte_array_to_int(role_data_bytes[96:100])
        current_role["EquipMagic"] = []
        for i in range(4):
            current_role["EquipMagic"].append(self.convert_byte_array_to_int(role_data_bytes[100+i*4:104+i*4]))
        current_role["EquipMagic2"] = []
        for i in range(4):
            current_role["EquipMagic2"].append(self.convert_byte_array_to_int(role_data_bytes[116+i*4:120+i*4]))
        current_role["EquipItem"] = self.convert_byte_array_to_int(role_data_bytes[132:136])
        current_role["Frame"] = []
        for i in range(6):
            current_role["Frame"].append(self.convert_byte_array_to_int(role_data_bytes[136+i*4:140+i*4]))
        current_role["MPType"] = self.convert_byte_array_to_int(role_data_bytes[160:164])
        current_role["MP"] = self.convert_byte_array_to_int(role_data_bytes[164:168])
        current_role["MaxMP"] = self.convert_byte_array_to_int(role_data_bytes[168:172])
        current_role["Attack"] = self.convert_byte_array_to_int(role_data_bytes[172:176])
        current_role["Speed"] = self.convert_byte_array_to_int(role_data_bytes[176:180])
        current_role["Defence"] = self.convert_byte_array_to_int(role_data_bytes[180:184])
        current_role["Medicine"] = self.convert_byte_array_to_int(role_data_bytes[184:188])
        current_role["UsePoison"] = self.convert_byte_array_to_int(role_data_bytes[188:192])
        current_role["Detoxification"] = self.convert_byte_array_to_int(role_data_bytes[192:196])
        current_role["AntiPoison"] = self.convert_byte_array_to_int(role_data_bytes[196:200])
        current_role["Fist"] = self.convert_byte_array_to_int(role_data_bytes[200:204])
        current_role["Sword"] = self.convert_byte_array_to_int(role_data_bytes[204:208])
        current_role["Knife"] = self.convert_byte_array_to_int(role_data_bytes[208:212])
        current_role["Unusual"] = self.convert_byte_array_to_int(role_data_bytes[212:216])
        current_role["HiddenWeapon"] = self.convert_byte_array_to_int(role_data_bytes[216:220])
        current_role["Knowledge"] = self.convert_byte_array_to_int(role_data_bytes[220:224])
        current_role["Morality"] = self.convert_byte_array_to_int(role_data_bytes[224:228])
        current_role["AttackWithPoison"] = self.convert_byte_array_to_int(role_data_bytes[228:232])
        current_role["AttackTwice"] = self.convert_byte_array_to_int(role_data_bytes[232:236])
        current_role["Fame"] = self.convert_byte_array_to_int(role_data_bytes[236:240])
        current_role["IQ"] = self.convert_byte_array_to_int(role_data_bytes[240:244])
        current_role["PracticeItem"] = self.convert_byte_array_to_int(role_data_bytes[244:248])
        current_role["ExpForItem"] = self.convert_byte_array_to_int(role_data_bytes[248:252])
        
        # ROLE_MAGIC_COUNT = 4
        # ROLE_TAKING_ITEM_COUNT = 10
        
        current_role["MagicID"] = []
        for i in range(4):
            current_role["MagicID"].append(self.convert_byte_array_to_int(role_data_bytes[252+i*4:256+i*4]))
        current_role["MagicLevel"] = []
        for i in range(4):
            current_role["MagicLevel"].append(self.convert_byte_array_to_int(role_data_bytes[268+i*4:272+i*4]))
        current_role["TakingItem"] = []
        for i in range(10):
            current_role["TakingItem"].append(self.convert_byte_array_to_int(role_data_bytes[284+i*4:288+i*4]))
        current_role["TakingItemCount"] = []
        for i in range(10):
            current_role["TakingItemCount"].append(self.convert_byte_array_to_int(role_data_bytes[324+i*4:328+i*4]))
            
            
        
        return current_role
    
    def load_one_item(self, item_data_bytes):
        
        # original c++ code of the items info data format:
        # int ID;
        # char Name[40];
        # int Name1[10];
        # char Introduction[60];
        # int MagicID, HiddenWeaponEffectID, User, EquipType, ShowIntroduction;
        # int ItemType;    //0剧情，1装备，2秘笈，3药品，4暗器
        # int UnKnown5, UnKnown6, UnKnown7;
        # int AddHP, AddMaxHP, AddPoison, AddPhysicalPower, ChangeMPType, AddMP, AddMaxMP;
        # int AddAttack, AddSpeed, AddDefence, AddMedicine, AddUsePoison, AddDetoxification, AddAntiPoison;
        # int AddFist, AddSword, AddKnife, AddUnusual, AddHiddenWeapon, AddKnowledge, AddMorality, AddAttackTwice, AddAttackWithPoison;
        # int OnlySuitableRole, NeedMPType, NeedMP, NeedAttack, NeedSpeed, NeedUsePoison, NeedMedicine, NeedDetoxification;
        # int NeedFist, NeedSword, NeedKnife, NeedUnusual, NeedHiddenWeapon, NeedIQ;
        # int NeedExp, NeedExpForMakeItem, NeedMaterial;
        # int MakeItem[5], MakeItemCount[5];
        
        current_item = {}
        
        current_item["ID"] = self.convert_byte_array_to_int(item_data_bytes[0:4])   
        name_str = self.decode_chinese_string(item_data_bytes[4:44])
        current_item["Name"] = name_str
        # name1_str = self.decode_chinese_string(item_data_bytes[44:84])
        # current_item["Name1"] = name1_str
        current_item["Name1"] = []
        for i in range(10):
            current_item["Name1"].append(self.convert_byte_array_to_int(item_data_bytes[44+i*4:48+i*4]))
        introduction_str = self.decode_chinese_string(item_data_bytes[84:144])
        current_item["Introduction"] = introduction_str
        current_item["MagicID"] = self.convert_byte_array_to_int(item_data_bytes[144:148])
        current_item["HiddenWeaponEffectID"] = self.convert_byte_array_to_int(item_data_bytes[148:152])
        current_item["User"] = self.convert_byte_array_to_int(item_data_bytes[152:156])
        current_item["EquipType"] = self.convert_byte_array_to_int(item_data_bytes[156:160])
        current_item["ShowIntroduction"] = self.convert_byte_array_to_int(item_data_bytes[160:164])
        current_item["ItemType"] = self.convert_byte_array_to_int(item_data_bytes[164:168])
        current_item["UnKnown5"] = self.convert_byte_array_to_int(item_data_bytes[168:172])
        current_item["UnKnown6"] = self.convert_byte_array_to_int(item_data_bytes[172:176])
        current_item["UnKnown7"] = self.convert_byte_array_to_int(item_data_bytes[176:180])
        current_item["AddHP"] = self.convert_byte_array_to_int(item_data_bytes[180:184])
        current_item["AddMaxHP"] = self.convert_byte_array_to_int(item_data_bytes[184:188])
        current_item["AddPoison"] = self.convert_byte_array_to_int(item_data_bytes[188:192])
        current_item["AddPhysicalPower"] = self.convert_byte_array_to_int(item_data_bytes[192:196])
        current_item["ChangeMPType"] = self.convert_byte_array_to_int(item_data_bytes[196:200])
        current_item["AddMP"] = self.convert_byte_array_to_int(item_data_bytes[200:204])
        current_item["AddMaxMP"] = self.convert_byte_array_to_int(item_data_bytes[204:208])
        current_item["AddAttack"] = self.convert_byte_array_to_int(item_data_bytes[208:212])
        current_item["AddSpeed"] = self.convert_byte_array_to_int(item_data_bytes[212:216])
        current_item["AddDefence"] = self.convert_byte_array_to_int(item_data_bytes[216:220])
        current_item["AddMedicine"] = self.convert_byte_array_to_int(item_data_bytes[220:224])
        current_item["AddUsePoison"] = self.convert_byte_array_to_int(item_data_bytes[224:228])
        current_item["AddDetoxification"] = self.convert_byte_array_to_int(item_data_bytes[228:232])
        current_item["AddAntiPoison"] = self.convert_byte_array_to_int(item_data_bytes[232:236])
        current_item["AddFist"] = self.convert_byte_array_to_int(item_data_bytes[236:240])
        current_item["AddSword"] = self.convert_byte_array_to_int(item_data_bytes[240:244])
        current_item["AddKnife"] = self.convert_byte_array_to_int(item_data_bytes[244:248])
        current_item["AddUnusual"] = self.convert_byte_array_to_int(item_data_bytes[248:252])
        current_item["AddHiddenWeapon"] = self.convert_byte_array_to_int(item_data_bytes[252:256])
        current_item["AddKnowledge"] = self.convert_byte_array_to_int(item_data_bytes[256:260])
        current_item["AddMorality"] = self.convert_byte_array_to_int(item_data_bytes[260:264])
        current_item["AddAttackTwice"] = self.convert_byte_array_to_int(item_data_bytes[264:268])
        current_item["AddAttackWithPoison"] = self.convert_byte_array_to_int(item_data_bytes[268:272])
        current_item["OnlySuitableRole"] = self.convert_byte_array_to_int(item_data_bytes[272:276])
        current_item["NeedMPType"] = self.convert_byte_array_to_int(item_data_bytes[276:280])
        current_item["NeedMP"] = self.convert_byte_array_to_int(item_data_bytes[280:284])
        current_item["NeedAttack"] = self.convert_byte_array_to_int(item_data_bytes[284:288])
        current_item["NeedSpeed"] = self.convert_byte_array_to_int(item_data_bytes[288:292])
        current_item["NeedUsePoison"] = self.convert_byte_array_to_int(item_data_bytes[292:296])
        current_item["NeedMedicine"] = self.convert_byte_array_to_int(item_data_bytes[296:300])
        current_item["NeedDetoxification"] = self.convert_byte_array_to_int(item_data_bytes[300:304])
        current_item["NeedFist"] = self.convert_byte_array_to_int(item_data_bytes[304:308])
        current_item["NeedSword"] = self.convert_byte_array_to_int(item_data_bytes[308:312])
        current_item["NeedKnife"] = self.convert_byte_array_to_int(item_data_bytes[312:316])
        current_item["NeedUnusual"] = self.convert_byte_array_to_int(item_data_bytes[316:320])
        current_item["NeedHiddenWeapon"] = self.convert_byte_array_to_int(item_data_bytes[320:324])
        current_item["NeedIQ"] = self.convert_byte_array_to_int(item_data_bytes[324:328])
        current_item["NeedExp"] = self.convert_byte_array_to_int(item_data_bytes[328:332])
        current_item["NeedExpForMakeItem"] = self.convert_byte_array_to_int(item_data_bytes[332:336])
        current_item["NeedMaterial"] = self.convert_byte_array_to_int(item_data_bytes[336:340])
        current_item["MakeItem"] = []
        for i in range(5):
            current_item["MakeItem"].append(self.convert_byte_array_to_int(item_data_bytes[340+i*4:344+i*4]))
        current_item["MakeItemCount"] = []
        for i in range(5):
            current_item["MakeItemCount"].append(self.convert_byte_array_to_int(item_data_bytes[360+i*4:364+i*4]))
        
        return current_item
        
    def load_one_submap(self, submap_data_bytes):
        # original c++ code of the submaps info data format:
        # int ID;
	    # char Name[20];
	    # int ExitMusic, EntranceMusic;
	    # int JumpSubMap, EntranceCondition;
	    # int MainEntranceX1, MainEntranceY1, MainEntranceX2, MainEntranceY2;
	    # int EntranceX, EntranceY;
	    # int ExitX[3], ExitY[3];
	    # int JumpX, JumpY, JumpReturnX, JumpReturnY;
     
        current_submap = {}
        
        current_submap["ID"] = self.convert_byte_array_to_int(submap_data_bytes[0:4])
        name_str = self.decode_chinese_string(submap_data_bytes[4:24])
        current_submap["Name"] = name_str
        current_submap["ExitMusic"] = self.convert_byte_array_to_int(submap_data_bytes[24:28])
        current_submap["EntranceMusic"] = self.convert_byte_array_to_int(submap_data_bytes[28:32])
        current_submap["JumpSubMap"] = self.convert_byte_array_to_int(submap_data_bytes[32:36])
        current_submap["EntranceCondition"] = self.convert_byte_array_to_int(submap_data_bytes[36:40])
        current_submap["MainEntranceX1"] = self.convert_byte_array_to_int(submap_data_bytes[40:44])
        current_submap["MainEntranceY1"] = self.convert_byte_array_to_int(submap_data_bytes[44:48])
        current_submap["MainEntranceX2"] = self.convert_byte_array_to_int(submap_data_bytes[48:52])
        current_submap["MainEntranceY2"] = self.convert_byte_array_to_int(submap_data_bytes[52:56])
        current_submap["EntranceX"] = self.convert_byte_array_to_int(submap_data_bytes[56:60])
        current_submap["EntranceY"] = self.convert_byte_array_to_int(submap_data_bytes[60:64])
        current_submap["ExitX"] = []
        for i in range(3):
            current_submap["ExitX"].append(self.convert_byte_array_to_int(submap_data_bytes[64+i*4:68+i*4]))
        current_submap["ExitY"] = []
        for i in range(3):
            current_submap["ExitY"].append(self.convert_byte_array_to_int(submap_data_bytes[76+i*4:80+i*4]))
        current_submap["JumpX"] = self.convert_byte_array_to_int(submap_data_bytes[88:92])
        current_submap["JumpY"] = self.convert_byte_array_to_int(submap_data_bytes[92:96])
        current_submap["JumpReturnX"] = self.convert_byte_array_to_int(submap_data_bytes[96:100])
        current_submap["JumpReturnY"] = self.convert_byte_array_to_int(submap_data_bytes[100:104])
        
        
        
        return current_submap
    
    
    def load_one_magic(self, magic_data_bytes):
        # original c++ code of the magics info data format:
        # int ID;
        # char Name[20];
        # int Unknown[5];
        # int SoundID;
        # int MagicType;    //1-拳，2-剑，3-刀，4-特殊
        # int EffectID;
        # int HurtType;          //0-普通，1-吸取MP
        # int AttackAreaType;    //0-点，1-线，2-十字，3-面
        # int NeedMP, WithPoison;
        # int Attack[10], SelectDistance[10], AttackDistance[10], AddMP[10], HurtMP[10];
        
        current_magic = {}
        
        current_magic["ID"] = self.convert_byte_array_to_int(magic_data_bytes[0:4])
        name_str = self.decode_chinese_string(magic_data_bytes[4:24])
        current_magic["Name"] = name_str
        current_magic["Unknown"] = []
        for i in range(5):
            current_magic["Unknown"].append(self.convert_byte_array_to_int(magic_data_bytes[24+i*4:28+i*4]))
        current_magic["SoundID"] = self.convert_byte_array_to_int(magic_data_bytes[44:48])
        current_magic["MagicType"] = self.convert_byte_array_to_int(magic_data_bytes[48:52])
        current_magic["EffectID"] = self.convert_byte_array_to_int(magic_data_bytes[52:56])
        current_magic["HurtType"] = self.convert_byte_array_to_int(magic_data_bytes[56:60])
        current_magic["AttackAreaType"] = self.convert_byte_array_to_int(magic_data_bytes[60:64])
        current_magic["NeedMP"] = self.convert_byte_array_to_int(magic_data_bytes[64:68])
        current_magic["WithPoison"] = self.convert_byte_array_to_int(magic_data_bytes[68:72])
        current_magic["Attack"] = []
        for i in range(10):
            current_magic["Attack"].append(self.convert_byte_array_to_int(magic_data_bytes[72+i*4:76+i*4]))
        current_magic["SelectDistance"] = []
        for i in range(10):
            current_magic["SelectDistance"].append(self.convert_byte_array_to_int(magic_data_bytes[112+i*4:116+i*4]))
        current_magic["AttackDistance"] = []
        for i in range(10):
            current_magic["AttackDistance"].append(self.convert_byte_array_to_int(magic_data_bytes[152+i*4:156+i*4]))
        current_magic["AddMP"] = []
        for i in range(10):
            current_magic["AddMP"].append(self.convert_byte_array_to_int(magic_data_bytes[192+i*4:196+i*4]))
        current_magic["HurtMP"] = []
        for i in range(10):
            current_magic["HurtMP"].append(self.convert_byte_array_to_int(magic_data_bytes[232+i*4:236+i*4]))

        return current_magic
    
    
    # int ItemID[5], Total[5], Price[5];
    def load_one_shop(self, shop_data_bytes):
        current_shop = {}
        
        current_shop["ItemID"] = []
        for i in range(5):
            current_shop["ItemID"].append(self.convert_byte_array_to_int(shop_data_bytes[i*4:i*4+4]))
        current_shop["Total"] = []
        for i in range(5):
            current_shop["Total"].append(self.convert_byte_array_to_int(shop_data_bytes[20+i*4:24+i*4]))
        current_shop["Price"] = []
        for i in range(5):
            current_shop["Price"].append(self.convert_byte_array_to_int(shop_data_bytes[40+i*4:44+i*4]))
        
        return current_shop
        
            
                