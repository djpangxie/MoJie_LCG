from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "乌夫塔克酋长.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (0, 1, 1)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "乌夫塔克酋长"  # 这张卡的名称
        self.clash_value = 35  # 这张卡的交锋值
        self.threat_force = 2  # 这张卡的威胁力
        self.attack_force = 3  # 这张卡的攻击力
        self.defense_force = 3  # 这张卡的防御力
        self.health_point = 6  # 这张卡的生命值
        self.encounter_symbol = "半兽人"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("多尔哥多", "半兽人")  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("永久", "强制")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 4  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "乌夫塔克酋长每有1枚资源标记，其获得+2攻击力。\n强制：在乌夫塔克酋长攻击后，放置1枚资源标记到乌夫塔克酋长上。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = ""

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.resource_mark = 0

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.main_game.information and self.main_game.information[1][-5:] == "卡牌攻击后" and self.main_game.information[2] == self and str(self) not in self.main_game.information:
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["强制", 0, 0, False, 0, 0]
        elif "资源标记" in self.active_condition and self.resource_mark != self.active_condition["资源标记"][0]:
            self.active_attack_force += (self.active_condition["资源标记"][0] - self.resource_mark) * 2
            if self.active_attack_force < 0:
                self.active_attack_force = 0
            self.update_mask()
            self.resource_mark = self.active_condition["资源标记"][0]

    # 执行这张卡片的效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "强制" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌将要执行强制效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if "资源标记" in self.active_condition:
                    self.active_condition["资源标记"][0] += 1
                else:
                    self.active_condition["资源标记"] = [1]
                    self.update_mask()
                self.main_game.information = [0, "敌军卡牌强制效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                self.card_order = [None, 0, 0, None, 0, 0]
