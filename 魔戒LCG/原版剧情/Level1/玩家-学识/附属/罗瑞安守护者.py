from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "罗瑞安守护者.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "罗瑞安守护者"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 1  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "学识"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.card_attribute = ("头衔",)  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "附属"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "附属到一名英雄上。\n行动：从你的手牌中弃除一张卡牌，以使所附属英雄获得+1防御力或+1意志力直到本阶段结束。每个阶段限制3次。"

        # 剧情描述的斜体文字
        self.describe_text = "“千万别污蔑凯兰崔尔女皇！”亚拉冈严厉地说，“除非人们自己将邪气带进来，那么，这个人就要小心了！” ——《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.phase_mark = None
        self.limit_number = 3
        self._increment = [0, 0]

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.phase_mark is not None and self.main_game.threat_area.current_phase != self.phase_mark:
            if "附属到" in self.active_condition:
                self.active_condition["附属到"][0].active_defense_force -= self._increment[0]
                if self.active_condition["附属到"][0].active_defense_force < 0:
                    self.active_condition["附属到"][0].active_defense_force = 0
                self.active_condition["附属到"][0].active_willpower -= self._increment[1]
                if self.active_condition["附属到"][0].active_willpower < 0:
                    self.active_condition["附属到"][0].active_willpower = 0
                self.active_condition["附属到"][0].update_mask()
            if "行动后" in self.active_condition:
                self.active_condition.pop("行动后")
                self.update_mask()
            self._increment = [0, 0]
            self.limit_number = 3
            self.phase_mark = None
        elif not self.limit_number and "行动后" not in self.active_condition:
            self.active_condition["行动后"] = None
            self.update_mask()
            self.main_game.button_option.reset()

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "打出附属后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                heros = []
                for hero in self.main_game.role_area.hero_group:
                    if "免疫" not in hero.rule_mark:
                        heros.append(hero)
                if heros:
                    self.select_hero = self.main_game.card_select(heros)
                    self.main_game.information = [0, "附属卡牌将要附属", self, self.select_hero]
                else:
                    self.card_order[2] = 1
                self.card_order[1] += 1
        elif self.card_order[0] == "打出附属后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.main_game.hand_area.card_group.pop(self)
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = [self]
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
                self.update_mask()
                self.select_hero.update_mask()
                self.main_game.information = [0, "附属卡牌附属后", self, self.select_hero]
                self.main_game.hand_area.card_group.pop(self)
                del self.select_hero
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "弃除附属" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "附属卡牌将要被弃除", self]
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
                    hero.active_defense_force -= self._increment[0]
                    if hero.active_defense_force < 0:
                        hero.active_defense_force = 0
                    hero.active_willpower -= self._increment[1]
                    if hero.active_willpower < 0:
                        hero.active_willpower = 0
                    hero.update_mask()
                self.active_condition.pop("附属到")
                if "行动后" in self.active_condition:
                    self.active_condition.pop("行动后")
                self._increment = [0, 0]
                self.limit_number = 3
                self.phase_mark = None
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = [self]
                self.update_mask()
                self.main_game.information = [0, "附属卡牌被弃除后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "行动" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self.main_game.hand_area.card_group:
                    cards = []
                    for card in self.main_game.hand_area.card_group:
                        if "免疫" not in card.rule_mark:
                            cards.append(card)
                    if cards:
                        card = self.main_game.card_select(cards)
                        card.card_order = ["被弃除", 0, 0, False, 0, 0]
                        self.main_game.response_conflict = True
                        self.card_order[1] += 1
                    else:
                        self.card_order = [None, 0, 0, None, 0, 0]
                else:
                    self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "行动" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif self.main_game.response_pause != True:
                self.main_game.response_pause = True
                self.main_game.button_option.import_button(str(self), (
                    ("+1防御力-" + self.active_condition["附属到"][0].card_name, None),
                    ("+1意志力-" + self.active_condition["附属到"][0].card_name, None)))
                if self.main_game.button_option.option // 100000 == 1:
                    self.phase_mark = self.main_game.threat_area.current_phase
                    self.active_condition["附属到"][0].active_defense_force += 1
                    self.active_condition["附属到"][0].update_mask()
                    self._increment[0] += 1
                    self.limit_number -= 1
                    if not self.limit_number:
                        self.active_condition["行动后"] = None
                        self.update_mask()
                    self.main_game.button_option.reset()
                    self.main_game.response_pause = False
                    self.card_order = [None, 0, 0, None, 0, 0]
                elif self.main_game.button_option.option // 100000 == 2:
                    self.phase_mark = self.main_game.threat_area.current_phase
                    self.active_condition["附属到"][0].active_willpower += 1
                    self.active_condition["附属到"][0].update_mask()
                    self._increment[1] += 1
                    self.limit_number -= 1
                    if not self.limit_number:
                        self.active_condition["行动后"] = None
                        self.update_mask()
                    self.main_game.button_option.reset()
                    self.main_game.response_pause = False
                    self.card_order = [None, 0, 0, None, 0, 0]
