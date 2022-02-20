from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "多尔哥多驯兽师.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (1, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "多尔哥多驯兽师"  # 这张卡的名称
        self.clash_value = 35  # 这张卡的交锋值
        self.threat_force = 2  # 这张卡的威胁力
        self.attack_force = 3  # 这张卡的攻击力
        self.defense_force = 1  # 这张卡的防御力
        self.health_point = 5  # 这张卡的生命值
        self.encounter_symbol = "半兽人"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("多尔哥多", "半兽人")  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("强制",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "敌军"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "强制：当多尔哥多驯兽师攻击时，额外分配一张暗影牌。"

        # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.shadow_text = ""

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.main_game.information and self.main_game.information[
            1] == "将要离开选择敌军步骤" and self.main_game.information[
            2] == "order" and self.main_game.threat_area.enemy == self and str(self) not in self.main_game.information:
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.card_order = ["强制", 0, 0, False, 0, 0]

    # 执行这张卡片的效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "强制" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌将要执行强制效果", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "将要分配暗影牌", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                shadow_card = Print_Card(self.main_game)
                if self.main_game.encounter_area.encounter_deck:
                    shadow_card.card_target = self.main_game.encounter_area.encounter_deck.pop(0)
                shadow_card.card_image = self.main_game.computer_card_image.copy()
                shadow_card.card_type = "暗影牌"
                shadow_card.active_condition["暗影牌"] = [self]
                if "分配暗影" in self.active_condition:
                    self.active_condition["分配暗影"].append(shadow_card)
                else:
                    self.active_condition["分配暗影"] = [shadow_card]
                    self.update_mask()
                if self.main_game.card_estimate(self)[self]:
                    self.main_game.card_estimate(self)[self].append(shadow_card)
                else:
                    self.main_game.card_estimate(self)[self] = [shadow_card]
                self.main_game.information = [0, "分配暗影牌后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌强制效果结算后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "强制" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                self.card_order = [None, 0, 0, None, 0, 0]
