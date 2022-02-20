from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "长枪方阵.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "长枪方阵"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 3  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "战术"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "事件"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "你必须使用来自三名不同英雄的资源池中的资源标记，以支付本卡牌。\n行动：选择一位玩家。与该玩家交锋的敌军本阶段不能攻击该玩家。"

        # 剧情描述的斜体文字
        self.describe_text = "毫无预警地，骑士们突然停了下来。密密的长枪一起指向圆心中的三人... ——《双城奇谋》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.phase_mark = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.phase_mark != None and self.main_game.information and "卡牌将要执行暗影效果" in self.main_game.information[
            1] and "暗影牌" in self.main_game.information[2].active_condition and \
                self.main_game.information[2].active_condition["暗影牌"][
                    0] in self.main_game.clash_area.card_group and "免疫" not in \
                self.main_game.information[2].active_condition["暗影牌"][0].rule_mark:
            self.main_game.information[2].card_order[2] = 1
            self.main_game.information[2].card_order[3] = False
            self.main_game.information = None
        if self.phase_mark != None and self.main_game.information and "敌军卡牌将要攻击" in self.main_game.information[1] and \
                self.main_game.information[2] in self.main_game.clash_area.card_group and "免疫" not in \
                self.main_game.information[2].rule_mark:
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
        elif self.phase_mark != None and self.main_game.threat_area.current_phase != self.phase_mark:
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
        if self.card_order[0] == "打出" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                point = 0
                heros = []
                for hero in self.main_game.role_area.hero_group:
                    if self.faction_symbol == hero.resource_symbol or "资源符+" in hero.active_condition and self.faction_symbol in \
                            hero.active_condition["资源符+"]:
                        heros.append(hero)
                for hero in heros:
                    point += hero.active_resource
                # 卡牌打出失败
                if len(heros) < 3 or point < self.active_card_cost:
                    self.card_order[0] = None
                    return
                # END
                self.deduction_heros = []
                for hero in heros:
                    self.deduction_heros.append([hero, 0])
                if self.active_card_cost < 3:
                    point = self.active_card_cost
                else:
                    point = 3
                random.shuffle(self.deduction_heros)
                for hero in self.deduction_heros:
                    if point <= 0:
                        break
                    elif hero[0].active_resource > 0:
                        hero[1] += 1
                        point -= 1
                if point > 0:
                    del self.deduction_heros
                    self.card_order[0] = None
                    return
                point = self.active_card_cost
                for hero in self.deduction_heros:
                    point -= hero[1]
                while point > 0:
                    for hero in self.deduction_heros:
                        if hero[0].active_resource > hero[1] and not random.randrange(len(heros)):
                            hero[1] += 1
                            point -= 1
                            if point <= 0:
                                break
                self.main_game.information = [0, "玩家将要打出卡牌", self]
                self.card_order[3] = True
                self.card_order[4] = 0
                self.card_order[5] = 0
                self.card_order[1] += 1
        elif self.card_order[0] == "打出" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information and self.card_order[3]:
                if self.card_order[5]:
                    self.card_order[4] += 1
                    self.card_order[5] -= 1
                    for hero in self.deduction_heros:
                        if hero[1] > 0:
                            hero[1] -= 1
                            break
                elif self.card_order[4] % 2:
                    for hero in self.deduction_heros:
                        if hero[1] > 0:
                            hero[1] -= 1
                            hero[0].active_resource -= 1
                            if hero[0].active_resource < 0:
                                hero[0].active_resource = 0
                            hero[0].update_mask()
                            self.main_game.information = [0, "英雄支付费用后", self, hero[0]]
                            break
                    self.card_order[4] += 1
                else:
                    for hero in self.deduction_heros:
                        if hero[1] > 0:
                            self.main_game.information = [0, "英雄将要支付费用", self, hero[0]]
                            self.card_order[4] += 1
                            return
                    del self.deduction_heros
                    self.main_game.information = [0, "玩家成功打出卡牌后", self]
                    self.card_order = ["打出事件后", 0, 0, False, 0, 0]
        elif self.card_order[0] != "打出":
            super().run_card_order()
        if self.card_order[0] == "打出事件后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.role_area.card_group[self] = self.main_game.hand_area.card_group.pop(self)
                self.phase_mark = self.main_game.threat_area.current_phase
                self.active_condition["行动后"] = None
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
