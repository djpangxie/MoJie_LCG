from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "甘道夫的搜寻.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "甘道夫的搜寻"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = "X"  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "学识"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "事件"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：查看任一玩家牌组顶端的X张卡牌，将其中一张加入其拥有者的手牌，并将余下的卡牌按任意顺序放回牌组顶端。"

        # 剧情描述的斜体文字
        self.describe_text = "但我所遇见的迪耐瑟却不似过去的城主那般友善，他很不情愿地让我搜读他的众多卷轴和书籍。 ——甘道夫，《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.select_value = None
        self.temporary_card_cost = None

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "打出事件后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                cards = []
                if self.select_value and self.main_game.playerdeck_area.player_deck:
                    for num in range(len(self.main_game.playerdeck_area.player_deck)):
                        cards.append(self.main_game.playerdeck_area.player_deck.pop(0))
                        if num > self.select_value - 2:
                            break
                if cards:
                    select_card = self.main_game.card_select(cards)
                    cards.remove(select_card)
                    self.main_game.hand_area.card_group[select_card] = None
                    while cards:
                        select_card = self.main_game.card_select(cards)
                        cards.remove(select_card)
                        self.main_game.playerdeck_area.player_deck.insert(0, select_card)
                self.card_order[1] += 1
        elif self.card_order[0] == "打出事件后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if self.temporary_card_cost:
                    self.active_card_cost = self.temporary_card_cost
                    self.temporary_card_cost = None
                    self.update_mask()
                self.select_value = None
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
