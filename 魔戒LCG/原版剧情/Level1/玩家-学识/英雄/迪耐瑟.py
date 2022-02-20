from main import *


class Hero(Hero_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "迪耐瑟.jpg"  # 英雄卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 英雄卡牌的原始图像
        self.card_name = "迪耐瑟"  # 英雄的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.initial_threat = 8  # 英雄的初始威胁值
        self.willpower = 1  # 英雄的意志力
        self.attack_force = 1  # 英雄的攻击力
        self.defense_force = 3  # 英雄的防御力
        self.health_point = 3  # 英雄的生命值
        self.resource_symbol = "学识"  # 资源符号，表示本英雄的资源池中的资源标记(及英雄自身)隶属于哪个影响力派系
        self.card_attribute = ("刚铎", "贵族", "摄政王")  # 英雄的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 英雄的规则关键词，表示英雄有些什么关键词
        self.rule_mark = ("行动",)  # 英雄的规则效果标志，表示英雄有些什么效果
        self.card_type = "英雄"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "行动：横置迪耐瑟，以查看遭遇牌组顶端的一张卡牌。你可以将该卡牌移至牌组底端。"

        # 剧情描述的斜体文字
        self.describe_text = "我主迪耐瑟和凡人不同，他可以看到十分远的地方。 ——贝瑞贡，《王者再临》"

        super().__init__()  # 初始化基类中的各种属性位置信息

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "行动" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要横置", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.active_condition["已横置"] = None
                self.update_mask()
                self.main_game.information = [0, "英雄卡牌横置后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "行动" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self.main_game.encounter_area.encounter_deck:
                    card = Print_Card(self.main_game)
                    card.card_image = self.main_game.computer_card_image.copy()
                    card_rect = card.card_image.get_rect()
                    font = pygame.font.Font(os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                                            card_rect.h // 6)
                    font_image = font.render("移至底端", True, self.main_game.settings.card_mask_font_color3)
                    font_image_rect = font_image.get_rect(center=card_rect.center)
                    card.card_image.blit(font_image, font_image_rect)
                    select_card = self.main_game.card_select((self.main_game.encounter_area.encounter_deck[0], card))
                    if select_card == card:
                        card = self.main_game.encounter_area.encounter_deck.pop(0)
                        card.reset_card()
                        card.update_mask()
                        self.main_game.encounter_area.encounter_deck.append(card)
                self.card_order = [None, 0, 0, None, 0, 0]
