from main import *


class Hero(Hero_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "葛罗音.jpg"  # 英雄卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 英雄卡牌的原始图像
        self.card_name = "葛罗音"  # 英雄的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.initial_threat = 9  # 英雄的初始威胁值
        self.willpower = 2  # 英雄的意志力
        self.attack_force = 2  # 英雄的攻击力
        self.defense_force = 1  # 英雄的防御力
        self.health_point = 4  # 英雄的生命值
        self.resource_symbol = "领导"  # 资源符号，表示本英雄的资源池中的资源标记(及英雄自身)隶属于哪个影响力派系
        self.card_attribute = ("矮人", "贵族")  # 英雄的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 英雄的规则关键词，表示英雄有些什么关键词
        self.rule_mark = ("响应",)  # 英雄的规则效果标志，表示英雄有些什么效果
        self.card_type = "英雄"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "响应：在葛罗音受到伤害后，他刚才每受到1点伤害，增加1枚资源标记到他的资源池中。"

        # 剧情描述的斜体文字
        self.describe_text = "他的胡子又长又卷，白得发亮，几乎像他所穿着的雪白上衣一样洁白。 ——《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.determine_health_point = self.active_health_point

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.active_health_point <= self.health_point:
            if self.active_health_point < self.determine_health_point:
                self.main_game.response_conflict = True
                self.card_order = ["响应", 0, 0, False, 0, 0]
                self.difference_value = self.determine_health_point - self.active_health_point
                self.determine_health_point = self.active_health_point
            elif self.active_health_point > self.determine_health_point:
                self.determine_health_point = self.active_health_point
        elif self.active_health_point > 0 and self.determine_health_point != self.health_point:
            self.determine_health_point = self.health_point

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
                    self.main_game.button_option.reset()
                    self.card_order[1] += 1
                elif self.main_game.button_option.option // 100000 == 2:
                    self.main_game.button_option.reset()
                    self.card_order[1] += 3
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if hasattr(self, "difference_value"):
                    self.main_game.information = [0, "英雄卡牌将要增加资源", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if hasattr(self, "difference_value"):
                    self.active_resource += self.difference_value
                    self.update_mask()
                    self.main_game.information = [0, "英雄卡牌增加资源后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                if hasattr(self, "difference_value"):
                    del self.difference_value
                self.main_game.response_pause = False
                self.card_order = [None, 0, 0, None, 0, 0]
