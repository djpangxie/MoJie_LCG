from main import *


class Enemy(Enemy_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "幽暗密林山区.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_amount = (3, 3, 3)  # 这张卡牌在简单、普通和噩梦难度下分别放多少张
        self.card_name = "幽暗密林山区"  # 这张卡的名称
        self.threat_force = 2  # 这张卡的威胁力
        self.task_point = 3  # 任务点，表示探索完该地区需要的进度标记数量
        self.encounter_symbol = "蜘蛛"  # 遭遇符号，表示属于哪类遭遇牌，与任务牌的遭遇信息对应
        self.card_attribute = ("森林", "山脉")  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ("探索", "响应")  # 这张卡片的规则效果标志，表示其有些什么效果
        self.victory_points = 0  # 表示这张卡牌的胜利点(如果有的话)
        self.card_type = "地区"  # 卡牌类型，表明本卡牌是敌军、地区、阴谋还是目标

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "探索：展示遭遇牌组顶端的一张卡牌并加入场景区，以探索本地区。\n响应：在幽暗密林山区作为已探索地区离场后，每位玩家可以从他牌组顶端的五张卡牌中搜寻一张卡牌并加入他的手牌。将余下的卡牌洗回他们拥有者的牌组。"

        # 剧情描述的斜体文字
        self.describe_text = ""

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._successful = False

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_task_point > 0 and self.main_game.information and self.main_game.information[1] == "地区卡牌将要激活" and self.main_game.information[2] == self and str(self) not in self.main_game.information:
            self.pause_card = self
            self.pause_card_order = self.card_order
            self.card_order = ["激活", 0, 0, False, 0, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None
        elif self.main_game.information and self.main_game.information[1] == "地区卡牌已探索后" and self.main_game.information[2] == self and str(self) not in self.main_game.information:
            self.main_game.response_conflict = True
            self.pause_card = self
            self.pause_card_order = self.card_order
            self.card_order = ["响应", 0, 0, False, 0, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None

    # 执行这张卡片的效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "激活" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.information = [0, "遭遇卡牌将要展示", self, self.main_game.encounter_area.encounter_deck[0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "激活" and self.card_order[1] == 1:
            if self.card_order[2]:
                if self.main_game.encounter_area.encounter_deck:
                    self.main_game.encounter_area.encounter_deck[0].reset_card()
                    self.main_game.encounter_area.encounter_deck[0].update_mask()
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.encounter_area.encounter_deck:
                    self.encounter_card = self.main_game.encounter_area.encounter_deck.pop(0)
                    self.main_game.card_exhibition(self.encounter_card, self.main_game.settings.card_exhibition_time)
                    self.main_game.scenario_area.card_group[self.encounter_card] = None
                    self.main_game.information = [0, "遭遇卡牌展示后", self, self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "激活" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌将要放置进场", self, self.encounter_card]
                self.card_order[1] += 1
        elif self.card_order[0] == "激活" and self.card_order[1] == 3:
            if self.card_order[2]:
                if hasattr(self, "encounter_card"):
                    self.main_game.scenario_area.card_group.pop(self.encounter_card)
                    self.encounter_card.reset_card()
                    self.encounter_card.update_mask()
                    if self.main_game.encounter_area.encounter_deck:
                        self.main_game.encounter_area.encounter_deck.insert(0, self.encounter_card)
                        random.shuffle(self.main_game.encounter_area.encounter_deck)
                    else:
                        self.main_game.encounter_area.encounter_deck = [self.encounter_card]
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "encounter_card") and self.encounter_card.card_type != "阴谋":
                    self.main_game.information = [0, self.encounter_card.card_type + "卡牌放置进场后", self, self.encounter_card]
                    self._successful = True
                self.card_order[1] += 1
        elif self.card_order[0] == "激活" and self.card_order[1] == 4:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if hasattr(self, "encounter_card"):
                    del self.encounter_card
                if self._successful:
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
                self._successful = False
        elif self.card_order[0] == "响应" and self.card_order[1] == 0:
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
                    self.card_order[1] += 2
                    self.main_game.button_option.reset()
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                cards = []
                if self.main_game.playerdeck_area.player_deck:
                    for (num, card) in enumerate(self.main_game.playerdeck_area.player_deck):
                        cards.append(card)
                        if num > 3:
                            break
                if cards:
                    select_card = self.main_game.card_select(cards)
                    self.main_game.playerdeck_area.player_deck.remove(select_card)
                    self.main_game.hand_area.card_group[select_card] = None
                    random.shuffle(self.main_game.playerdeck_area.player_deck)
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.response_pause = False
                self.pause_card.card_order = self.pause_card_order
                self.pause_card_order = None
                self.pause_card = None
                self.main_game.information = self.copy_information
                self.main_game.information.append(str(self))
                self.main_game.information[0] = 0
                self.copy_information = None
