from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "老林路.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (2, 2, 2)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "老林路"  # 这张卡的名称
        self.threat_force = 1  # 这张卡的威胁力
        self.task_point = 3  # 任务点，表示探索完该地区需要的进度标记数量
        self.encounter_symbol = "树"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("森林",)  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("响应",)  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "地区"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "响应：在你探索到老林路后，起始玩家可以选择并重置一名他控制的角色。"

        # 剧情描述的斜体文字
        self.describe_text = "...比翁警告他们，半兽人现在经常利用这条道路来旅行；而且他也听说，老林路本身在东边的区域已经被森林给遮蔽了，如果沿着路走，将会来到无路可穿越的沼泽。 ——《哈比人》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_task_point > 0 and self.main_game.information and self.main_game.information[1] == "地区卡牌激活后" and \
                self.main_game.information[2] == self and "响应后" not in self.active_condition:
            self.main_game.response_conflict = True
            self.card_order = ["响应", 0, 0, False, 0, 0]
            self.active_condition["响应后"] = None

    # 执行这张卡片的响应效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "响应" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif self.main_game.response_pause != True:
                self.main_game.response_pause = True
                self.main_game.button_option.import_button(str(self), (
                    ("响应-" + self.card_name, None), ("不响应-" + self.card_name, None)))
                if self.main_game.button_option.option // 100000 == 1:
                    self.card_order[1] += 1
                    self.main_game.button_option.reset()
                elif self.main_game.button_option.option // 100000 == 2:
                    self.card_order[1] += 3
                    self.main_game.button_option.reset()
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                roles = []
                for card in self.main_game.role_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" in card.active_condition:
                        roles.append(card)
                for card in self.main_game.clash_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" in card.active_condition:
                        roles.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" in card.active_condition:
                        roles.append(card)
                for card in self.main_game.hand_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "已横置" in card.active_condition:
                        roles.append(card)
                if roles:
                    self.select_role = self.main_game.card_select(roles)
                    self.main_game.information = [0, self.select_role.card_type + "卡牌将要重置", self, self.select_role]
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "select_role") and "已横置" in self.select_role.active_condition:
                    self.select_role.active_condition.pop("已横置")
                    self.select_role.update_mask()
                    self.main_game.information = [0, self.select_role.card_type + "卡牌重置后", self, self.select_role]
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if hasattr(self, "select_role"):
                    del self.select_role
                self.main_game.response_pause = False
                self.active_condition.pop("响应后")
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
