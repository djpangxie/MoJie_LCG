from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "森林诱捕网.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "森林诱捕网"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 3  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "学识"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.card_attribute = ("物品", "陷阱")  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ()  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "附属"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "附属到一个与玩家交锋的敌军上。\n所附属敌军不能攻击。"

        # 剧情描述的斜体文字
        self.describe_text = "我猜躲在那些蕨丛里面，他们这次插翅也难飞了。然后我们就可以知道这些家伙到底是什么东西。 ——身份不明的刚铎男子，《双城奇谋》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if "附属到" in self.active_condition and self.main_game.information and "卡牌将要执行暗影效果" in self.main_game.information[
            1] and "暗影牌" in self.main_game.information[2].active_condition and \
                self.main_game.information[2].active_condition["暗影牌"][0] == self.active_condition["附属到"][0]:
            self.main_game.information[2].card_order[2] = 1
            self.main_game.information[2].card_order[3] = False
            self.main_game.information = None
        if "附属到" in self.active_condition and self.main_game.information and "敌军卡牌将要攻击" in self.main_game.information[
            1] and self.main_game.information[2] == self.active_condition["附属到"][0]:
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

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "打出附属后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                enemys = []
                for enemy in self.main_game.clash_area.card_group:
                    if enemy.card_type == "敌军" and "免疫" not in enemy.rule_mark:
                        enemys.append(enemy)
                if enemys:
                    self.select_enemy = self.main_game.card_select(enemys)
                    self.main_game.information = [0, "附属卡牌将要附属", self, self.select_enemy]
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
                if self.main_game.card_estimate(self.select_enemy)[self.select_enemy]:
                    self.main_game.card_estimate(self.select_enemy)[self.select_enemy].append(self)
                else:
                    self.main_game.card_estimate(self.select_enemy)[self.select_enemy] = [self]
                if "被附属" not in self.select_enemy.active_condition or not self.select_enemy.active_condition["被附属"]:
                    self.select_enemy.active_condition["被附属"] = [self]
                else:
                    self.select_enemy.active_condition["被附属"].append(self)
                self.active_condition["附属到"] = [self.select_enemy]
                self.update_mask()
                self.select_enemy.update_mask()
                self.main_game.information = [0, "附属卡牌附属后", self, self.select_enemy]
                self.main_game.hand_area.card_group.pop(self)
                del self.select_enemy
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
                for enemy in self.active_condition["附属到"]:
                    enemy.active_condition["被附属"].remove(self)
                    if not enemy.active_condition["被附属"]:
                        enemy.active_condition.pop("被附属")
                    self.main_game.card_estimate(enemy)[enemy].remove(self)
                    enemy.update_mask()
                self.active_condition.pop("附属到")
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = [self]
                self.update_mask()
                self.main_game.information = [0, "附属卡牌被弃除后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
