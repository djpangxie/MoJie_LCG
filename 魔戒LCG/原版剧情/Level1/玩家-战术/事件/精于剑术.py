from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "精于剑术.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "精于剑术"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 1  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "战术"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "事件"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：选择一名角色。该角色获得+1攻击力和+1防御力直到本阶段结束。"

        # 剧情描述的斜体文字
        self.describe_text = "他掀开斗篷，将手放到腰间刻意隐匿的剑柄上。众人动也不敢动。 ——《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.phase_mark = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if "目标卡牌" in self.active_condition and not self.main_game.on_spot(self.active_condition["目标卡牌"][
                                                                              0]) or self.phase_mark is not None and self.main_game.threat_area.current_phase != self.phase_mark:
            if self.main_game.on_spot(self.active_condition["目标卡牌"][0]):
                self.active_condition["目标卡牌"][0].active_attack_force -= 1
                if self.active_condition["目标卡牌"][0].active_attack_force < 0:
                    self.active_condition["目标卡牌"][0].active_attack_force = 0
                self.active_condition["目标卡牌"][0].active_defense_force -= 1
                if self.active_condition["目标卡牌"][0].active_defense_force < 0:
                    self.active_condition["目标卡牌"][0].active_defense_force = 0
                self.active_condition["目标卡牌"][0].update_mask()
            self.active_condition.pop("目标卡牌")
            self.update_mask()
            our_affiliate = []
            enemy_affiliate = []
            if self.main_game.role_area.card_group[self]:
                for card in self.main_game.role_area.card_group[self]:
                    if self.main_game.player_control(card):
                        our_affiliate.append(card)
                    else:
                        enemy_affiliate.append(card)
            self.main_game.role_area.card_group.pop(self)
            if self.main_game.playerdiscard_area.playerdiscard_deck:
                for card in our_affiliate:
                    self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, card)
                self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
            else:
                self.main_game.playerdiscard_area.playerdiscard_deck = [self]
                self.main_game.playerdiscard_area.playerdiscard_deck.extend(our_affiliate)
            if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                for card in enemy_affiliate:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, card)
            else:
                self.main_game.encounterdiscard_area.encounterdiscard_deck = enemy_affiliate
            self.phase_mark = None

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "打出事件后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                cards = []
                for card in self.main_game.role_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "免疫" not in card.rule_mark:
                        cards.append(card)
                for card in self.main_game.clash_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "免疫" not in card.rule_mark:
                        cards.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if (card.card_type == "英雄" or card.card_type == "盟友") and "免疫" not in card.rule_mark:
                        cards.append(card)
                if cards:
                    self.active_condition["目标卡牌"] = [self.main_game.card_select(cards)]
                    self.active_condition["目标卡牌"][0].active_attack_force += 1
                    self.active_condition["目标卡牌"][0].active_defense_force += 1
                    self.active_condition["目标卡牌"][0].update_mask()
                    self.active_condition["行动后"] = None
                    self.update_mask()
                    self.main_game.role_area.card_group[self] = self.main_game.hand_area.card_group.pop(self)
                    self.phase_mark = self.main_game.threat_area.current_phase
                    self.card_order = [None, 0, 0, None, 0, 0]
                else:
                    self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                our_affiliate = []
                enemy_affiliate = []
                if self.main_game.hand_area.card_group[self]:
                    for card in self.main_game.hand_area.card_group[self]:
                        if self.main_game.player_control(card):
                            our_affiliate.append(card)
                        else:
                            enemy_affiliate.append(card)
                self.main_game.hand_area.card_group.pop(self)
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    for card in our_affiliate:
                        self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, card)
                    self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = [self]
                    self.main_game.playerdiscard_area.playerdiscard_deck.extend(our_affiliate)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    for card in enemy_affiliate:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, card)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = enemy_affiliate
                self.card_order = [None, 0, 0, None, 0, 0]
