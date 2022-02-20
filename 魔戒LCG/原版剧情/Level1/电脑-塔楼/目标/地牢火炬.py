from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "地牢火炬.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (1, 1, 1)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "地牢火炬"  # 这张卡的名称
        self.encounter_symbol = "塔楼"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("物品",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ("守护", "限制")  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("行动", "强制")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = "目标"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "守护.限制.\n行动：当本目标未附属时，上升2点你的威胁等级，以获取本目标。获取时，将地牢火炬附属到你控制的一名英雄上。（视为一张附属牌。如果附属解除，将地牢火炬返回场景区。）\n强制：在每回合结束时，所附属英雄控制者的威胁等级上升２点。"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌被选中时，导入卡牌按钮树
    def import_button(self):
        super().import_button()
        if self.main_game.threat_area.action_window and "行动" in self.rule_mark and self.main_game.card_estimate(
                self) is not None and "附属到" not in self.active_condition and "已横置" not in self.active_condition and "行动后" not in self.active_condition and "暗影牌" not in self.active_condition and \
                self.main_game.button_option.buttons[0][0] != "获取":
            self.main_game.button_option.buttons.insert(0, ("获取", None))
            self.main_game.button_option._set_current_button()

    # 卡牌被选中时，侦听按钮树的选项选择
    def listening_button(self):
        if self.main_game.button_option.option // 100000:
            for (num, button) in enumerate(self.main_game.button_option.buttons):
                if button[0] == "获取" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["获取", 0, 0, False, 0, 0]
                    self.main_game.button_option.reset()
                    self.main_game.select_card = None
        super().listening_button()

    # 执行这张卡片的效果
    def run_card_order(self):
        if self.card_order[0] == "获取" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "玩家将要上升威胁等级", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "获取" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.threat_area.threat_value += 2
                self.main_game.information = [0, "玩家上升威胁等级后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "获取" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                heros = []
                for hero in self.main_game.role_area.hero_group:
                    if "免疫" not in hero.rule_mark:
                        heros.append(hero)
                if heros:
                    self.select_hero = self.main_game.card_select(heros)
                    self.main_game.information = [0, "目标卡牌将要附属", self, self.select_hero]
                else:
                    self.card_order[2] = 1
                self.card_order[1] += 1
        elif self.card_order[0] == "获取" and self.card_order[1] == 3:
            if self.card_order[2]:
                if hasattr(self, "select_hero"):
                    del self.select_hero
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self.main_game.card_estimate(self.select_hero)[self.select_hero]:
                    self.main_game.card_estimate(self.select_hero)[self.select_hero].append(self)
                else:
                    self.main_game.card_estimate(self.select_hero)[self.select_hero] = [self]
                if "被附属" not in self.select_hero.active_condition or not self.select_hero.active_condition["被附属"]:
                    self.select_hero.active_condition["被附属"] = [self]
                else:
                    self.select_hero.active_condition["被附属"].append(self)
                self.active_condition["附属到"] = [self.select_hero]
                if "类型+" in self.active_condition:
                    self.active_condition["类型+"].append("附属")
                else:
                    self.active_condition["类型+"] = ["附属"]
                self.update_mask()
                self.select_hero.update_mask()
                self.main_game.information = [0, "目标卡牌附属后", self, self.select_hero]
                self.main_game.card_estimate(self).pop(self)
                self.card_order[1] += 1
        elif self.card_order[0] == "获取" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                num = 0
                affiliate = []
                for target in self.select_hero.active_condition["被附属"]:
                    if "限制" in target.rule_keyword:
                        affiliate.append(target)
                        num += 1
                if num > 2:
                    del self.select_hero
                    self.card_order = [None, 0, 0, None, 0, 0]
                    select_affiliate = self.main_game.card_select(affiliate)
                    select_affiliate.card_order = ["弃除附属", 0, 0, False, 0, 0]
                else:
                    del self.select_hero
                    self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "弃除附属" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "目标卡牌将要被弃除", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "弃除附属" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                for hero in self.active_condition["附属到"]:
                    hero.active_condition["被附属"].remove(self)
                    if not hero.active_condition["被附属"]:
                        hero.active_condition.pop("被附属")
                    self.main_game.card_estimate(hero)[hero].remove(self)
                    hero.update_mask()
                self.reset_card()
                self.update_mask()
                self.main_game.scenario_area.card_group[self] = None
                self.main_game.information = [0, "目标卡牌被弃除后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
