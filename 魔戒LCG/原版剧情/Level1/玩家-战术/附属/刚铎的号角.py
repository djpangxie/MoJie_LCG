from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "刚铎的号角.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "刚铎的号角"  # 卡牌的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 1  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "战术"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.card_attribute = ("物品", "宝物")  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ("限制",)  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("响应",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "附属"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "限制.\n附属到一名英雄上。\n响应：在一名角色被消灭后，增加1枚资源标记到所附属英雄的资源池中。"

        # 剧情描述的斜体文字
        self.describe_text = "“下次别再贸然吹动这号角，波罗莫，”爱隆说，“除非你再度踏上自己的国界，或是遭遇十万火急的危险。” ——《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if "附属到" in self.active_condition and "响应后" not in self.active_condition and self.main_game.information and (
                self.main_game.information[1] == "英雄卡牌被消灭后" or self.main_game.information[1] == "盟友卡牌被消灭后") and \
                self.main_game.information[2] != self.active_condition["附属到"][0]:
            self.main_game.response_conflict = True
            self.card_order = ["响应", 0, 0, False, 0, 0]
            self.active_condition["响应后"] = None

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
                self.card_order[1] += 1
        elif self.card_order[0] == "打出附属后" and self.card_order[1] == 2:
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
                    hero.update_mask()
                self.active_condition.pop("附属到")
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = [self]
                self.update_mask()
                self.main_game.information = [0, "附属卡牌被弃除后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "响应" and self.card_order[1] == 0:
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
                self.main_game.information = [0, "英雄卡牌将要增加资源", self, self.active_condition["附属到"][0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.active_condition["附属到"][0].active_resource += 1
                self.active_condition["附属到"][0].update_mask()
                self.main_game.information = [0, "英雄卡牌增加资源后", self, self.active_condition["附属到"][0]]
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.response_pause = False
                self.active_condition.pop("响应后")
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
