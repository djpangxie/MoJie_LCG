from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "依鲁伯铁匠.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "依鲁伯铁匠"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 2  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "学识"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.willpower = 1  # 卡牌的意志力
        self.attack_force = 1  # 卡牌的攻击力
        self.defense_force = 1  # 卡牌的防御力
        self.health_point = 3  # 卡牌的生命值
        self.card_attribute = ("矮人", "工匠")  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("响应",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "盟友"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "响应：在你打出依鲁伯铁匠后，从任一玩家的弃牌堆中返回一张最顶部的附属牌到他的手牌。"

        # 剧情描述的斜体文字
        self.describe_text = "在丹恩的国度中，依鲁伯的工匠们有这种技术... ——亚拉冈，《王者再临》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.main_game.information and "玩家成功打出卡牌后" in self.main_game.information[
            1] and self.main_game.information[2] == self and str(self) not in self.main_game.information:
            self.main_game.response_conflict = True
            self.pause_card = self
            self.pause_card_order = self.card_order
            self.card_order = ["响应", 0, 0, False, 0, 0]
            self.copy_information = self.main_game.information
            self.main_game.information = None

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
                    card = None
                    if self.main_game.playerdiscard_area.playerdiscard_deck:
                        for card in self.main_game.playerdiscard_area.playerdiscard_deck:
                            if card.card_type == "附属":
                                break
                    if card is not None and card.card_type == "附属":
                        self.main_game.playerdiscard_area.playerdiscard_deck.remove(card)
                        card.reset_card()
                        card.update_mask()
                        self.main_game.hand_area.card_group[card] = None
                    self.card_order[1] += 1
                    self.main_game.button_option.reset()
                elif self.main_game.button_option.option // 100000 == 2:
                    self.card_order[1] += 1
                    self.main_game.button_option.reset()
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
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
