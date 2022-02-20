from main import *


class Hero(Hero_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "金雳.jpg"  # 英雄卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 英雄卡牌的原始图像
        self.card_name = "金雳"  # 英雄的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.initial_threat = 11  # 英雄的初始威胁值
        self.willpower = 2  # 英雄的意志力
        self.attack_force = 2  # 英雄的攻击力
        self.defense_force = 2  # 英雄的防御力
        self.health_point = 5  # 英雄的生命值
        self.resource_symbol = "战术"  # 资源符号，表示本英雄的资源池中的资源标记(及英雄自身)隶属于哪个影响力派系
        self.card_attribute = ("矮人", "贵族", "战士")  # 英雄的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 英雄的规则关键词，表示英雄有些什么关键词
        self.rule_mark = ("永久",)  # 英雄的规则效果标志，表示英雄有些什么效果
        self.card_type = "英雄"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "金雳每有1枚伤害标记，他获得+1攻击力。"

        # 剧情描述的斜体文字
        self.describe_text = "人类每次要做什么事情总是要先说一大堆话，我的斧头都等得不耐烦了。 ——《双城奇谋》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.damage_mark = 0

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.active_health_point > 0 and self.damage_mark != self.health_point - self.active_health_point:
            if self.damage_mark > 0:
                self.active_attack_force -= self.damage_mark
            self.damage_mark = self.health_point - self.active_health_point
            if self.damage_mark > 0:
                self.active_attack_force += self.damage_mark
            if self.active_attack_force < 0:
                self.active_attack_force = 0
            self.update_mask()
