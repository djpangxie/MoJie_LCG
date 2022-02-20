from main import *


class Hero(Hero_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "勒苟拉斯.jpg"  # 英雄卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 英雄卡牌的原始图像
        self.card_name = "勒苟拉斯"  # 英雄的名称
        self.unique_symbol = True  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.initial_threat = 9  # 英雄的初始威胁值
        self.willpower = 1  # 英雄的意志力
        self.attack_force = 3  # 英雄的攻击力
        self.defense_force = 1  # 英雄的防御力
        self.health_point = 4  # 英雄的生命值
        self.resource_symbol = "战术"  # 资源符号，表示本英雄的资源池中的资源标记(及英雄自身)隶属于哪个影响力派系
        self.card_attribute = ("贵族", "西尔凡精灵", "战士")  # 英雄的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ("远攻",)  # 英雄的规则关键词，表示英雄有些什么关键词
        self.rule_mark = ("响应",)  # 英雄的规则效果标志，表示英雄有些什么效果
        self.card_type = "英雄"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "远攻.\n响应：在勒苟拉斯参与一次攻击并消灭敌军后，放置2枚进度标记到当前任务上。"

        # 剧情描述的斜体文字
        self.describe_text = "我可以这么走，但其他人可不行。 ——《魔戒现身》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self.attack_object = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if self.main_game.information and "英雄卡牌攻击后" in self.main_game.information[1] and self.main_game.information[
            2] == self and self.main_game.information[3] != self.attack_object:
            self.attack_object = self.main_game.information[3]
        elif self.attack_object is not None and "宣告攻击" not in self.active_condition and self.attack_object.active_health_point > 0:
            self.attack_object = None
        elif self.active_health_point > 0 and "响应后" not in self.active_condition and self.main_game.information and \
                self.main_game.information[1] == "敌军卡牌被消灭后" and self.main_game.information[2] == self.attack_object:
            self.main_game.response_conflict = True
            self.card_order = ["响应", 0, 0, False, 0, 0]
            self.active_condition["响应后"] = None
            self.attack_object = None

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
                    self.card_order[1] += 2
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                regions = []
                for region in self.main_game.task_area.region_card:
                    if region.card_type == "地区" and "免疫" not in region.rule_mark:
                        regions.append(region)
                if regions:
                    if len(regions) > 1:
                        region = self.main_game.card_select(regions)
                    else:
                        region = regions[0]
                    region.active_task_point -= 2
                    if region.active_task_point < 0:
                        region.active_task_point = 0
                    region.update_mask()
                elif not self.main_game.task_area.region_card and "免疫" not in self.main_game.task_area.task_deck[
                    self.main_game.task_area.task_number].rule_mark:
                    self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point -= 2
                    if self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point < 0:
                        self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point = 0
                    self.main_game.task_area.task_deck[self.main_game.task_area.task_number].update_mask()
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.response_pause = False
                self.active_condition.pop("响应后")
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
