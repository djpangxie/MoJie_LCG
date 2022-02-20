from main import *


class Hero(Hero_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "埃莉诺.jpg"  # 英雄卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 英雄卡牌的原始图像
        self.card_name = "埃莉诺"  # 英雄的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.initial_threat = 7  # 英雄的初始威胁值
        self.willpower = 1  # 英雄的意志力
        self.attack_force = 1  # 英雄的攻击力
        self.defense_force = 2  # 英雄的防御力
        self.health_point = 3  # 英雄的生命值
        self.resource_symbol = "精神"  # 资源符号，表示本英雄的资源池中的资源标记(及英雄自身)隶属于哪个影响力派系
        self.card_attribute = ("刚铎", "贵族")  # 英雄的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 英雄的规则关键词，表示英雄有些什么关键词
        self.rule_mark = ("响应",)  # 英雄的规则效果标志，表示英雄有些什么效果
        self.card_type = "英雄"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "响应：横置埃莉诺，以取消一张刚从遭遇牌组展示的阴谋牌的“展示后”效果。然后，弃除该卡牌，并以遭遇牌组的下一张卡牌代替。"

        # 剧情描述的斜体文字
        self.describe_text = "你说刚铎逐渐没落，但刚铎依然挺立，它没落时的国力依旧十分强大。 ——波罗莫，《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.main_game.on_spot(self) and "已横置" not in self.active_condition and self.main_game.information and "阴谋卡牌将要执行展示后效果" in self.main_game.information[1] and str(self) not in self.main_game.information:
            self.pause_card = self.main_game.information[2]
            self.pause_card_order = self.main_game.information[2].card_order
            self.main_game.information[2].card_order = [None, -1, 0, None, -1, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None
            self.main_game.response_conflict = True
            self.card_order = ["响应", 0, 0, False, 0, 0]

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
                    self.main_game.button_option.reset()
                    self.card_order[1] += 1
                elif self.main_game.button_option.option // 100000 == 2:
                    self.main_game.button_option.reset()
                    self.card_order[1] += 3
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if "已横置" not in self.active_condition:
                    self.main_game.information = [0, "英雄卡牌将要横置", self, self]
                else:
                    self.card_order[2] = 1
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if "已横置" not in self.active_condition:
                    self.active_condition["已横置"] = None
                    self.update_mask()
                    self.main_game.information = [0, "英雄卡牌横置后", self, self]
                    self.pause_card_order[2] = 1
                    self.pause_card_order[3] = False
                    if self.pause_card.pause_card:
                        if self.pause_card.pause_card_order[3]:
                            self.pause_card.pause_card_order[4] -= 2
                        else:
                            self.pause_card.pause_card_order[1] -= 2
                    else:
                        if self.main_game.threat_area.order[3]:
                            self.main_game.threat_area.order[4] -= 2
                        else:
                            self.main_game.threat_area.order[1] -= 2
                    self.pause_card.card_order = self.pause_card_order
                    self.pause_card = None
                    self.pause_card_order = None
                    self.copy_information = None
                    self.main_game.response_pause = False
                    self.card_order = [None, 0, 0, None, 0, 0]
                else:
                    self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.pause_card.card_order = self.pause_card_order
                self.pause_card = None
                self.pause_card_order = None
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
                self.main_game.response_pause = False
                self.card_order = [None, 0, 0, None, 0, 0]
