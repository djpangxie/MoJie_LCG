from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "密布蛛网的森林.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (2, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "密布蛛网的森林"  # 这张卡的名称
        self.threat_force = 2  # 这张卡的威胁力
        self.task_point = 2  # 任务点，表示探索完该地区需要的进度标记数量
        self.encounter_symbol = "蜘蛛"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("森林",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("探索",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "地区"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "探索：每位玩家必须横置一名他控制的英雄，以探索本地区。"

        # 剧情描述的斜体文字
        self.describe_text = "随着他越来越靠近，他才知道那是由层层叠叠的蜘蛛网所构成的。 ——《哈比人》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_task_point > 0 and self.main_game.information and self.main_game.information[1] == "地区卡牌将要激活" and \
                self.main_game.information[2] == self and str(self) not in self.main_game.information:
            self.pause_card = self
            self.pause_card_order = self.card_order
            self.card_order = ["激活", 0, 0, False, 0, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None

    # 执行这张卡片的响应效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "激活" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                heros = []
                for card in self.main_game.role_area.card_group:
                    if card.card_type == "英雄" and "已横置" not in card.active_condition:
                        heros.append(card)
                for card in self.main_game.clash_area.card_group:
                    if card.card_type == "英雄" and "已横置" not in card.active_condition:
                        heros.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "英雄" and "已横置" not in card.active_condition:
                        heros.append(card)
                if heros:
                    self.select_hero = self.main_game.card_select(heros)
                    self.main_game.information = [0, "英雄卡牌将要横置", self, self.select_hero]
                self.card_order[1] += 1
        elif self.card_order[0] == "激活" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "select_hero") and "已横置" not in self.select_hero.active_condition:
                    self.select_hero.active_condition["已横置"] = None
                    self.select_hero.update_mask()
                    self.main_game.information = [0, "英雄卡牌横置后", self, self.select_hero]
                    self.select_hero = "OK"
                self.card_order[1] += 1
        elif self.card_order[0] == "激活" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if hasattr(self, "select_hero") and self.select_hero == "OK":
                    self.pause_card.card_order = self.pause_card_order
                    self.pause_card_order = None
                    self.pause_card = None
                    self.main_game.information = self.copy_information
                    self.main_game.information.append(str(self))
                    self.main_game.information[0] = 0
                    self.copy_information = None
                else:
                    self.pause_card = None
                    self.pause_card_order = None
                    self.copy_information = None
                    self.card_order = [None, 0, 0, None, 0, 0]
                if hasattr(self, "select_hero"):
                    del self.select_hero
