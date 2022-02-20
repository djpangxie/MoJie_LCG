from main import *


class Hero(Hero_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "督希尔.jpg"  # 英雄卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 英雄卡牌的原始图像
        self.card_name = "督希尔"  # 英雄的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.initial_threat = 8  # 英雄的初始威胁值
        self.willpower = 1  # 英雄的意志力
        self.attack_force = 2  # 英雄的攻击力
        self.defense_force = 1  # 英雄的防御力
        self.health_point = 4  # 英雄的生命值
        self.resource_symbol = "精神"  # 资源符号，表示本英雄的资源池中的资源标记(及英雄自身)隶属于哪个影响力派系
        self.card_attribute = ("洛汗", "战士")  # 英雄的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 英雄的规则关键词，表示英雄有些什么关键词
        self.rule_mark = ("攻击场景区",)  # 英雄的规则效果标志，表示英雄有些什么效果
        self.card_type = "英雄"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "当督希尔单独攻击时，他能将场景区中的敌军作为目标。这样做时，他获得+1攻击力。"

        # 剧情描述的斜体文字
        self.describe_text = "将军们立刻骑马来到渡口晋见王上，并且带来了甘道夫的口信；率领众将前来的是哈洛谷的领主督希尔。 ——《王者再临》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._increment = 0

    # 重置卡牌
    def reset_card(self):
        super().reset_card()
        self._increment = 0

    # 卡牌被选中时，导入卡牌按钮树
    def import_button(self):
        super().import_button()
        if self.main_game.threat_area.current_phase == 5 and self.main_game.threat_area.current_step == 4 and not self.main_game.threat_area.action_window and self in self.main_game.role_area.card_group and "宣告攻击" not in self.active_condition and "已横置" not in self.active_condition and (
                not hasattr(self.main_game.threat_area, "enemy") or not self.main_game.threat_area.enemy) and \
                self.main_game.button_option.buttons[0][0] != "单独攻击":
            self.main_game.button_option.buttons.insert(0, ("单独攻击", None))
            self.main_game.button_option._set_current_button()

    # 卡牌被选中时，侦听按钮树的选项选择
    def listening_button(self):
        if self.main_game.button_option.option // 100000:
            for (num, button) in enumerate(self.main_game.button_option.buttons):
                if button[0] == "单独攻击" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["单独攻击", 0, 0, False, 0, 0]
                    self.main_game.button_option.reset()
                    self.main_game.select_card = None
        super().listening_button()

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self._increment and "宣告攻击" not in self.active_condition:
            self.active_attack_force -= self._increment
            if self.active_attack_force < 0:
                self.active_attack_force = 0
            self.update_mask()
            self._increment = 0

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "单独攻击" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                enemys = []
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "敌军" and "防御中" not in card.active_condition and "已防御" not in card.active_condition:
                        enemys.append(card)
                if enemys:
                    self.select_enemy = self.main_game.card_select(enemys)
                    self.main_game.information = [0, "敌军卡牌将要选为攻击目标", self.select_enemy]
                    self.card_order[1] += 1
                else:
                    self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "单独攻击" and self.card_order[1] == 1:
            if self.card_order[2]:
                del self.select_enemy
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.threat_area.enemy = self.select_enemy
                self.select_enemy.active_condition["防御中"] = [self]
                self.select_enemy.update_mask()
                self.main_game.information = [0, "敌军卡牌选为攻击目标后", self.select_enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "单独攻击" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if "已横置" not in self.active_condition:
                    self.main_game.information = [0, "英雄卡牌将要横置", self, self]
                else:
                    self.card_order[2] = 1
                self.card_order[1] += 1
        elif self.card_order[0] == "单独攻击" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if "已横置" not in self.active_condition:
                    self.active_condition["已横置"] = None
                    self.update_mask()
                    self.main_game.information = [0, "英雄卡牌横置后", self, self]
                else:
                    self.card_order[2] = 1
                self.card_order[1] += 1
        elif self.card_order[0] == "单独攻击" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要宣告攻击", self, self.select_enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "单独攻击" and self.card_order[1] == 5:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.active_condition["宣告攻击"] = [self.select_enemy]
                self.update_mask()
                self.main_game.information = [0, "英雄卡牌宣告攻击后", self, self.select_enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "单独攻击" and self.card_order[1] == 6:
            if self.card_order[2]:
                self.select_enemy.active_condition.pop("防御中")
                self.select_enemy.update_mask()
                del self.select_enemy
                del self.main_game.threat_area.enemy
                self.main_game.threat_area.order[4] = 0
                if "宣告攻击" in self.active_condition:
                    self.active_condition.pop("宣告攻击")
                    self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.active_attack_force += 1
                self.update_mask()
                self._increment += 1
                del self.select_enemy
                self.main_game.information = [0, "将要离开宣告攻击目标步骤", "order"]
                self.main_game.threat_area.order[4] += 1
                self.card_order = [None, 0, 0, None, 0, 0]
