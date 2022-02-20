from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "大地的力量.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "大地的力量"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 1  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "精神"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.card_attribute = ("状态",)  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ()  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "附属"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "附属到一个地区上。\n所附属地区获得-1威胁值。"

        # 剧情描述的斜体文字
        self.describe_text = "“他并无阻挡魔王的力量，除非这种力量来自大地本身。” ——甘道夫，《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._successful = None

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "打出附属后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                regions = []
                for card in self.main_game.task_area.region_card:
                    if card.card_type == "地区" and "免疫" not in card.rule_mark:
                        regions.append(card)
                for card in self.main_game.scenario_area.card_group:
                    if card.card_type == "地区" and "免疫" not in card.rule_mark:
                        regions.append(card)
                for card in self.main_game.clash_area.card_group:
                    if card.card_type == "地区" and "免疫" not in card.rule_mark:
                        regions.append(card)
                for card in self.main_game.role_area.card_group:
                    if card.card_type == "地区" and "免疫" not in card.rule_mark:
                        regions.append(card)
                if regions:
                    self.select_region = self.main_game.card_select(regions)
                    self.main_game.information = [0, "附属卡牌将要附属", self, self.select_region]
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
                if self.main_game.card_estimate(self.select_region)[self.select_region]:
                    self.main_game.card_estimate(self.select_region)[self.select_region].append(self)
                else:
                    self.main_game.card_estimate(self.select_region)[self.select_region] = [self]
                if "被附属" not in self.select_region.active_condition or not self.select_region.active_condition["被附属"]:
                    self.select_region.active_condition["被附属"] = [self]
                else:
                    self.select_region.active_condition["被附属"].append(self)
                self.active_condition["附属到"] = [self.select_region]
                self.select_region.active_threat_force -= 1
                self._successful = True
                if self.select_region.active_threat_force < 0:
                    self.select_region.active_threat_force = 0
                    self._successful = False
                self.update_mask()
                self.select_region.update_mask()
                self.main_game.information = [0, "附属卡牌附属后", self, self.select_region]
                self.main_game.hand_area.card_group.pop(self)
                del self.select_region
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
                for region in self.active_condition["附属到"]:
                    region.active_condition["被附属"].remove(self)
                    if not region.active_condition["被附属"]:
                        region.active_condition.pop("被附属")
                    self.main_game.card_estimate(region)[region].remove(self)
                    if self._successful:
                        region.active_threat_force += 1
                        self._successful = None
                    region.update_mask()
                self.active_condition.pop("附属到")
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = [self]
                self.update_mask()
                self.main_game.information = [0, "附属卡牌被弃除后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
