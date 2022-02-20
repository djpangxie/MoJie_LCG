from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "葛里欧温.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "葛里欧温"  # 卡牌的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 2  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "学识"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.willpower = 1  # 卡牌的意志力
        self.attack_force = 0  # 卡牌的攻击力
        self.defense_force = 0  # 卡牌的防御力
        self.health_point = 2  # 卡牌的生命值
        self.card_attribute = ("吟游诗人", "洛汗")  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "盟友"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：横置葛理欧温，以选择一位玩家。该玩家补一张卡牌。"

        # 剧情描述的斜体文字
        self.describe_text = "然后，王室的骠骑们骑着白马，绕着墓冢走，吟唱着王的吟游诗人葛里欧温为塞哲尔之子希优顿所作的诗歌。从那之后，葛里欧温就封琴退隐... ——《王者再临》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "行动" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌将要横置", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.active_condition["已横置"] = None
                self.update_mask()
                self.main_game.information = [0, "盟友卡牌横置后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                self.main_game.information = [0, "玩家将要补卡", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self.main_game.playerdeck_area.player_deck:
                    card = self.main_game.playerdeck_area.player_deck.pop(0)
                    self.main_game.hand_area.card_group[card] = None
                    self.main_game.information = [0, "玩家补卡后", self, card]
                self.card_order = [None, 0, 0, None, 0, 0]
