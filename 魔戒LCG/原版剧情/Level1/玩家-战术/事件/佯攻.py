from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "佯攻.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "佯攻"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 1  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "战术"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("战斗行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "事件"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "战斗行动：选择一个与玩家交锋的敌军。该敌军本阶段不能攻击该玩家。"

        # 剧情描述的斜体文字
        self.describe_text = "少部分的人类被安插在敌军攻势的正前方，担任佯攻的任务，在接获往两边撤退诱敌的命令之前，许多人已经在猛烈的攻势下牺牲。 ——《哈比人》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.phase_mark = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if "目标卡牌" in self.active_condition and self.main_game.information and "卡牌将要执行暗影效果" in \
                self.main_game.information[1] and "暗影牌" in self.main_game.information[2].active_condition and \
                self.main_game.information[2].active_condition["暗影牌"][0] == self.active_condition["目标卡牌"][0]:
            self.main_game.information[2].card_order[2] = 1
            self.main_game.information[2].card_order[3] = False
            self.main_game.information = None
        if "目标卡牌" in self.active_condition and self.main_game.information and "敌军卡牌将要攻击" in self.main_game.information[
            1] and self.main_game.information[2] == self.active_condition["目标卡牌"][0]:
            if "战斗阶段" in self.main_game.information[1]:
                if self.main_game.threat_area.order[3]:
                    self.main_game.threat_area.order[5] = 1
                else:
                    self.main_game.threat_area.order[2] = 1
            else:
                if self.main_game.information[2].card_order[3]:
                    self.main_game.information[2].card_order[5] = 1
                else:
                    self.main_game.information[2].card_order[2] = 1
            self.main_game.information = None
        elif self.phase_mark is not None and self.main_game.threat_area.current_phase != self.phase_mark:
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
                enemys = []
                for card in self.main_game.clash_area.card_group:
                    if card.card_type == "敌军" and "免疫" not in card.rule_mark:
                        enemys.append(card)
                if enemys:
                    self.active_condition["目标卡牌"] = [self.main_game.card_select(enemys)]
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
