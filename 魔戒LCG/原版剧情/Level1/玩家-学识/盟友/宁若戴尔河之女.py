from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "宁若戴尔河之女.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "宁若戴尔河之女"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 3  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "学识"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.willpower = 1  # 卡牌的意志力
        self.attack_force = 0  # 卡牌的攻击力
        self.defense_force = 0  # 卡牌的防御力
        self.health_point = 1  # 卡牌的生命值
        self.card_attribute = ("西尔凡精灵",)  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("行动",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "盟友"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：横置宁若戴尔河之女，以治疗任一英雄的最多2点伤害。"

        # 剧情描述的斜体文字
        self.describe_text = "“这是宁若戴尔河！”勒苟拉斯说，“西尔凡精灵为了这条河作了许多歌谣，我们在北方依旧传唱着这些歌谣...我要在这里冲冲脚，据说这河水对于治疗疲倦有奇效。” ——勒苟拉斯，《魔戒现身》"

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
                if hasattr(self, "select_hero"):
                    del self.select_hero
                hero_group = []
                for hero in self.main_game.role_area.hero_group:
                    if hero.active_health_point < hero.health_point and "免疫" not in hero.rule_mark:
                        hero_group.append(hero)
                if hero_group:
                    self.select_hero = self.main_game.card_select(hero_group)
                    self.main_game.information = [0, "盟友卡牌将要治疗", self, self.select_hero]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if hasattr(self, "select_hero"):
                    self.select_hero.active_health_point += 2
                    if self.select_hero.active_health_point > self.select_hero.health_point:
                        self.select_hero.active_health_point = self.select_hero.health_point
                    self.select_hero.update_mask()
                    self.main_game.information = [0, "盟友卡牌治疗后", self, self.select_hero]
                    del self.select_hero
                self.card_order = [None, 0, 0, None, 0, 0]
